# License Server (FastAPI)

License management API server for the Video Mixer desktop application.

## Features

- License activation and validation
- Device fingerprinting and activation tracking
- JWT-based activation tokens
- Rate limiting
- Admin endpoints for license and release management
- Audit logging

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `env.example` to `.env` and fill in the values:

```bash
cp env.example .env
```

Required environment variables:
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_SERVICE_ROLE_KEY`: Supabase service role key (server-only, never expose to clients)
- `JWT_SIGNING_SECRET`: Secret key for signing JWT tokens (min 32 characters)
- `ADMIN_EMAILS`: Comma-separated list of admin email addresses
- `CORS_ORIGINS`: Comma-separated list of allowed CORS origins

### 3. Run the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

For production:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Public Endpoints (Desktop App)

- `POST /api/v1/activate` - Activate a license
- `POST /api/v1/validate` - Validate an activation token
- `POST /api/v1/deactivate` - Deactivate an activation
- `GET /api/v1/releases/latest` - Get latest release information

### Admin Endpoints (Dashboard)

All admin endpoints require Supabase JWT authentication.

- `POST /admin/licenses` - Create a license
- `GET /admin/licenses` - List licenses (with search)
- `GET /admin/licenses/{id}` - Get license details
- `PUT /admin/licenses/{id}` - Update a license
- `POST /admin/licenses/{id}/revoke` - Revoke a license
- `GET /admin/licenses/{id}/activations` - Get license activations
- `POST /admin/activations/{id}/revoke` - Revoke an activation
- `POST /admin/releases` - Create a release
- `GET /admin/releases` - List releases
- `POST /admin/releases/{id}/set-latest` - Set release as latest
- `GET /admin/audit-logs` - Get audit logs

## Security

- JWT tokens are signed with a secret key
- Device fingerprints are hashed (SHA-256) before storage
- Rate limiting on activation and validation endpoints
- Admin endpoints protected by Supabase JWT verification
- CORS configured for specific origins

## Development

The server uses FastAPI with automatic API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
