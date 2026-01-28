"""Activation service for managing device activations."""
from datetime import datetime
from typing import Optional
from uuid import UUID
from supabase import Client


def get_activation_by_device_hash(
    supabase: Client,
    license_id: str,
    device_id_hash: str
) -> Optional[dict]:
    """Get activation by license ID and device hash."""
    try:
        response = supabase.table("activations").select("*").eq(
            "license_id", license_id
        ).eq("device_id_hash", device_id_hash).execute()
        
        if not response.data or len(response.data) == 0:
            return None
        
        return response.data[0]
    except Exception as e:
        error_msg = str(e)
        if "PGRST205" in error_msg or "schema cache" in error_msg.lower():
            # Schema cache not ready, return None
            return None
        raise


def create_activation(
    supabase: Client,
    license_id: str,
    device_id_hash: str,
    device_label: Optional[str],
    app_version: str
) -> dict:
    """Create a new activation."""
    data = {
        "license_id": license_id,
        "device_id_hash": device_id_hash,
        "device_label": device_label,
        "status": "active",
        "activated_app_version": app_version,
        "first_activated_at": datetime.utcnow().isoformat(),
        "last_seen_at": datetime.utcnow().isoformat()
    }
    
    try:
        response = supabase.table("activations").insert(data).execute()
        return response.data[0] if response.data else {}
    except Exception as e:
        error_msg = str(e)
        if "PGRST205" in error_msg or "schema cache" in error_msg.lower():
            raise Exception("Database schema cache is being refreshed. Please try again in a moment.")
        raise


def update_activation_last_seen(
    supabase: Client,
    activation_id: str
) -> dict:
    """Update activation last_seen_at timestamp."""
    data = {
        "last_seen_at": datetime.utcnow().isoformat()
    }
    
    try:
        response = supabase.table("activations").update(data).eq(
            "id", activation_id
        ).execute()
        return response.data[0] if response.data else {}
    except Exception as e:
        error_msg = str(e)
        if "PGRST205" in error_msg or "schema cache" in error_msg.lower():
            # Silently fail - this is not critical
            return {}
        raise


def revoke_activation(supabase: Client, activation_id: str) -> dict:
    """Revoke an activation."""
    data = {
        "status": "revoked"
    }
    
    try:
        response = supabase.table("activations").update(data).eq(
            "id", activation_id
        ).execute()
        return response.data[0] if response.data else {}
    except Exception as e:
        error_msg = str(e)
        if "PGRST205" in error_msg or "schema cache" in error_msg.lower():
            raise Exception("Database schema cache is being refreshed. Please try again in a moment.")
        raise
