# การตั้งค่า Root Directory สำหรับ Deployment

เอกสารนี้อธิบายความสำคัญและวิธีการตั้งค่า Root Directory เมื่อ deploy โปรเจกต์ที่มีหลาย folders

## ทำไมต้องตั้งค่า Root Directory?

โปรเจกต์ FlowMix มีโครงสร้างแบบ monorepo (หลาย modules ใน repo เดียว):

```
FlowMix/
├── admin_dashboard/      # Next.js Admin Dashboard
├── desktop_app/          # PySide6 Desktop App
├── license_server/       # FastAPI License Server
└── supabase/             # Database migrations
```

เมื่อ deploy แต่ละ service ต้องระบุ **Root Directory** เพื่อบอก platform ว่า code อยู่ที่ไหน

---

## 1. License Server (Railway/Render)

### Railway

1. ไปที่ Railway Dashboard → Project → Service
2. คลิก **"Settings"** → **"Source"**
3. ในส่วน **"Root Directory"**:
   - คลิก **"Add Root Directory"** หรือ **"Edit"**
   - ใส่: `license_server`
   - คลิก **"Save"**

**ภาพตัวอย่าง:**
```
Source Repo: phearom922/video_mixer_concat
Branch: main
Root Directory: license_server  ← ตั้งค่าตรงนี้
```

### Render

1. ไปที่ Render Dashboard → Service
2. ในส่วน **"Settings"** → **"Build & Deploy"**
3. ในส่วน **"Root Directory"**:
   - ใส่: `license_server`
   - คลิก **"Save Changes"**

---

## 2. Admin Dashboard (Vercel)

1. ไปที่ Vercel Dashboard → Project
2. คลิก **"Settings"** → **"General"**
3. ในส่วน **"Root Directory"**:
   - ใส่: `admin_dashboard`
   - คลิก **"Save"**

**ภาพตัวอย่าง:**
```
Project Name: video-mixer-admin
Framework: Next.js
Root Directory: admin_dashboard  ← ตั้งค่าตรงนี้
```

---

## 3. ตรวจสอบว่า Root Directory ถูกต้อง

### License Server

หลังจากตั้งค่า Root Directory แล้ว Railway/Render จะ:
- ✅ ใช้ `license_server/requirements.txt` สำหรับ dependencies
- ✅ ใช้ `license_server/app/main.py` เป็น entry point
- ✅ ใช้ `license_server/` เป็น working directory

**ตรวจสอบ:**
- ไปที่ **"Deployments"** → ดู logs
- ควรเห็น: `Installing dependencies from requirements.txt`
- ควรเห็น: `Starting: uvicorn app.main:app ...`

### Admin Dashboard

หลังจากตั้งค่า Root Directory แล้ว Vercel จะ:
- ✅ ใช้ `admin_dashboard/package.json` สำหรับ dependencies
- ✅ ใช้ `admin_dashboard/` เป็น working directory
- ✅ Build output จะอยู่ใน `admin_dashboard/.next/`

**ตรวจสอบ:**
- ไปที่ **"Deployments"** → ดู logs
- ควรเห็น: `Installing dependencies from package.json`
- ควรเห็น: `Building Next.js application`

---

## 4. ปัญหาที่พบบ่อย

### ปัญหา: Build Failed - Cannot find requirements.txt

**สาเหตุ:**
- Root Directory ไม่ได้ตั้งค่า หรือตั้งค่าผิด

**วิธีแก้ไข:**
1. ตรวจสอบ Root Directory ใน Settings
2. ตรวจสอบว่า path ถูกต้อง (ไม่มี `/` หน้าหรือหลัง)
3. Redeploy

### ปัญหา: Module not found

**สาเหตุ:**
- Root Directory ตั้งค่าผิด ทำให้ import paths ไม่ถูกต้อง

**วิธีแก้ไข:**
1. ตรวจสอบ Root Directory
2. ตรวจสอบว่า code structure ถูกต้อง
3. ตรวจสอบ logs เพื่อดู working directory

### ปัญหา: Deploy สำเร็จแต่ไม่ทำงาน

**สาเหตุ:**
- Root Directory ถูกต้อง แต่ Start Command ผิด

**วิธีแก้ไข:**
- License Server: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Admin Dashboard: Vercel จะ auto-detect (ไม่ต้องตั้งค่า)

---

## 5. Checklist

### License Server (Railway/Render):

- [ ] Root Directory ตั้งค่าเป็น `license_server`
- [ ] Start Command ใช้ `$PORT` (Railway/Render)
- [ ] Build Command (ถ้ามี): `pip install -r requirements.txt`
- [ ] Environment Variables ตั้งค่าครบถ้วน

### Admin Dashboard (Vercel):

- [ ] Root Directory ตั้งค่าเป็น `admin_dashboard`
- [ ] Framework Preset: Next.js (auto-detected)
- [ ] Build Command: `npm run build` (default)
- [ ] Environment Variables ตั้งค่าครบถ้วน

---

## 6. ตัวอย่างการตั้งค่า

### Railway (License Server):

```
Settings → Source:
├── Source Repo: phearom922/video_mixer_concat
├── Branch: main
└── Root Directory: license_server  ← ตั้งค่าตรงนี้
```

### Vercel (Admin Dashboard):

```
Settings → General:
├── Project Name: video-mixer-admin
├── Framework: Next.js
└── Root Directory: admin_dashboard  ← ตั้งค่าตรงนี้
```

---

## หมายเหตุ

- **Root Directory ไม่มี `/` หน้าหรือหลัง**: ใช้ `license_server` ไม่ใช่ `/license_server` หรือ `license_server/`
- **Case-sensitive**: ตรวจสอบว่าใช้ตัวพิมพ์เล็ก-ใหญ่ถูกต้อง
- **Path ต้องถูกต้อง**: ตรวจสอบว่า folder มีอยู่จริงใน repo

---

## ข้อมูลเพิ่มเติม

- **Railway Docs**: https://docs.railway.app/develop/variables#root-directory
- **Render Docs**: https://render.com/docs/configure-builds#root-directory
- **Vercel Docs**: https://vercel.com/docs/projects/monorepos#root-directory
