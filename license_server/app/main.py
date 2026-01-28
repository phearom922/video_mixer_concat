"""FastAPI application entry point."""
from fastapi import FastAPI, Request, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request as StarletteRequest
from app.config import settings
from app.routers import public, admin

app = FastAPI(
    title="Video Mixer License Server",
    description="License management API for Video Mixer desktop application",
    version="1.0.0"
)

# Error handler middleware - catches all unhandled exceptions BEFORE they reach exception handlers
# This MUST be added LAST so it executes FIRST (FastAPI reverses middleware order)
class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware to catch all unhandled exceptions and add CORS headers."""
    async def dispatch(self, request: StarletteRequest, call_next):
        try:
            response = await call_next(request)
            # Ensure CORS headers are present even on successful responses
            origin = request.headers.get("origin")
            allowed_origins = settings.cors_origins_list
            if origin and origin in allowed_origins:
                if not response.headers.get("Access-Control-Allow-Origin"):
                    response.headers["Access-Control-Allow-Origin"] = origin
                    response.headers["Access-Control-Allow-Credentials"] = "true"
            return response
        except Exception as exc:
            # Catch ALL exceptions (including HTTPException) and add CORS headers
            # This ensures CORS headers are ALWAYS present, even for unhandled errors
            origin = request.headers.get("origin")
            allowed_origins = settings.cors_origins_list
            cors_origin = origin if origin in allowed_origins else (allowed_origins[0] if allowed_origins else "*")
            
            # Log error for debugging (but don't expose to client)
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Unhandled exception in ErrorHandlerMiddleware: {type(exc).__name__}: {str(exc)}")
            
            # Return JSON response with CORS headers
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"},
                headers={
                    "Access-Control-Allow-Origin": cors_origin,
                    "Access-Control-Allow-Credentials": "true",
                    "Access-Control-Allow-Methods": "*",
                    "Access-Control-Allow-Headers": "*",
                }
            )

# IMPORTANT: In FastAPI, middleware execution order is REVERSED
# Last added = First executed
# We want ErrorHandlerMiddleware to execute FIRST to catch all exceptions
# 
# CRITICAL: Based on testing, when CORSMiddleware is added, it seems to be
# placed at the end of the middleware stack, so we need to add ErrorHandlerMiddleware
# FIRST in code to ensure it executes FIRST (as the last added middleware)

# Add error handler middleware FIRST in code (will be added to stack first, but executes LAST)
# Wait, that's wrong. Let me test the actual behavior.
# Actually, based on the test results, CORSMiddleware always ends up at index 1
# when added after another middleware. So we need to add ErrorHandlerMiddleware FIRST.

# Add error handler middleware FIRST in code
# This ensures it's at the beginning of the middleware stack
app.add_middleware(ErrorHandlerMiddleware)

# Add CORS middleware SECOND in code
# This will be added after ErrorHandlerMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Exception handlers to ensure CORS headers are always present
# Register for both FastAPI and Starlette HTTPException to ensure coverage
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """HTTPException handler with CORS headers."""
    origin = request.headers.get("origin")
    # Only allow configured origins
    allowed_origins = settings.cors_origins_list
    cors_origin = origin if origin in allowed_origins else allowed_origins[0] if allowed_origins else "*"
    
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers={
            "Access-Control-Allow-Origin": cors_origin,
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        }
    )

@app.exception_handler(StarletteHTTPException)
async def starlette_http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Starlette HTTPException handler with CORS headers."""
    origin = request.headers.get("origin")
    # Only allow configured origins
    allowed_origins = settings.cors_origins_list
    cors_origin = origin if origin in allowed_origins else allowed_origins[0] if allowed_origins else "*"
    
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers={
            "Access-Control-Allow-Origin": cors_origin,
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler to ensure CORS headers are always present."""
    from fastapi import HTTPException
    
    # If it's already an HTTPException, it should be handled by http_exception_handler
    # But just in case, handle it here too
    if isinstance(exc, HTTPException):
        origin = request.headers.get("origin")
        allowed_origins = settings.cors_origins_list
        cors_origin = origin if origin in allowed_origins else allowed_origins[0] if allowed_origins else "*"
        
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers={
                "Access-Control-Allow-Origin": cors_origin,
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Headers": "*",
            }
        )
    
    # For unexpected errors, return 500 with CORS headers
    origin = request.headers.get("origin")
    allowed_origins = settings.cors_origins_list
    cors_origin = origin if origin in allowed_origins else allowed_origins[0] if allowed_origins else "*"
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
        headers={
            "Access-Control-Allow-Origin": cors_origin,
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        }
    )

# Include routers
app.include_router(public.router, prefix="/api/v1", tags=["public"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Video Mixer License Server", "version": "1.0.0"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}
