"""Admin API endpoints for dashboard."""
import secrets
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Depends
from app.models.license import LicenseCreate, LicenseResponse, LicenseUpdate
from app.models.activation import ActivationInfo
from app.models.release import ReleaseCreate, ReleaseResponse, ReleaseUpdate
from app.middleware.auth import verify_admin_token
from app.database import get_supabase_client, insert_via_direct_sql
from supabase import Client

router = APIRouter()


def generate_license_key(length: int = 32) -> str:
    """Generate a secure random license key."""
    # Use URL-safe base64 encoding for readability
    return secrets.token_urlsafe(length)


def log_admin_action(
    supabase: Client,
    admin_user_id: str,
    action: str,
    payload: dict
):
    """Log an admin action to audit log."""
    try:
        supabase.table("admin_audit_logs").insert({
            "admin_user_id": admin_user_id,
            "action": action,
            "payload": payload
        }).execute()
    except Exception as e:
        # Silently fail audit logging if PostgREST schema cache not ready
        # This allows the main operation to succeed
        error_msg = str(e)
        if "PGRST205" not in error_msg and "schema cache" not in error_msg.lower():
            raise


@router.post("/licenses", response_model=LicenseResponse)
async def create_license(
    license_data: LicenseCreate,
    admin: dict = Depends(verify_admin_token)
):
    """Create a new license."""
    supabase: Client = get_supabase_client()
    
    # Generate license key
    license_key = generate_license_key(32)
    
    # Ensure unique key
    max_attempts = 10
    for _ in range(max_attempts):
        try:
            existing = supabase.table("licenses").select("id").eq(
                "license_key", license_key
            ).execute()
            if not existing.data:
                break
        except Exception as e:
            error_msg = str(e)
            if "PGRST205" in error_msg or "schema cache" in error_msg.lower():
                # Schema cache not ready, assume key is unique
                break
            raise
        license_key = generate_license_key(32)
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate unique license key"
        )
    
    # Create license
    data = {
        "license_key": license_key,
        "customer_name": license_data.customer_name,
        "max_activations": license_data.max_activations,
        "status": license_data.status,
        "expires_at": license_data.expires_at.isoformat() if license_data.expires_at else None,
        "notes": license_data.notes
    }
    
    # Try PostgREST with retry logic
    max_retries = 3
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            response = supabase.table("licenses").insert(data).execute()
            if not response.data:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create license"
                )
            created_license = response.data[0]
            break  # Success, exit retry loop
        except Exception as e:
            error_msg = str(e)
            if "PGRST205" in error_msg or "schema cache" in error_msg.lower():
                if attempt < max_retries - 1:
                    # Wait before retry
                    import time
                    time.sleep(retry_delay)
                    continue
                else:
                    # All retries failed, try direct HTTP as last resort
                    try:
                        result = insert_via_direct_sql("licenses", data)
                        if not result:
                            raise HTTPException(
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Failed to create license (direct HTTP fallback)"
                            )
                        created_license = result[0]
                        break  # Success with fallback
                    except Exception as fallback_error:
                        # If direct HTTP also fails, return 503 with helpful message
                        raise HTTPException(
                            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Database schema cache is still being refreshed. Please wait a few more minutes and try again. If the problem persists, please restart the Supabase project again."
                        )
            else:
                # Non-schema-cache error, raise immediately
                raise
    
    # Log action
    log_admin_action(
        supabase,
        admin["user_id"],
        "CREATE_LICENSE",
        {
            "license_id": str(created_license["id"]),
            "license_key": license_key,
            "customer_name": license_data.customer_name
        }
    )
    
    return LicenseResponse(**created_license)


@router.get("/licenses", response_model=List[LicenseResponse])
async def list_licenses(
    search: Optional[str] = None,
    status_filter: Optional[str] = None,
    admin: dict = Depends(verify_admin_token)
):
    """List all licenses with optional search and filter."""
    supabase: Client = get_supabase_client()
    
    try:
        query = supabase.table("licenses").select("*")
        
        if search:
            # Search in license_key and customer_name
            query = query.or_(f"license_key.ilike.%{search}%,customer_name.ilike.%{search}%")
        
        if status_filter:
            query = query.eq("status", status_filter)
        
        query = query.order("created_at", desc=True)
        
        response = query.execute()
        
        return [LicenseResponse(**item) for item in response.data]
    except Exception as e:
        error_msg = str(e)
        if "PGRST205" in error_msg or "schema cache" in error_msg.lower():
            # Return empty list instead of error to allow dashboard to load
            # The schema cache will eventually refresh
            return []
        raise


