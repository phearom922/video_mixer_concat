"""Release Pydantic models."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID


class ReleaseCreate(BaseModel):
    """Model for creating a release."""
    platform: str = "windows"
    version: str
    release_notes: Optional[str] = None
    download_url: str
    is_latest: bool = False


class ReleaseResponse(BaseModel):
    """Release response model."""
    id: UUID
    platform: str
    version: str
    release_notes: Optional[str]
    download_url: str
    is_latest: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class LatestReleaseResponse(BaseModel):
    """Response for latest release check."""
    update_available: bool
    latest_version: Optional[str] = None
    release_notes: Optional[str] = None
    download_url: Optional[str] = None
