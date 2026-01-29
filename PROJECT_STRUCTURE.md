# โครงสร้างโปรเจกต์ (Project Structure)

เอกสารนี้อธิบายโครงสร้างของโปรเจกต์ FlowMix สำหรับการ deploy และ development

## โครงสร้างหลัก

```
FlowMix/
├── admin_dashboard/          # Next.js Admin Dashboard
├── desktop_app/              # PySide6 Desktop Application
├── license_server/           # FastAPI License Server
├── supabase/                 # Database migrations
└── docs/                     # Documentation files
```

---

## 1. Admin Dashboard (`admin_dashboard/`)

**Technology**: Next.js 14, React, TypeScript, Tailwind CSS

### โครงสร้าง:

```
admin_dashboard/
├── app/                      # Next.js App Router
│   ├── globals.css
│   ├── layout.tsx
│   ├── page.tsx              # Dashboard home
│   ├── login/
│   │   └── page.tsx          # Admin login
│   ├── licenses/
│   │   ├── page.tsx          # License list
│   │   └── [id]/
│   │       └── page.tsx      # License detail
│   └── releases/
│       └── page.tsx          # Release management
├── components/               # React components
│   ├── DashboardLayout.tsx
│   ├── Sidebar.tsx
│   ├── LicenseList.tsx
│   ├── LicenseForm.tsx
│   └── ...
├── lib/                      # Utilities
│   ├── api.ts                # API client
│   ├── auth.ts               # Authentication
│   └── supabase.ts           # Supabase client
├── env.example               # Environment variables template
├── package.json
├── tsconfig.json
└── README.md
```

### Environment Variables (`.env.local`):

```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_ADMIN_EMAILS=admin@example.com
NEXT_PUBLIC_API_BASE_URL=https://your-license-server.com
```

### Deploy:

- **Platform**: Vercel (แนะนำ)
- **Build Command**: `npm run build`
- **Output Directory**: `.next`

---

## 2. Desktop App (`desktop_app/`)

**Technology**: Python 3.11+, PySide6, FFmpeg

### โครงสร้าง:

```
desktop_app/
├── app/
│   ├── main.py               # Entry point
│   ├── core/                 # Core logic
│   │   ├── grouper.py        # Video grouping
│   │   ├── worker.py         # Processing worker
│   │   └── ffmpeg_concat.py  # FFmpeg operations
│   ├── services/             # Services
│   │   ├── api_client.py     # License server API
│   │   ├── config_service.py # Configuration
│   │   ├── license_guard.py   # License validation
│   │   └── update_service.py # Update checking
│   ├── ui/                   # UI components
│   │   ├── main_window.py    # Main window
│   │   ├── activation_window.py
│   │   ├── update_dialog.py
│   │   ├── assets/           # Icons and logos
│   │   └── ...
│   ├── utils/                # Utilities
│   │   ├── ffmpeg_helper.py  # FFmpeg path detection
│   │   ├── paths.py          # Path management
│   │   └── semver.py         # Version comparison
│   └── ffmpeg/               # FFmpeg binaries (optional, for bundling)
│       └── bin/
│           ├── ffmpeg.exe
│           ├── ffplay.exe
│           └── ffprobe.exe
├── build/                    # Build artifacts (ignored)
├── dist/                     # Output executable (ignored)
├── pyinstaller.spec          # PyInstaller config
├── requirements.txt
└── README.md
```

### Build:

```bash
cd desktop_app
pip install -r requirements.txt
python -m PyInstaller pyinstaller.spec
# Output: dist/VideoMixerConcat.exe
```

### Configuration:

- Config file: `%APPDATA%\VideoMixerConcat\config.json`
- Logs: `%APPDATA%\VideoMixerConcat\logs\`

---

## 3. License Server (`license_server/`)

**Technology**: FastAPI, Python 3.11+, Supabase

### โครงสร้าง:

```
license_server/
├── app/
│   ├── main.py               # FastAPI app
│   ├── config.py             # Configuration
│   ├── database.py            # Supabase client
│   ├── middleware/           # Middleware
│   │   └── auth.py            # Authentication
│   ├── models/               # Pydantic models
│   │   ├── license.py
│   │   ├── activation.py
│   │   └── release.py
│   ├── routers/              # API routes
│   │   ├── public.py         # Public endpoints
│   │   └── admin.py          # Admin endpoints
│   └── services/             # Business logic
│       ├── license_service.py
│       ├── activation_service.py
│       ├── jwt_service.py
│       └── ...
├── env.example               # Environment variables template
├── requirements.txt
├── run_server.sh             # Start script (Linux/Mac)
├── run_server.bat            # Start script (Windows)
└── README.md
```

### Environment Variables (`.env`):

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
JWT_SIGNING_SECRET=your-secret-key-min-32-chars
ADMIN_EMAILS=admin@example.com
CORS_ORIGINS=https://your-admin-dashboard.vercel.app
```