@router.get("/licenses/{license_id}", response_model=LicenseResponse)
async def get_license(
    license_id: str,
    admin: dict = Depends(verify_admin_token)
):
    """Get a specific license by ID."""
    supabase: Client = get_supabase_client()
    
    try:
        response = supabase.table("licenses").select("*").eq("id", license_id).execute()
    except Exception as e:
        error_msg = str(e)
        if "PGRST205" in error_msg or "schema cache" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database schema cache is being refreshed. Please wait a moment and try again."
            )
        raise
    
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="License not found"
        )
    
    return LicenseResponse(**response.data[0])


@router.put("/licenses/{license_id}", response_model=LicenseResponse)
async def update_license(
    license_id: str,
    license_data: LicenseUpdate,
    admin: dict = Depends(verify_admin_token)
):
    """Update a license."""
    supabase: Client = get_supabase_client()
    
    # Check if license exists
    try:
        existing = supabase.table("licenses").select("*").eq("id", license_id).execute()
    except Exception as e:
        error_msg = str(e)
        if "PGRST205" in error_msg or "schema cache" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database schema cache is being refreshed. Please wait a moment and try again."
            )
        raise
    
    if not existing.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="License not found"
        )
    
    # Build update data
    update_data = {}
    if license_data.customer_name is not None:
        update_data["customer_name"] = license_data.customer_name
    if license_data.max_activations is not None:
        update_data["max_activations"] = license_data.max_activations
    if license_data.status is not None:
        update_data["status"] = license_data.status
    if license_data.expires_at is not None:
        update_data["expires_at"] = license_data.expires_at.isoformat()
    if license_data.notes is not None:
        update_data["notes"] = license_data.notes
    
    if not update_data:
        return LicenseResponse(**existing.data[0])
    
    try:
        response = supabase.table("licenses").update(update_data).eq("id", license_id).execute()
    except Exception as e:
        error_msg = str(e)
        if "PGRST205" in error_msg or "schema cache" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database schema cache is being refreshed. Please wait a moment and try again."
            )
        raise
    
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update license"
        )
    
    # Log action
    log_admin_action(
        supabase,
        admin["user_id"],
        "UPDATE_LICENSE",
        {
            "license_id": license_id,
            "updates": update_data
        }
    )
    
    return LicenseResponse(**response.data[0])


@router.post("/licenses/{license_id}/revoke")
async def revoke_license(
    license_id: str,
    admin: dict = Depends(verify_admin_token)
):
    """Revoke a license."""
    supabase: Client = get_supabase_client()
    
    # Check if license exists
    try:
        existing = supabase.table("licenses").select("*").eq("id", license_id).execute()
    except Exception as e:
        error_msg = str(e)
        if "PGRST205" in error_msg or "schema cache" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database schema cache is being refreshed. Please wait a moment and try again."
            )
        raise
    
    if not existing.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="License not found"
        )
    
    # Update status
    try:
        response = supabase.table("licenses").update({
            "status": "revoked"
        }).eq("id", license_id).execute()
    except Exception as e:
        error_msg = str(e)
        if "PGRST205" in error_msg or "schema cache" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database schema cache is being refreshed. Please wait a moment and try again."
            )
        raise
    
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to revoke license"
        )
    
    # Log action
    log_admin_action(
        supabase,
        admin["user_id"],
        "REVOKE_LICENSE",
        {
            "license_id": license_id
        }
    )
    
    return {"success": True, "message": "License revoked successfully"}


@router.get("/licenses/{license_id}/activations", response_model=List[ActivationInfo])
async def get_license_activations(
    license_id: str,
    admin: dict = Depends(verify_admin_token)
):
    """Get all activations for a license."""
    supabase: Client = get_supabase_client()
    
    try:
        response = supabase.table("activations").select("*").eq(
            "license_id", license_id
        ).order("created_at", desc=True).execute()
    except Exception as e:
        error_msg = str(e)
        if "PGRST205" in error_msg or "schema cache" in error_msg.lower():
            # Return empty list if schema cache not ready
            return []
        raise
    
    return [ActivationInfo(**item) for item in response.data]


@router.post("/activations/{activation_id}/revoke")
async def revoke_activation(
    activation_id: str,
    admin: dict = Depends(verify_admin_token)
):
    """Revoke a specific activation."""
    supabase: Client = get_supabase_client()
    
    # Check if activation exists
    try:
        existing = supabase.table("activations").select("*").eq("id", activation_id).execute()
    except Exception as e:
        error_msg = str(e)
        if "PGRST205" in error_msg or "schema cache" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database schema cache is being refreshed. Please wait a moment and try again."
            )
        raise
    
    if not existing.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activation not found"
        )
    
    # Revoke activation
    try:
        response = supabase.table("activations").update({
            "status": "revoked"
        }).eq("id", activation_id).execute()
    except Exception as e:
        error_msg = str(e)
        if "PGRST205" in error_msg or "schema cache" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database schema cache is being refreshed. Please wait a moment and try again."
            )
        raise
    
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to revoke activation"
        )
    
    # Log action
    log_admin_action(
        supabase,
        admin["user_id"],
        "REVOKE_ACTIVATION",
        {
            "activation_id": activation_id,
            "license_id": existing.data[0]["license_id"]
        }
    )
    
    return {"success": True, "message": "Activation revoked successfully"}


