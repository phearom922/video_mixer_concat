"""Public API endpoints for desktop app."""
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Request, Depends
from app.models.activation import (
    ActivationRequest,
    ActivationResponse,
    ValidateRequest,
    ValidateResponse
)
from app.models.release import LatestReleaseResponse
from app.services.jwt_service import create_activation_token, verify_activation_token
from app.services.device_hash import hash_device_fingerprint
from app.services.rate_limiter import rate_limiter
from app.services.license_service import (
    get_license_by_key,
    is_license_valid,
    count_active_activations
)
from app.services.activation_service import (
    get_activation_by_device_hash,
    create_activation,
    update_activation_last_seen
)
from app.database import get_supabase_client
from app.config import settings
from supabase import Client

router = APIRouter()


def get_client_ip(request: Request) -> str:
    """Get client IP address."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


@router.post("/activate", response_model=ActivationResponse)
async def activate_license(
    request: ActivationRequest,
    http_request: Request = None
):
    """
    Activate a license with device fingerprint.
    
    Rate limited: 5 requests per minute per IP.
    """
    # Rate limiting
    client_ip = get_client_ip(http_request) if http_request else "unknown"
    allowed, remaining = rate_limiter.is_allowed(
        f"activate:{client_ip}",
        settings.RATE_LIMIT_ACTIVATE_PER_MINUTE,
        60
    )
    
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Try again later."
        )
    
    supabase: Client = get_supabase_client()
    
    # Get license
    license_data = get_license_by_key(supabase, request.license_key)
    if not license_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="License key not found"
        )
    
    # Validate license
    is_valid, reason = is_license_valid(license_data)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=reason or "License is not valid"
        )
    
    # Hash device fingerprint
    device_id_hash = hash_device_fingerprint(request.device_fingerprint)
    
    # Check existing activation
    existing_activation = get_activation_by_device_hash(
        supabase,
        license_data["id"],
        device_id_hash
    )
    
    if existing_activation:
        # Update existing activation
        if existing_activation.get("status") == "revoked":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This device activation has been revoked"
            )
        
        # Reactivate or update
        activation_data = existing_activation
        activation_data["last_seen_at"] = datetime.utcnow().isoformat()
        activation_data["activated_app_version"] = request.app_version
        
        try:
            supabase.table("activations").update({
                "last_seen_at": activation_data["last_seen_at"],
                "activated_app_version": request.app_version,
                "status": "active"
            }).eq("id", activation_data["id"]).execute()
        except Exception as e:
            error_msg = str(e)
            if "PGRST205" not in error_msg and "schema cache" not in error_msg.lower():
                raise
    else:
        # Check activation limit
        active_count = count_active_activations(supabase, license_data["id"])
        max_activations = license_data.get("max_activations", 1)
        
        if active_count >= max_activations:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Maximum activations ({max_activations}) reached for this license"
            )
        
        # Create new activation
        activation_data = create_activation(
            supabase,
            license_data["id"],
            device_id_hash,
            request.device_label,
            request.app_version
        )
    
    # Create JWT token
    activation_token = create_activation_token(
        str(license_data["id"]),
        str(activation_data["id"]),
        device_id_hash
    )
    
    # Prepare response
    expires_at = license_data.get("expires_at")
    if expires_at and isinstance(expires_at, str):
        try:
            expires_at = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
        except ValueError:
            expires_at = None
    
    return ActivationResponse(
        activation_token=activation_token,
        license={
            "id": license_data["id"],
            "customer_name": license_data.get("customer_name"),
            "max_activations": license_data.get("max_activations", 1),
            "status": license_data.get("status"),
            "expires_at": expires_at.isoformat() if expires_at else None
        },
        activation={
            "id": activation_data["id"],
            "device_label": activation_data.get("device_label"),
            "activated_app_version": activation_data.get("activated_app_version"),
            "first_activated_at": activation_data.get("first_activated_at"),
            "last_seen_at": activation_data.get("last_seen_at")
        },
        grace_days=settings.GRACE_DAYS
    )


@router.post("/validate", response_model=ValidateResponse)
async def validate_license(
    request: ValidateRequest,
    http_request: Request = None
):
    """
    Validate an activation token.
    
    Rate limited: 60 requests per minute per token.
    """
    # Get token from Authorization header
    auth_header = http_request.headers.get("Authorization") if http_request else None
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header"
        )
    
    token = auth_header.replace("Bearer ", "")
    
    # Rate limiting by token
    allowed, remaining = rate_limiter.is_allowed(
        f"validate:{token[:20]}",
        settings.RATE_LIMIT_VALIDATE_PER_MINUTE,
        60
    )
    
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded"
        )
    
    # Verify token
    payload = verify_activation_token(token)
    if not payload:
        return ValidateResponse(
            valid=False,
            reason="Invalid or expired activation token",
            server_time=datetime.utcnow()
        )
    
    supabase: Client = get_supabase_client()
    
    # Get activation
    activation_id = payload.get("activation_id")
    license_id = payload.get("license_id")
    
    try:
        activation_response = supabase.table("activations").select("*").eq(
            "id", activation_id
        ).execute()
    except Exception as e:
        error_msg = str(e)
        if "PGRST205" in error_msg or "schema cache" in error_msg.lower():
            return ValidateResponse(
                valid=False,
                reason="Database schema cache is being refreshed. Please try again in a moment.",
                server_time=datetime.utcnow()
            )
        raise
    
    if not activation_response.data:
        return ValidateResponse(
            valid=False,
            reason="Activation not found",
            server_time=datetime.utcnow()
        )
    
    activation = activation_response.data[0]
    
    # Check activation status
    if activation.get("status") == "revoked":
        return ValidateResponse(
            valid=False,
            reason="Activation has been revoked",
            server_time=datetime.utcnow()
        )
    
    # Get license by ID
    try:
        license_response = supabase.table("licenses").select("*").eq("id", license_id).execute()
    except Exception as e:
        error_msg = str(e)
        if "PGRST205" in error_msg or "schema cache" in error_msg.lower():
            return ValidateResponse(
                valid=False,
                reason="Database schema cache is being refreshed. Please try again in a moment.",
                server_time=datetime.utcnow()
            )
        raise
    
    if not license_response.data:
        return ValidateResponse(
            valid=False,
            reason="License not found",
            server_time=datetime.utcnow()
        )
    license_data = license_response.data[0]
    
    if not license_data:
        return ValidateResponse(
            valid=False,
            reason="License not found",
            server_time=datetime.utcnow()
        )
    
    # Validate license
    is_valid, reason = is_license_valid(license_data)
    if not is_valid:
        return ValidateResponse(
            valid=False,
            reason=reason or "License is not valid",
            server_time=datetime.utcnow()
        )
    
    # Update last_seen_at
    update_activation_last_seen(supabase, activation_id)
    
    expires_at = license_data.get("expires_at")
    if expires_at and isinstance(expires_at, str):
        try:
            expires_at = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
        except ValueError:
            expires_at = None
    
    return ValidateResponse(
        valid=True,
        expires_at=expires_at,
        status=license_data.get("status"),
        server_time=datetime.utcnow()
    )


@router.post("/deactivate")
async def deactivate_license(http_request: Request = None):
    """
    Deactivate an activation (revoke device activation).
    """
    auth_header = http_request.headers.get("Authorization") if http_request else None
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header"
        )
    
    token = auth_header.replace("Bearer ", "")
    
    # Verify token
    payload = verify_activation_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired activation token"
        )
    
    supabase: Client = get_supabase_client()
    activation_id = payload.get("activation_id")
    
    # Revoke activation
    from app.services.activation_service import revoke_activation
    revoke_activation(supabase, activation_id)
    
    return {"success": True, "message": "Activation deactivated successfully"}


@router.get("/releases/latest", response_model=LatestReleaseResponse)
async def get_latest_release(
    platform: str = "windows",
    current_version: str = "0.0.0"
):
    """
    Get latest release information for update checking.
    """
    supabase: Client = get_supabase_client()
    
    # Get latest release for platform
    try:
        response = supabase.table("app_releases").select("*").eq(
            "platform", platform
        ).eq("is_latest", True).execute()
    except Exception as e:
        error_msg = str(e)
        if "PGRST205" in error_msg or "schema cache" in error_msg.lower():
            # Return no update available if schema cache not ready
            return ReleaseResponse(
                update_available=False,
                latest_version=current_version,
                release_notes="",
                download_url=""
            )
        raise
    
    if not response.data or len(response.data) == 0:
        return LatestReleaseResponse(update_available=False)
    
    latest_release = response.data[0]
    latest_version = latest_release.get("version", "0.0.0")
    
    # Simple semver comparison (basic implementation)
    def compare_versions(v1: str, v2: str) -> int:
        """Compare two version strings. Returns 1 if v1 > v2, -1 if v1 < v2, 0 if equal."""
        v1_parts = [int(x) for x in v1.split(".")]
        v2_parts = [int(x) for x in v2.split(".")]
        
        max_len = max(len(v1_parts), len(v2_parts))
        v1_parts.extend([0] * (max_len - len(v1_parts)))
        v2_parts.extend([0] * (max_len - len(v2_parts)))
        
        for i in range(max_len):
            if v1_parts[i] > v2_parts[i]:
                return 1
            elif v1_parts[i] < v2_parts[i]:
                return -1
        return 0
    
    update_available = compare_versions(latest_version, current_version) > 0
    
    return LatestReleaseResponse(
        update_available=update_available,
        latest_version=latest_version if update_available else None,
        release_notes=latest_release.get("release_notes") if update_available else None,
        download_url=latest_release.get("download_url") if update_available else None
    )
