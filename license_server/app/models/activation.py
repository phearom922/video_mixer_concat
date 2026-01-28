"""Activation Pydantic models."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID


class ActivationRequest(BaseModel):
    """Request model for license activation."""
    license_key: str
    device_fingerprint: str
    app_version: str
    device_label: Optional[str] = None


class ActivationResponse(BaseModel):
    """Response model for activation."""
    activation_token: str
    license: dict
    activation: dict
    grace_days: int


class ValidateRequest(BaseModel):
    """Request model for license validation."""
    app_version: str


class ValidateResponse(BaseModel):
    """Response model for validation."""
    valid: bool
    reason: Optional[str] = None
    expires_at: Optional[datetime] = None
    status: Optional[str] = None
    server_time: datetime = Field(default_factory=datetime.utcnow)


class ActivationInfo(BaseModel):
    """Activation information model."""
    id: UUID
    license_id: UUID
    device_id_hash: str
    device_label: Optional[str]
    first_activated_at: datetime
    last_seen_at: datetime
    status: str
    activated_app_version: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