@router.post("/releases", response_model=ReleaseResponse)
async def create_release(
    release_data: ReleaseCreate,
    admin: dict = Depends(verify_admin_token)
):
    """Create a new app release."""
    supabase: Client = get_supabase_client()
    
    # If this is marked as latest, unset previous latest for this platform
    if release_data.is_latest:
        try:
            supabase.table("app_releases").update({
                "is_latest": False
            }).eq("platform", release_data.platform).eq("is_latest", True).execute()
        except Exception as e:
            error_msg = str(e)
            if "PGRST205" not in error_msg and "schema cache" not in error_msg.lower():
                raise
    
    # Create release
    data = {
        "platform": release_data.platform,
        "version": release_data.version,
        "release_notes": release_data.release_notes,
        "download_url": release_data.download_url,
        "is_latest": release_data.is_latest
    }
    
    try:
        response = supabase.table("app_releases").insert(data).execute()
    except Exception as e:
        error_msg = str(e)
        if "PGRST205" in error_msg or "schema cache" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database schema cache is being refreshed. Please wait a moment and try again."
            )
        raise
    
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create release"
        )
    
    created_release = response.data[0]
    
    # Log action
    log_admin_action(
        supabase,
        admin["user_id"],
        "CREATE_RELEASE",
        {
            "release_id": str(created_release["id"]),
            "platform": release_data.platform,
            "version": release_data.version
        }
    )
    
    return ReleaseResponse(**created_release)


@router.get("/releases", response_model=List[ReleaseResponse])
async def list_releases(
    platform: Optional[str] = None,
    admin: dict = Depends(verify_admin_token)
):
    """List all releases."""
    supabase: Client = get_supabase_client()
    
    try:
        query = supabase.table("app_releases").select("*")
        
        if platform:
            query = query.eq("platform", platform)
        
        query = query.order("created_at", desc=True)
        
        response = query.execute()
        
        return [ReleaseResponse(**item) for item in response.data]
    except Exception as e:
        error_msg = str(e)
        if "PGRST205" in error_msg or "schema cache" in error_msg.lower():
            # Return empty list if schema cache not ready
            return []
        raise


@router.post("/releases/{release_id}/set-latest")
async def set_latest_release(
    release_id: str,
    admin: dict = Depends(verify_admin_token)
):
    """Set a release as the latest for its platform."""
    supabase: Client = get_supabase_client()
    
    # Get release
    try:
        release_response = supabase.table("app_releases").select("*").eq("id", release_id).execute()
    except Exception as e:
        error_msg = str(e)
        if "PGRST205" in error_msg or "schema cache" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database schema cache is being refreshed. Please wait a moment and try again."
            )
        raise
    
    if not release_response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Release not found"
        )
    
    release = release_response.data[0]
    platform = release["platform"]
    
    # Unset previous latest for this platform
    try:
        supabase.table("app_releases").update({
            "is_latest": False
        }).eq("platform", platform).eq("is_latest", True).execute()
    except Exception as e:
        error_msg = str(e)
        if "PGRST205" not in error_msg and "schema cache" not in error_msg.lower():
            raise
    
    # Set this as latest
    try:
        response = supabase.table("app_releases").update({
            "is_latest": True
        }).eq("id", release_id).execute()
    except Exception as e:
        error_msg = str(e)
        if "PGRST205" in error_msg or "schema cache" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database schema cache is being refreshed. Please wait a moment and try again."
            )
        raise
    
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to set latest release"
        )
    
    # Log action
    log_admin_action(
        supabase,
        admin["user_id"],
        "UPDATE_RELEASE",
        {
            "release_id": release_id,
            "action": "set_latest",
            "platform": platform,
            "version": release["version"]
        }
    )
    
    return {"success": True, "message": "Release set as latest"}


@router.get("/audit-logs")
async def get_audit_logs(
    limit: int = 100,
    admin: dict = Depends(verify_admin_token)
):
    """Get admin audit logs."""
    supabase: Client = get_supabase_client()
    
    try:
        response = supabase.table("admin_audit_logs").select(
            "*, admin_user_id"
        ).order("created_at", desc=True).limit(limit).execute()
        
        return response.data
    except Exception as e:
        error_msg = str(e)
        if "PGRST205" in error_msg or "schema cache" in error_msg.lower():
            # Return empty list if schema cache not ready
            return []
        raise
