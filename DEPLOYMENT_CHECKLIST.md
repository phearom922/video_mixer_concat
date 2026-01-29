# Deployment Checklist

Checklist สำหรับการ deploy โปรเจกต์ FlowMix ขึ้น GitHub และ production

---

## ✅ Pre-Deployment Checklist

### 1. Code Quality

- [ ] ลบไฟล์ temporary/debug files แล้ว
- [ ] `.gitignore` ตั้งค่าครบถ้วนแล้ว
- [ ] ไม่มี sensitive data (API keys, passwords) ใน code
- [ ] Environment variables ใช้ `.env` หรือ environment variables

### 2. Documentation

- [ ] `README.md` อัพเดทแล้ว
- [ ] `PROJECT_STRUCTURE.md` สร้างแล้ว
- [ ] `DEPLOYMENT_GUIDE.md` ครบถ้วน
- [ ] `DISTRIBUTION_GUIDE.md` ครบถ้วน
- [ ] `UPDATE_VERSION_GUIDE.md` ครบถ้วน
- [ ] `VERCEL_RAILWAY_DEPLOYMENT.md` ครบถ้วน (ถ้าใช้ Railway)
- [ ] `VERCEL_RENDER_DEPLOYMENT.md` ครบถ้วน (ถ้าใช้ Render)

### 3. Configuration Files

#### Admin Dashboard:
- [ ] `env.example` มีอยู่และครบถ้วน
- [ ] `package.json` มี dependencies ครบถ้วน
- [ ] `tsconfig.json` ตั้งค่าถูกต้อง
- [ ] `next.config.js` ตั้งค่าถูกต้อง

#### License Server:
- [ ] `env.example` มีอยู่และครบถ้วน
- [ ] `requirements.txt` มี dependencies ครบถ้วน
- [ ] Start command ใช้ `$PORT` สำหรับ Railway/Render

#### Desktop App:
- [ ] `requirements.txt` มี dependencies ครบถ้วน
- [ ] `pyinstaller.spec` ตั้งค่าถูกต้อง
- [ ] API URL ตั้งค่าแล้ว (hardcode หรือ config)

### 4. Database

- [ ] Supabase project สร้างแล้ว
- [ ] Migration (`001_initial_schema.sql`) run แล้ว
- [ ] Tables ถูกสร้างแล้ว:
  - [ ] `licenses`
  - [ ] `activations`
  - [ ] `app_releases`
  - [ ] `admin_audit_logs`
- [ ] RLS policies ตั้งค่าแล้ว

### 5. Git Repository

- [ ] `.gitignore` ครบถ้วน
- [ ] `.gitattributes` สร้างแล้ว (optional แต่แนะนำ)
- [ ] ไม่มีไฟล์ sensitive ใน git history
- [ ] Branch structure ชัดเจน (main/master, develop, etc.)

---

## 🚀 Deployment Steps

### Step 1: Push to GitHub

```bash
# Initialize git (ถ้ายังไม่มี)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: FlowMix licensing system"

# Add remote
git remote add origin https://github.com/your-username/FlowMix.git

# Push
git push -u origin main
```

### Step 2: Deploy License Server (Railway/Render)

1. **Railway:**
   - [ ] สร้าง project บน Railway
   - [ ] Connect GitHub repository
   - [ ] ⚠️ **สำคัญ**: ตั้งค่า Root Directory: `license_server`
     - ไปที่ **"Settings"** → **"Source"**
     - คลิก **"Add Root Directory"** หรือ **"Edit"**
     - ใส่: `license_server`
   - [ ] ตั้งค่า Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - [ ] ตั้งค่า Environment Variables:
     - [ ] `SUPABASE_URL`
     - [ ] `SUPABASE_SERVICE_ROLE_KEY`
     - [ ] `JWT_SIGNING_SECRET`
     - [ ] `ADMIN_EMAILS`
     - [ ] `CORS_ORIGINS` (เพิ่ม Vercel URL หลังจาก deploy Admin Dashboard)
   - [ ] Deploy และเก็บ URL

2. **Render:**
   - [ ] สร้าง Web Service บน Render
   - [ ] Connect GitHub repository
   - [ ] ตั้งค่า Root Directory: `license_server`
   - [ ] ตั้งค่า Build Command: `pip install -r requirements.txt`
   - [ ] ตั้งค่า Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - [ ] ตั้งค่า Environment Variables (เหมือน Railway)
   - [ ] Deploy และเก็บ URL

