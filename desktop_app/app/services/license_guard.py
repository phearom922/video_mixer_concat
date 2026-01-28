"""License guard service for grace period and validation."""
from datetime import datetime, timedelta
from typing import Optional, Tuple
from app.services.config_service import config_service
from app.services.api_client import api_client
from app.services.logging_service import logger
from app import APP_VERSION


class LicenseGuard:
    """Service for managing license validation and grace period."""
    
    GRACE_DAYS = 7
    
    def __init__(self):
        self._last_validation_result: Optional[dict] = None
    
    def is_license_valid(self) -> Tuple[bool, Optional[str]]:
        """
        Check if license is valid.
        
        Returns:
            (is_valid, reason_if_invalid)
        """
        token = config_service.get_activation_token()
        if not token:
            return False, "No activation token found. Please activate your license."
        
        # Try to validate with server
        try:
            result = api_client.validate(token, APP_VERSION)
            self._last_validation_result = result
            
            if result.get("valid"):
                return True, None
            else:
                return False, result.get("reason", "License validation failed")
        except Exception as e:
            logger.error(f"Validation error: {e}")
            # Check grace period
            return self._check_grace_period()
    
    def _check_grace_period(self) -> Tuple[bool, Optional[str]]:
        """Check if we're within grace period."""
        last_validation = config_service.get_last_validation_time()
        if not last_validation:
            return False, "No previous validation found. Internet connection required."
        
        try:
            last_time = datetime.fromisoformat(last_validation)
            grace_end = last_time + timedelta(days=self.GRACE_DAYS)
            
            if datetime.utcnow() < grace_end:
                days_remaining = (grace_end - datetime.utcnow()).days
                return True, f"Offline mode (grace period: {days_remaining} days remaining)"
            else:
                return False, f"Grace period expired. Internet connection required for validation."
        except (ValueError, TypeError):
            return False, "Invalid validation timestamp. Internet connection required."
    
    def get_validation_info(self) -> dict:
        """Get current validation information."""
        is_valid, reason = self.is_license_valid()
        return {
            "valid": is_valid,
            "reason": reason,
            "last_validation": self._last_validation_result
        }


license_guard = LicenseGuard()
