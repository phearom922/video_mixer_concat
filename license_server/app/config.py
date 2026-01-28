"""Configuration settings from environment variables."""
import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Supabase
    SUPABASE_URL: str
    SUPABASE_SERVICE_ROLE_KEY: str
    
    # JWT
    JWT_SIGNING_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24 * 365  # 1 year default
    
    # Device Hashing
    DEVICE_HASH_SALT: str = ""  # Optional salt for device fingerprint hashing
    
    # Admin
    ADMIN_EMAILS: str = ""  # Comma-separated list of admin emails
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001"
    
    # Rate Limiting
    RATE_LIMIT_ACTIVATE_PER_MINUTE: int = 5
    RATE_LIMIT_VALIDATE_PER_MINUTE: int = 60
    
    # Grace Period
    GRACE_DAYS: int = 7
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    @property
    def admin_emails_list(self) -> List[str]:
        """Get admin emails as a list."""
        if not self.ADMIN_EMAILS:
            return []
        return [email.strip().lower() for email in self.ADMIN_EMAILS.split(",") if email.strip()]
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


settings = Settings()