### Step 3: Deploy Admin Dashboard (Vercel)

- [ ] สร้าง project บน Vercel
- [ ] Connect GitHub repository
- [ ] ⚠️ **สำคัญ**: ตั้งค่า Root Directory: `admin_dashboard`
  - ไปที่ **"Settings"** → **"General"**
  - ในส่วน **"Root Directory"** ใส่: `admin_dashboard`
- [ ] ตั้งค่า Environment Variables:
  - [ ] `NEXT_PUBLIC_SUPABASE_URL`
  - [ ] `NEXT_PUBLIC_SUPABASE_ANON_KEY`
  - [ ] `NEXT_PUBLIC_ADMIN_EMAILS`
  - [ ] `NEXT_PUBLIC_API_BASE_URL` (License Server URL)
- [ ] Deploy และเก็บ URL

### Step 4: Update CORS in License Server

- [ ] ไปที่ License Server (Railway/Render)
- [ ] อัพเดท `CORS_ORIGINS` ให้รวม Vercel URL
- [ ] Redeploy License Server

### Step 5: Test Deployment

- [ ] ทดสอบ Admin Dashboard login
- [ ] ทดสอบสร้าง License
- [ ] ทดสอบ Desktop App activation
- [ ] ทดสอบ License validation
- [ ] ทดสอบ Update check

---

## 📦 Desktop App Distribution

### Build Executable

- [ ] อัพเดท `APP_VERSION` ในโค้ด
- [ ] Bundle FFmpeg (optional แต่แนะนำ)
- [ ] Build executable: `python -m PyInstaller pyinstaller.spec`
- [ ] ทดสอบ executable
- [ ] อัพโหลดไปยัง hosting (Google Drive, Dropbox, S3, etc.)

### Create Release

- [ ] Login Admin Dashboard
- [ ] ไปที่ Releases page
- [ ] สร้าง Release ใหม่:
  - [ ] Platform: `windows`
  - [ ] Version: (ตาม SemVer)
  - [ ] Release Notes
  - [ ] Download URL
  - [ ] Set as latest
- [ ] ทดสอบ update notification

---

## 🔍 Post-Deployment Verification

### License Server

- [ ] API accessible: `https://your-license-server.com/docs`
- [ ] CORS ทำงานถูกต้อง
- [ ] Authentication ทำงานถูกต้อง
- [ ] Database connection ทำงาน

### Admin Dashboard

- [ ] Dashboard accessible
- [ ] Login ทำงาน
- [ ] API calls ทำงาน
- [ ] License management ทำงาน

### Desktop App

- [ ] Activation ทำงาน
- [ ] Validation ทำงาน
- [ ] Update check ทำงาน
- [ ] FFmpeg ทำงาน (ถ้า bundle)

---

## 🐛 Troubleshooting

### Common Issues

1. **CORS Error**
   - ตรวจสอบ `CORS_ORIGINS` ใน License Server
   - ตรวจสอบว่า URL ตรงกันทุกตัวอักษร

2. **Environment Variables ไม่ทำงาน**
   - ตรวจสอบว่าใช้ `NEXT_PUBLIC_` prefix สำหรับ client-side variables
   - Redeploy หลังจากแก้ไข environment variables

3. **Database Connection Failed**
   - ตรวจสอบ Supabase URL และ Service Role Key
   - ตรวจสอบว่า migration run แล้ว

4. **Build Failed**
   - ตรวจสอบ dependencies
   - ตรวจสอบ logs ใน deployment platform

---

## 📝 Notes

- เก็บ credentials ไว้ในที่ปลอดภัย
- ใช้ environment variables สำหรับ sensitive data
- ทดสอบทุกขั้นตอนก่อน production
- Backup database เป็นประจำ

---

## 🔗 Quick Links

- **Deployment Guide**: `DEPLOYMENT_GUIDE.md`
- **Vercel + Railway**: `VERCEL_RAILWAY_DEPLOYMENT.md`
- **Vercel + Render**: `VERCEL_RENDER_DEPLOYMENT.md`
- **Distribution Guide**: `DISTRIBUTION_GUIDE.md`
- **Project Structure**: `PROJECT_STRUCTURE.md`
