# Quick Start Guide - License Server

## ✅ Server is Running!

FastAPI License Server is now running at:
- **URL**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## How to Run

### Option 1: Using Python Module (Recommended)
```bash
cd license_server
python -m uvicorn app.main:app --reload
```

### Option 2: Using Script (Windows)
```bash
cd license_server
run_server.bat
```

### Option 3: Using Script (Linux/Mac)
```bash
cd license_server
chmod +x run_server.sh
./run_server.sh
```

## API Endpoints

### Public Endpoints (Desktop App)
- `POST /api/v1/activate` - Activate license
- `POST /api/v1/validate` - Validate activation token
- `POST /api/v1/deactivate` - Deactivate activation
- `GET /api/v1/releases/latest` - Get latest release info

### Admin Endpoints (Dashboard)
- `POST /admin/licenses` - Create license
- `GET /admin/licenses` - List licenses
- `GET /admin/licenses/{id}` - Get license details
- `POST /admin/licenses/{id}/revoke` - Revoke license
- `GET /admin/licenses/{id}/activations` - Get activations
- `POST /admin/activations/{id}/revoke` - Revoke activation
- `POST /admin/releases` - Create release
- `GET /admin/releases` - List releases
- `POST /admin/releases/{id}/set-latest` - Set latest release

## Testing

1. **Health Check:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **API Documentation:**
   Open http://localhost:8000/docs in your browser

3. **Test Activation:**
   Use the Swagger UI at http://localhost:8000/docs to test endpoints

## Troubleshooting

### uvicorn: command not found
Use `python -m uvicorn` instead of `uvicorn` directly.

### Port already in use
Change the port:
```bash
python -m uvicorn app.main:app --reload --port 8001
```

### Database connection errors
Check your `.env` file and ensure:
- `SUPABASE_URL` is correct
- `SUPABASE_SERVICE_ROLE_KEY` is valid
