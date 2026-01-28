# คู่มือการตั้งค่า (Setup Guide)

## ข้อมูลที่ได้จาก Supabase แล้ว

- **Supabase URL**: `https://ajeudhzebocbwzbifebb.supabase.co`
- **Supabase Anon Key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFqZXVkaHplYm9jYnd6YmlmZWJiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njg3MjUxNjksImV4cCI6MjA4NDMwMTE2OX0.fHgr4gq5_Zv6Ry6kEjkV_eaHSkx0tt-AIpVkNCtAW7o`
- **JWT Signing Secret** (สร้างให้แล้ว): `2dp-y1XYn7kfm3cnWNEFUTPHLq8vbvCr-iOvdkv0C6o`

## ขั้นตอนการตั้งค่า

### 1. FastAPI License Server

สร้างไฟล์ `license_server/.env` ด้วยเนื้อหาด้านล่าง:

```env
# Supabase Configuration
SUPABASE_URL=https://ajeudhzebocbwzbifebb.supabase.co
SUPABASE_SERVICE_ROLE_KEY=YOUR_SERVICE_ROLE_KEY_HERE

# JWT Configuration
JWT_SIGNING_SECRET=2dp-y1XYn7kfm3cnWNEFUTPHLq8vbvCr-iOvdkv0C6o
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=8760

# Device Hashing (optional)
DEVICE_HASH_SALT=

# Admin Configuration
# IMPORTANT: Replace with your actual admin email(s)
ADMIN_EMAILS=your-email@example.com

# CORS Origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Rate Limiting
RATE_LIMIT_ACTIVATE_PER_MINUTE=5
RATE_LIMIT_VALIDATE_PER_MINUTE=60

# Grace Period (days)
GRACE_DAYS=7
```

**สิ่งที่ต้องทำ:**
1. หา **Service Role Key** จาก Supabase Dashboard:
   - ไปที่ https://ajeudhzebocbwzbifebb.supabase.co
   - Settings → API
   - คัดลอก **service_role** key (⚠️ อย่าเปิดเผย key นี้!)
   - ใส่ใน `SUPABASE_SERVICE_ROLE_KEY`

2. เปลี่ยน `ADMIN_EMAILS` เป็น email ของคุณที่ใช้ login Supabase

### 2. Next.js Admin Dashboard

สร้างไฟล์ `admin_dashboard/.env.local` ด้วยเนื้อหาด้านล่าง:

```env
# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=https://ajeudhzebocbwzbifebb.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFqZXVkaHplYm9jYnd6YmlmZWJiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njg3MjUxNjksImV4cCI6MjA4NDMwMTE2OX0.fHgr4gq5_Zv6Ry6kEjkV_eaHSkx0tt-AIpVkNCtAW7o

# Admin Configuration
# IMPORTANT: Replace with your actual admin email(s) - must match Supabase Auth users
NEXT_PUBLIC_ADMIN_EMAILS=your-email@example.com

# API Configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

**สิ่งที่ต้องทำ:**
1. เปลี่ยน `NEXT_PUBLIC_ADMIN_EMAILS` เป็น email ของคุณ (ต้องตรงกับ email ที่ใช้ login Supabase)
2. ตรวจสอบว่า `NEXT_PUBLIC_API_BASE_URL` ตรงกับ FastAPI server

### 3. Desktop App

Desktop app ไม่ต้องมีไฟล์ .env เพราะจะใช้ค่า default หรือตั้งค่าใน UI

แต่ถ้าต้องการตั้งค่า API URL เริ่มต้น ให้แก้ไขใน:
- `desktop_app/app/services/config_service.py` หรือ
- ตั้งค่าใน UI เมื่อรัน app

## การรันระบบ

### 1. รัน FastAPI License Server

```bash
cd license_server
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Server จะรันที่ http://localhost:8000
- API Docs: http://localhost:8000/docs

### 2. รัน Next.js Admin Dashboard

```bash
cd admin_dashboard
npm install
npm run dev
```

Dashboard จะรันที่ http://localhost:3000

### 3. รัน Desktop App

```bash
cd desktop_app
pip install -r requirements.txt
python -m app.main
```

## สร้าง Admin User ใน Supabase

ก่อนใช้งาน dashboard คุณต้องสร้าง user ใน Supabase Auth:

1. ไปที่ Supabase Dashboard → Authentication → Users
2. คลิก "Add user" → "Create new user"
3. ใส่ email และ password
4. ใช้ email เดียวกันนี้ใน `ADMIN_EMAILS` ของทั้ง FastAPI และ Next.js

## ทดสอบระบบ

1. **ทดสอบ FastAPI:**
   - เปิด http://localhost:8000/docs
   - ทดสอบ endpoint `/health`

2. **ทดสอบ Dashboard:**
   - เปิด http://localhost:3000
   - Login ด้วย email ที่ตั้งค่าไว้
   - สร้าง license ใหม่

3. **ทดสอบ Desktop App:**
   - รัน app
   - ใช้ license key ที่สร้างจาก dashboard
   - ตรวจสอบว่า activation สำเร็จ

## หมายเหตุสำคัญ

- ⚠️ **Service Role Key** ต้องเก็บเป็นความลับ อย่า commit ลง git
- ⚠️ **JWT Signing Secret** ควรเปลี่ยนใน production
- ⚠️ **Admin Emails** ต้องตรงกันทั้ง FastAPI และ Next.js
- ⚠️ ตรวจสอบ CORS origins ใน production
