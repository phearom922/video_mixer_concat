"""License service for validation and management."""
from datetime import datetime
from typing import Optional
from supabase import Client
from app.models.license import LicenseResponse


def get_license_by_key(supabase: Client, license_key: str) -> Optional[dict]:
    """Get license by license key."""
    try:
        response = supabase.table("licenses").select("*").eq("license_key", license_key).execute()
        
        if not response.data or len(response.data) == 0:
            return None
        
        return response.data[0]
    except Exception as e:
        error_msg = str(e)
        if "PGRST205" in error_msg or "schema cache" in error_msg.lower():
            # Schema cache not ready, return None
            return None
        raise


def is_license_valid(license: dict) -> tuple[bool, Optional[str]]:
    """
    Check if license is valid.
    
    Returns:
        (is_valid, reason_if_invalid)
    """
    if not license:
        return False, "License not found"
    
    if license.get("status") == "revoked":
        return False, "License has been revoked"
    
    if license.get("status") == "suspended":
        return False, "License is suspended"
    
    expires_at = license.get("expires_at")
    if expires_at:
        try:
            if isinstance(expires_at, str):
                expires = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
            else:
                expires = expires_at
            
            if expires < datetime.utcnow().replace(tzinfo=expires.tzinfo):
                return False, "License has expired"
        except (ValueError, TypeError):
            pass
    
    return True, None


def count_active_activations(supabase: Client, license_id: str) -> int:
    """Count active activations for a license."""
    try:
        response = supabase.table("activations").select(
            "id",
            count="exact"
        ).eq("license_id", license_id).eq("status", "active").execute()
        
        return response.count if hasattr(response, 'count') else len(response.data)
    except Exception as e:
        error_msg = str(e)
        if "PGRST205" in error_msg or "schema cache" in error_msg.lower():
            # Return 0 if schema cache not ready
            return 0
        raise
