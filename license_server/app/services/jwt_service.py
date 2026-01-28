"""JWT token service for activation tokens."""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import jwt, JWTError
from app.config import settings


def create_activation_token(
    license_id: str,
    activation_id: str,
    device_id_hash: str,
    expires_hours: Optional[int] = None
) -> str:
    """Create a JWT activation token."""
    if expires_hours is None:
        expires_hours = settings.JWT_EXPIRATION_HOURS
    
    expire = datetime.utcnow() + timedelta(hours=expires_hours)
    
    payload = {
        "license_id": license_id,
        "activation_id": activation_id,
        "device_id_hash": device_id_hash,
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "activation"
    }
    
    return jwt.encode(
        payload,
        settings.JWT_SIGNING_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )


def verify_activation_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify and decode an activation token."""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SIGNING_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        # Verify token type
        if payload.get("type") != "activation":
            return None
        
        return payload
    except JWTError:
        return None


def get_token_expiry(token: str) -> Optional[datetime]:
    """Get expiry time from token."""
    payload = verify_activation_token(token)
    if payload and "exp" in payload:
        return datetime.utcfromtimestamp(payload["exp"])
    return None