### Deploy:

- **Platform**: Railway (แนะนำ), Render, Fly.io, หรือ VPS
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Port**: ใช้ `$PORT` environment variable

---

## 4. Supabase (`supabase/`)

### โครงสร้าง:

```
supabase/
└── migrations/
    └── 001_initial_schema.sql  # Database schema
```

### Tables:

- `licenses` - License keys
- `activations` - Device activations
- `app_releases` - Application releases
- `admin_audit_logs` - Admin action logs

---

## 5. Documentation

### Essential Documentation:

- `README.md` - Project overview
- `DEPLOYMENT_GUIDE.md` - How to deploy License Server
- `DISTRIBUTION_GUIDE.md` - How to distribute Desktop App
- `UPDATE_VERSION_GUIDE.md` - How to create new releases
- `VERCEL_RAILWAY_DEPLOYMENT.md` - Vercel + Railway deployment
- `VERCEL_RENDER_DEPLOYMENT.md` - Vercel + Render deployment
- `SETUP_GUIDE.md` - Local development setup
- `QUICK_SETUP.md` - Quick start guide

### Per-Module Documentation:

- `admin_dashboard/README.md`
- `desktop_app/README.md`
- `license_server/README.md`

---

## Environment Variables Summary

### Admin Dashboard (Vercel):

```env
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
NEXT_PUBLIC_ADMIN_EMAILS=
NEXT_PUBLIC_API_BASE_URL=
```

### License Server (Railway/Render):

```env
SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=
JWT_SIGNING_SECRET=
ADMIN_EMAILS=
CORS_ORIGINS=
```

### Desktop App:

- Config file: `%APPDATA%\VideoMixerConcat\config.json`
- API URL: Hardcoded หรือ config file

---

## Deployment Checklist

### Before Deploying:

- [ ] Supabase database setup และ migrations run แล้ว
- [ ] Environment variables ตั้งค่าครบถ้วน
- [ ] CORS origins ตั้งค่าถูกต้อง
- [ ] API URLs ตั้งค่าถูกต้อง
- [ ] ทดสอบ local development แล้ว

### Deploy Order:

1. **Supabase** - Setup database และ migrations
2. **License Server** - Deploy บน Railway/Render
3. **Admin Dashboard** - Deploy บน Vercel
4. **Desktop App** - Build executable และ distribute

---

## File Ignore Rules

### Files/Folders ที่ไม่ควร commit:

- `__pycache__/` - Python cache
- `node_modules/` - Node.js dependencies
- `.env`, `.env.local` - Environment variables
- `build/`, `dist/` - Build artifacts
- `*.exe` - Executable files
- `desktop_app/app/ffmpeg/` - FFmpeg binaries (ใหญ่)
- Temporary markdown files (FIX_*, CRITICAL_*, etc.)

### Files ที่ควร commit:

- `env.example` - Environment variable templates
- `requirements.txt` - Python dependencies
- `package.json` - Node.js dependencies
- `pyinstaller.spec` - Build configuration
- Source code files
- Documentation files

---

## Quick Start

### Local Development:

1. **Setup Supabase**: Run migration
2. **License Server**: `cd license_server && uvicorn app.main:app --reload`
3. **Admin Dashboard**: `cd admin_dashboard && npm run dev`
4. **Desktop App**: `cd desktop_app && python -m app.main`

### Production Deployment:

1. **License Server**: Deploy บน Railway/Render
2. **Admin Dashboard**: Deploy บน Vercel
3. **Desktop App**: Build executable และ distribute

ดูรายละเอียดเพิ่มเติมใน:
- `DEPLOYMENT_GUIDE.md` - สำหรับ License Server
- `VERCEL_RAILWAY_DEPLOYMENT.md` - สำหรับ Vercel + Railway
- `DISTRIBUTION_GUIDE.md` - สำหรับ Desktop App distribution
