"""Update service for checking and managing app updates."""
from datetime import datetime, timedelta
from typing import Optional
from app.services.config_service import config_service
from app.services.api_client import api_client
from app.services.logging_service import logger
from app.utils.semver import is_newer_version
from app import APP_VERSION


class UpdateService:
    """Service for checking app updates."""
    
    CHECK_INTERVAL_HOURS = 12
    
    def __init__(self):
        self._last_check_time: Optional[datetime] = None
        self._last_check_result: Optional[dict] = None
    
    def should_check(self) -> bool:
        """Check if enough time has passed since last check."""
        last_check_str = config_service.get("last_update_check")
        if not last_check_str:
            return True
        
        try:
            last_check = datetime.fromisoformat(last_check_str)
            next_check = last_check + timedelta(hours=self.CHECK_INTERVAL_HOURS)
            return datetime.utcnow() >= next_check
        except (ValueError, TypeError):
            return True
    
    def check_for_updates(self, force: bool = False) -> Optional[dict]:
        """
        Check for available updates.
        
        Returns:
            Update info dict if update available, None otherwise
        """
        if not force and not self.should_check():
            return self._last_check_result
        
        try:
            result = api_client.get_latest_release("windows", APP_VERSION)
            self._last_check_result = result
            
            # Update last check time
            config_service.set("last_update_check", datetime.utcnow().isoformat())
            
            if result.get("update_available"):
                latest_version = result.get("latest_version")
                
                # Check if this version was skipped
                if latest_version and config_service.is_version_skipped(latest_version):
                    logger.info(f"Update {latest_version} was skipped by user")
                    return None
                
                return result
            
            return None
        except Exception as e:
            logger.error(f"Update check failed: {e}")
            return None
    
    def skip_version(self, version: str):
        """Mark a version as skipped."""
        config_service.add_skipped_version(version)


update_service = UpdateService()
