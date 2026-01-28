"""Device fingerprint hashing service."""
import hashlib
from app.config import settings


def hash_device_fingerprint(device_fingerprint: str) -> str:
    """Hash device fingerprint with optional salt."""
    # Combine fingerprint with salt if provided
    data = device_fingerprint
    if settings.DEVICE_HASH_SALT:
        data = f"{device_fingerprint}:{settings.DEVICE_HASH_SALT}"
    
    # SHA-256 hash
    return hashlib.sha256(data.encode('utf-8')).hexdigest()
