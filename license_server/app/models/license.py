"""License Pydantic models."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID


class LicenseBase(BaseModel):
    """Base license model."""
    customer_name: Optional[str] = None
    max_activations: int = Field(default=1, ge=1)
    status: str = Field(default="active", pattern="^(active|revoked|suspended)$")
    expires_at: Optional[datetime] = None
    notes: Optional[str] = None


class LicenseCreate(LicenseBase):
    """Model for creating a license."""
    pass


class LicenseResponse(LicenseBase):
    """License response model."""
    id: UUID
    license_key: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class LicenseUpdate(BaseModel):
    """Model for updating a license."""
    customer_name: Optional[str] = None
    max_activations: Optional[int] = Field(None, ge=1)
    status: Optional[str] = Field(None, pattern="^(active|revoked|suspended)$")
    expires_at: Optional[datetime] = None
    notes: Optional[str] = None
