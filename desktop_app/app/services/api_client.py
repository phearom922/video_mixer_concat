"""API client for communicating with license server."""
import requests
from typing import Optional, Dict, Any
from datetime import datetime
from app.services.config_service import config_service
from app.services.logging_service import logger


class APIClient:
    """Client for FastAPI license server."""
    
    def __init__(self):
        self.base_url = config_service.get_api_base_url()
    
    def _get_headers(self, token: Optional[str] = None) -> Dict[str, str]:
        """Get request headers."""
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers
    
    def activate(
        self,
        license_key: str,
        device_fingerprint: str,
        app_version: str,
        device_label: Optional[str] = None
    ) -> Dict[str, Any]:
        """Activate a license."""
        url = f"{self.base_url}/api/v1/activate"
        data = {
            "license_key": license_key,
            "device_fingerprint": device_fingerprint,
            "app_version": app_version,
            "device_label": device_label
        }
        
        try:
            response = requests.post(url, json=data, headers=self._get_headers(), timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Activation failed: {e}")
            raise
    
    def validate(self, token: str, app_version: str) -> Dict[str, Any]:
        """Validate an activation token."""
        url = f"{self.base_url}/api/v1/validate"
        data = {"app_version": app_version}
        
        try:
            response = requests.post(
                url,
                json=data,
                headers=self._get_headers(token),
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get("valid"):
                # Update last validation time
                config_service.set_last_validation_time(datetime.utcnow().isoformat())
            
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"Validation failed: {e}")
            # Return invalid on network error
            return {
                "valid": False,
                "reason": "Network error",
                "server_time": datetime.utcnow().isoformat()
            }
    
    def deactivate(self, token: str) -> Dict[str, Any]:
        """Deactivate an activation."""
        url = f"{self.base_url}/api/v1/deactivate"
        
        try:
            response = requests.post(
                url,
                headers=self._get_headers(token),
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Deactivation failed: {e}")
            raise
    
    def get_latest_release(self, platform: str = "windows", current_version: str = "0.0.0") -> Dict[str, Any]:
        """Get latest release information."""
        url = f"{self.base_url}/api/v1/releases/latest"
        params = {
            "platform": platform,
            "current_version": current_version
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to check for updates: {e}")
            return {"update_available": False}


api_client = APIClient()
