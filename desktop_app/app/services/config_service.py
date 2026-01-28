"""Configuration service for storing app settings."""
import json
from pathlib import Path
from typing import Optional, Dict, Any
from app.utils.paths import get_config_file, ensure_directories


class ConfigService:
    """Service for managing application configuration."""
    
    def __init__(self):
        ensure_directories()
        self._config_file = get_config_file()
        self._config: Dict[str, Any] = {}
        self.load()
    
    def load(self):
        """Load configuration from file."""
        if self._config_file.exists():
            try:
                with open(self._config_file, 'r', encoding='utf-8') as f:
                    self._config = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._config = {}
        else:
            self._config = {}
    
    def save(self):
        """Save configuration to file."""
        ensure_directories()
        try:
            with open(self._config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2)
        except IOError:
            pass
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set a configuration value."""
        self._config[key] = value
        self.save()
    
    def get_activation_token(self) -> Optional[str]:
        """Get stored activation token."""
        return self.get("activation_token")
    
    def set_activation_token(self, token: str):
        """Set activation token."""
        self.set("activation_token", token)
    
    def get_api_base_url(self) -> str:
        """Get API base URL."""
        return self.get("api_base_url", "http://localhost:8000")
    
    def set_api_base_url(self, url: str):
        """Set API base URL."""
        self.set("api_base_url", url)
    
    def get_ffmpeg_path(self) -> Optional[str]:
        """Get FFmpeg executable path."""
        return self.get("ffmpeg_path")
    
    def set_ffmpeg_path(self, path: str):
        """Set FFmpeg executable path."""
        self.set("ffmpeg_path", path)
    
    def get_last_validation_time(self) -> Optional[str]:
        """Get last successful validation timestamp."""
        return self.get("last_validation_time")
    
    def set_last_validation_time(self, timestamp: str):
        """Set last successful validation timestamp."""
        self.set("last_validation_time", timestamp)
    
    def get_skipped_versions(self) -> list:
        """Get list of skipped update versions."""
        return self.get("skipped_versions", [])
    
    def add_skipped_version(self, version: str):
        """Add a version to skipped list."""
        skipped = self.get_skipped_versions()
        if version not in skipped:
            skipped.append(version)
            self.set("skipped_versions", skipped)
    
    def is_version_skipped(self, version: str) -> bool:
        """Check if a version is skipped."""
        return version in self.get_skipped_versions()
    
    def get_license_expires_at(self) -> Optional[str]:
        """Get license expiration date."""
        return self.get("license_expires_at")
    
    def set_license_expires_at(self, expires_at: str):
        """Set license expiration date."""
        self.set("license_expires_at", expires_at)


# Global instance
config_service = ConfigService()
