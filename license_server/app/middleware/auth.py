"""Admin authentication middleware."""
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from supabase import Client
from app.config import settings
from app.database import get_supabase_client


security = HTTPBearer()


async def verify_admin_token(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> dict:
    """
    Verify Supabase JWT token and check if user is admin.
    
    Raises HTTPException if token is invalid or user is not admin.
    """
    token = credentials.credentials
    
    try:
        # Verify token with Supabase
        supabase: Client = get_supabase_client()
        
        # Get user from token
        user_response = supabase.auth.get_user(token)
        
        if not user_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token"
            )
        
        user = user_response.user
        user_email = user.email.lower() if user.email else None
        
        # Check if user is admin
        admin_emails = settings.admin_emails_list
        if not admin_emails:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Admin emails not configured"
            )
        
        if user_email not in admin_emails:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Admin privileges required."
            )
        
        return {
            "user_id": user.id,
            "email": user_email
        }
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )
