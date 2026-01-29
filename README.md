# Video Mixer Licensing System

Complete licensing and update ecosystem for a Windows Python desktop video concatenation application.

## Architecture

```
┌─────────────────┐         ┌──────────────┐         ┌─────────────┐
│  Desktop App    │────────▶│  FastAPI     │────────▶│  Supabase   │
│  (PySide6)      │         │  License     │         │  (Postgres) │
│                 │         │  Server      │         │             │
└─────────────────┘         └──────────────┘         └─────────────┘
                                      ▲
                                      │
                            ┌─────────┴─────────┐
                            │                   │
                    ┌───────▼──────┐   ┌───────▼──────┐
                    │  Admin       │   │  Supabase    │
                    │  Dashboard   │   │  Auth        │
                    │  (Next.js)   │   │              │
                    └──────────────┘   └──────────────┘
```

## Components

1. **Supabase Database** - PostgreSQL database with RLS policies
2. **FastAPI License Server** - Backend API for license management
3. **Next.js Admin Dashboard** - Web interface for admin operations
4. **PySide6 Desktop App** - Windows desktop application for video concatenation

## Quick Start

### 1. Supabase Setup

1. Create a Supabase project
2. Run the migration:
   ```sql
   -- Copy contents from supabase/migrations/001_initial_schema.sql
   -- Run in Supabase SQL Editor
   ```
3. Note your Supabase URL and service role key

### 2. FastAPI License Server

```bash
cd license_server
pip install -r requirements.txt
cp env.example .env
# Edit .env with your Supabase credentials
uvicorn app.main:app --reload
```

Server runs on http://localhost:8000

### 3. Next.js Admin Dashboard

```bash
cd admin_dashboard
npm install
cp env.example .env.local
# Edit .env.local with your Supabase and API credentials
npm run dev
```

Dashboard runs on http://localhost:3000

### 4. Desktop App

```bash
cd desktop_app
pip install -r requirements.txt
# Configure API URL in app (default: http://localhost:8000)
python -m app.main
```

## Setup Steps

### Step 1: Supabase Database

1. Create a new Supabase project
2. Go to SQL Editor
3. Copy and run the SQL from `supabase/migrations/001_initial_schema.sql`
4. This creates:
   - `licenses` table
   - `activations` table
   - `admin_audit_logs` table
   - `app_releases` table
   - RLS policies (admin-only access)

### Step 2: FastAPI License Server

1. Navigate to `license_server/`
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `env.example` to `.env`
4. Configure:
   - `SUPABASE_URL`: Your Supabase project URL
   - `SUPABASE_SERVICE_ROLE_KEY`: Service role key (from Supabase settings)
   - `JWT_SIGNING_SECRET`: Random secret (min 32 chars)
   - `ADMIN_EMAILS`: Comma-separated admin emails
   - `CORS_ORIGINS`: Allowed origins for CORS
5. Run: `uvicorn app.main:app --reload`

### Step 3: Next.js Admin Dashboard

1. Navigate to `admin_dashboard/`
2. Install dependencies: `npm install`
3. Copy `env.example` to `.env.local`
4. Configure:
   - `NEXT_PUBLIC_SUPABASE_URL`: Your Supabase project URL
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`: Supabase anonymous key
   - `NEXT_PUBLIC_ADMIN_EMAILS`: Comma-separated admin emails
   - `NEXT_PUBLIC_API_BASE_URL`: FastAPI server URL (default: http://localhost:8000)
5. Run: `npm run dev`

### Step 4: Desktop App

1. Navigate to `desktop_app/`
2. Install dependencies: `pip install -r requirements.txt`
3. Install FFmpeg (see desktop_app/README.md)
4. Run: `python -m app.main`
5. On first launch, activate with a license key

## Creating Your First License

1. Log in to the admin dashboard (http://localhost:3000)
2. Go to Licenses page
3. Click "Create License"
4. Fill in:
   - Customer Name (optional)
   - Max Activations (default: 1)
   - Status (default: active)
   - Expires At (optional)
   - Notes (optional)
5. Click "Save"
6. Copy the generated license key
7. Use this key to activate the desktop app

## Creating a Release

1. Log in to the admin dashboard
2. Go to Releases page
3. Click "Create Release"
4. Fill in:
   - Platform: windows
   - Version: e.g., 1.0.0 (semver format)
   - Release Notes: What's new
   - Download URL: URL to download the new version
   - Check "Set as latest" if this should be the latest version
5. Click "Save"
6. Desktop apps will be notified of the update

## Security Notes

- **Never expose** `SUPABASE_SERVICE_ROLE_KEY` to clients
- Use strong `JWT_SIGNING_SECRET` (min 32 characters)
- Configure CORS origins properly in production
- Admin emails are checked both client-side and server-side
- Device fingerprints are hashed before storage

## Development

### FastAPI API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Building Desktop App

```bash
cd desktop_app
pip install pyinstaller
pyinstaller pyinstaller.spec
```

Executable will be in `dist/VideoMixerConcat.exe`

## 📚 Documentation

- **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)** - คู่มือการ deploy License Server
- **[DISTRIBUTION_GUIDE.md](./DISTRIBUTION_GUIDE.md)** - คู่มือการส่งไฟล์ Desktop App ให้ลูกค้า
- **[UPDATE_VERSION_GUIDE.md](./UPDATE_VERSION_GUIDE.md)** - คู่มือการอัพเดทเวอร์ชั่น
- **[VERCEL_RAILWAY_DEPLOYMENT.md](./VERCEL_RAILWAY_DEPLOYMENT.md)** - Deploy ด้วย Vercel + Railway (แนะนำ)
- **[VERCEL_RENDER_DEPLOYMENT.md](./VERCEL_RENDER_DEPLOYMENT.md)** - Deploy ด้วย Vercel + Render
- **[PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)** - โครงสร้างโปรเจกต์
- **[ROOT_DIRECTORY_SETUP.md](./ROOT_DIRECTORY_SETUP.md)** - ⚠️ การตั้งค่า Root Directory (สำคัญ!)
- **[VPS_DEPLOYMENT_GUIDE.md](./VPS_DEPLOYMENT_GUIDE.md)** - Deploy บน VPS (1 Core, 2GB RAM พอใช้งานได้)
- **[DOCKER_DEPLOYMENT_GUIDE.md](./DOCKER_DEPLOYMENT_GUIDE.md)** - Deploy ด้วย Docker (แนะนำถ้ามี services อื่นรันอยู่แล้ว)
- **[RAILWAY_PRICING_GUIDE.md](./RAILWAY_PRICING_GUIDE.md)** - Railway pricing และ trial
- **[SETUP_GUIDE.md](./SETUP_GUIDE.md)** - คู่มือการตั้งค่า local development
- **[QUICK_SETUP.md](./QUICK_SETUP.md)** - Quick start guide

## Project Structure

```
.
├── supabase/
│   └── migrations/
│       └── 001_initial_schema.sql
├── license_server/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── routers/
│   │   ├── services/
│   │   └── models/
│   ├── requirements.txt
│   └── README.md
├── admin_dashboard/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── package.json
│   └── README.md
└── desktop_app/
    ├── app/
    │   ├── main.py
    │   ├── ui/
    │   ├── services/
    │   ├── core/
    │   └── utils/
    ├── requirements.txt
    └── README.md
```

## License

This is a complete licensing system implementation. All components are provided as-is for your use.
