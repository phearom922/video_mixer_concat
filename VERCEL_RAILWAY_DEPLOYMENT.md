# คู่มือการ Deploy ด้วย Vercel + Railway

เอกสารนี้อธิบายวิธีการ deploy Admin Dashboard บน Vercel และ License Server บน Railway พร้อมข้อควรระวังและวิธีแก้ไขปัญหา

## ภาพรวม

**Architecture:**
```
┌─────────────────┐         ┌──────────────┐         ┌─────────────┐
│  Admin Dashboard│────────▶│  License     │────────▶│  Supabase   │
│  (Vercel)       │         │  Server      │         │  (Database) │
│  Next.js        │         │  (Railway)   │         │             │
└─────────────────┘         └──────────────┘         └─────────────┘
       │                            │
       │                            │
       └────────────────────────────┘
              Desktop App
```

---

## ส่วนที่ 1: Deploy License Server บน Railway

### ขั้นตอนที่ 1: สร้าง Project บน Railway

1. **สร้าง Account และ Login:**
   - ไปที่ https://railway.app
   - สร้าง account (หรือ login ด้วย GitHub)

2. **สร้าง New Project:**
   - คลิก **"New Project"**
   - เลือก **"Deploy from GitHub repo"** (แนะนำ) หรือ **"Empty Project"**

3. **Deploy from GitHub (แนะนำ):**
   - เลือก repository ที่มี code
   - Railway จะ auto-detect Python project
   - เลือก **"Add Service"** → **"GitHub Repo"**
   - เลือก branch ที่ต้องการ (เช่น `main`)

4. **ตั้งค่า Service:**
   - Railway จะ detect Python อัตโนมัติ
   - ไปที่ **"Settings"** → **"Source"**
   - ⚠️ **สำคัญ**: ตั้งค่า **Root Directory**: `license_server`
     - คลิก **"Add Root Directory"** หรือ **"Edit"** ในส่วน Source
     - ใส่: `license_server`
     - นี้จะบอกให้ Railway รู้ว่า code อยู่ที่ไหนใน repo

5. **ตั้งค่า Build และ Start Commands:**
   - ไปที่ **"Settings"** → **"Deploy"**
   - **Build Command**: (ไม่จำเป็น - Railway จะ auto-install dependencies)
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```bash
     uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```
   - ⚠️ **สำคัญ**: Railway ใช้ environment variable `$PORT` สำหรับ port

6. **ตั้งค่า Environment Variables:**
   - ไปที่ **"Variables"** tab
   - เพิ่ม environment variables:
     ```
     SUPABASE_URL=https://your-project.supabase.co
     SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
     JWT_SIGNING_SECRET=your-very-long-secret-key-min-32-chars
     ADMIN_EMAILS=admin@example.com
     CORS_ORIGINS=https://your-admin-dashboard.vercel.app,https://your-custom-domain.com
     ```
   - ⚠️ **สำคัญ**: ต้องเพิ่ม Vercel URL ใน `CORS_ORIGINS` (ดู URL จาก Vercel deployment)

7. **Deploy:**
   - Railway จะ auto-deploy เมื่อ push code ไปยัง GitHub
   - หรือคลิก **"Deploy"** เพื่อ deploy manual
   - รอให้ deploy เสร็จ (ประมาณ 1-3 นาที)

8. **เก็บ URL:**
   - หลังจาก deploy สำเร็จ จะได้ URL เช่น `https://license-server-production.up.railway.app`
   - หรือตั้งค่า custom domain (ดูขั้นตอนที่ 2)
   - เก็บ URL นี้ไว้เพื่อใช้ใน Admin Dashboard

### ขั้นตอนที่ 2: ตั้งค่า Custom Domain (Optional)

1. ไปที่ **"Settings"** → **"Networking"**
2. คลิก **"Generate Domain"** เพื่อสร้าง Railway domain
3. หรือเพิ่ม **Custom Domain**:
   - คลิก **"Custom Domain"**
   - เพิ่ม domain (เช่น `api.yourdomain.com`)
   - ตั้งค่า DNS records ตามที่ Railway แนะนำ:
     - Type: `CNAME`
     - Name: `api` (หรือ subdomain ที่ต้องการ)
     - Value: `xxx.up.railway.app` (Railway จะบอก)
   - Railway จะออก SSL certificate อัตโนมัติ

### ขั้นตอนที่ 3: ตั้งค่า Health Check (Optional)

Railway จะตรวจสอบ health อัตโนมัติ แต่ถ้าต้องการ custom:

1. ไปที่ **"Settings"** → **"Healthcheck"**
2. ตั้งค่า **Healthcheck Path**: `/docs` (FastAPI docs endpoint)
3. Railway จะตรวจสอบ service ทุก 30 วินาที

---

## ส่วนที่ 2: Deploy Admin Dashboard บน Vercel

### ขั้นตอนที่ 1: สร้าง Project บน Vercel

1. **สร้าง Account และ Login:**
   - ไปที่ https://vercel.com
   - สร้าง account (หรือ login ด้วย GitHub)

2. **Import Project:**
   - คลิก **"Add New..."** → **"Project"**
   - เลือก GitHub repository
   - Vercel จะ detect Next.js อัตโนมัติ

3. **ตั้งค่า Build Settings:**
   - **Framework Preset**: Next.js (auto-detected)
   - ⚠️ **สำคัญ**: ตั้งค่า **Root Directory**: `admin_dashboard`
     - ไปที่ **"Settings"** → **"General"**
     - ในส่วน **"Root Directory"** ใส่: `admin_dashboard`
     - นี้จะบอกให้ Vercel รู้ว่า code อยู่ที่ไหนใน repo
   - **Build Command**: `npm run build` (default)
   - **Output Directory**: `.next` (default)

4. **ตั้งค่า Environment Variables:**
   - ไปที่ **"Environment Variables"**
   - เพิ่ม environment variables:
     ```
     NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
     NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
     NEXT_PUBLIC_ADMIN_EMAILS=admin@example.com
     NEXT_PUBLIC_API_BASE_URL=https://license-server-production.up.railway.app
     ```
   - ⚠️ **สำคัญ**: `NEXT_PUBLIC_API_BASE_URL` ต้องชี้ไปที่ Railway URL ที่ได้จากขั้นตอนที่ 1

5. **Deploy:**
   - คลิก **"Deploy"**
   - Vercel จะ build และ deploy อัตโนมัติ
   - รอให้ deploy เสร็จ (ประมาณ 1-3 นาที)

6. **เก็บ URL:**
   - หลังจาก deploy สำเร็จ จะได้ URL เช่น `https://admin-dashboard.vercel.app`
   - เก็บ URL นี้ไว้เพื่อใช้ใน `CORS_ORIGINS` ของ License Server

### ขั้นตอนที่ 2: อัพเดท CORS ใน License Server

หลังจากได้ Vercel URL แล้ว:

1. ไปที่ Railway Dashboard → License Server → **"Variables"**
2. แก้ไข `CORS_ORIGINS`:
   ```
   CORS_ORIGINS=https://admin-dashboard.vercel.app,https://your-custom-domain.com
   ```
3. **Redeploy** License Server (Railway จะ auto-redeploy เมื่อแก้ไข environment variables)

### ขั้นตอนที่ 3: ตั้งค่า Custom Domain (Optional)

1. ไปที่ Vercel Project → **"Settings"** → **"Domains"**
2. เพิ่ม custom domain (เช่น `admin.yourdomain.com`)
3. ตั้งค่า DNS records ตามที่ Vercel แนะนำ
4. Vercel จะออก SSL certificate อัตโนมัติ

---

## ส่วนที่ 3: ตั้งค่า Desktop App

### ตั้งค่า API URL ใน Desktop App

Desktop App ต้องชี้ไปที่ Railway URL ของ License Server:

**วิธีที่ 1: Hardcode ในโค้ด (แนะนำสำหรับ Production)**

แก้ไข `desktop_app/app/services/config_service.py`:

```python
def get_api_base_url(self) -> str:
    """Get API base URL."""
    # Production URL - change this before building
    return self.get("api_base_url", "https://license-server-production.up.railway.app")
```

**วิธีที่ 2: ใช้ Environment Variable**

```python
import os

def get_api_base_url(self) -> str:
    """Get API base URL."""
    return os.getenv("API_BASE_URL") or self.get("api_base_url") or "https://license-server-production.up.railway.app"
```

---

## ข้อควรระวังและผลกระทบ

### ✅ ข้อดี

1. **Vercel:**
   - รองรับ Next.js ได้ดี (optimized)
   - Auto SSL/HTTPS
   - Global CDN
   - Auto deployment จาก GitHub
   - Free tier ใช้งานได้ดี

2. **Railway:**
   - **ไม่ sleep** (ไม่มี cold start) - ดีกว่า Render Free Tier
   - Auto SSL/HTTPS
   - Auto deployment จาก GitHub
   - Free tier มี $5 credit/month (พอใช้งานได้)
   - Monitoring และ logs ดี

### ⚠️ ข้อควรระวัง

1. **Railway Free Tier / Trial:**
   - Railway มี **Trial period** (ปกติ 5-7 วัน หรือ $5 credit)
   - **เมื่อ trial หมดแล้วต้อง upgrade เป็น Paid plan** ถึงจะ deploy ได้
   - Paid plan เริ่มต้นที่ **$5/month** (Hobby plan)
   - **ไม่มี sleep** - service ทำงานตลอดเวลา (ดี!)
   - ถ้าใช้เกิน credit จะต้อง upgrade

2. **CORS Configuration:**
   - ต้องตั้งค่า `CORS_ORIGINS` ใน License Server ให้รวม Vercel URL
   - ถ้าใช้ custom domain ต้องเพิ่มทั้ง Vercel URL และ custom domain

3. **Environment Variables:**
   - ต้องตั้งค่าทั้งสองฝั่ง (Vercel และ Railway)
   - `NEXT_PUBLIC_API_BASE_URL` ใน Vercel ต้องชี้ไปที่ Railway URL

4. **Network Latency:**
   - Vercel และ Railway อาจอยู่คนละ region
   - อาจมี latency สูงขึ้นเล็กน้อย (แต่ปกติไม่เป็นปัญหา)

5. **Railway Port:**
   - Railway ใช้ environment variable `$PORT` สำหรับ port
   - ต้องใช้ `--port $PORT` ใน start command

---

## Checklist สำหรับ Deploy

### License Server (Railway):

- [ ] สร้าง Project บน Railway
- [ ] Deploy from GitHub (หรือ Empty Project)
- [ ] ตั้งค่า Root Directory: `license_server` (ถ้าจำเป็น)
- [ ] ตั้งค่า Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [ ] ตั้งค่า Environment Variables:
  - [ ] `SUPABASE_URL`
  - [ ] `SUPABASE_SERVICE_ROLE_KEY`
  - [ ] `JWT_SIGNING_SECRET`
  - [ ] `ADMIN_EMAILS`
  - [ ] `CORS_ORIGINS` (เพิ่ม Vercel URL หลังจาก deploy)
- [ ] Deploy สำเร็จ
- [ ] ทดสอบ API: `https://license-server-production.up.railway.app/docs`
- [ ] เก็บ URL ไว้

### Admin Dashboard (Vercel):

- [ ] Import project จาก GitHub
- [ ] ตั้งค่า Root Directory: `admin_dashboard`
- [ ] ตั้งค่า Environment Variables:
  - [ ] `NEXT_PUBLIC_SUPABASE_URL`
  - [ ] `NEXT_PUBLIC_SUPABASE_ANON_KEY`
  - [ ] `NEXT_PUBLIC_ADMIN_EMAILS`
  - [ ] `NEXT_PUBLIC_API_BASE_URL` (Railway URL)
- [ ] Deploy สำเร็จ
- [ ] เก็บ URL ไว้
- [ ] อัพเดท `CORS_ORIGINS` ใน License Server ให้รวม Vercel URL
- [ ] Redeploy License Server

### Desktop App:

- [ ] ตั้งค่า API URL ในโค้ด (hardcode หรือ environment variable)
- [ ] Build executable
- [ ] ทดสอบ activation จาก Desktop App

---

## Troubleshooting

### ปัญหา: CORS Error ใน Admin Dashboard

**อาการ:**
```
Access to fetch at 'https://license-server-production.up.railway.app/...' from origin 'https://admin-dashboard.vercel.app' has been blocked by CORS policy
```

**วิธีแก้ไข:**
1. ตรวจสอบว่า `CORS_ORIGINS` ใน License Server รวม Vercel URL
2. ตรวจสอบว่า URL ตรงกันทุกตัวอักษร (รวม https://)
3. Redeploy License Server หลังจากแก้ไข

### ปัญหา: Railway Service ไม่ Start

**อาการ:**
- Service ไม่ทำงาน
- Error ใน logs

**วิธีแก้ไข:**
1. ตรวจสอบ Start Command ว่าใช้ `--port $PORT`
2. ตรวจสอบ logs ใน Railway Dashboard
3. ตรวจสอบว่า environment variables ตั้งค่าถูกต้อง

### ปัญหา: API Connection Failed

**อาการ:**
- Desktop App ไม่สามารถ activate ได้
- Admin Dashboard ไม่สามารถเรียก API ได้

**วิธีแก้ไข:**
1. ตรวจสอบว่า License Server ทำงานอยู่ (ไปที่ Railway Dashboard)
2. ตรวจสอบว่า URL ถูกต้อง
3. ตรวจสอบว่า CORS ตั้งค่าถูกต้อง
4. ตรวจสอบ logs ใน Railway Dashboard

### ปัญหา: Environment Variables ไม่ทำงาน

**อาการ:**
- Admin Dashboard ไม่สามารถเรียก API ได้
- API URL ยังเป็น localhost

**วิธีแก้ไข:**
1. ตรวจสอบว่า environment variables ตั้งค่าใน Vercel แล้ว
2. Redeploy Admin Dashboard (Vercel จะ rebuild)
3. ตรวจสอบว่าใช้ `NEXT_PUBLIC_` prefix สำหรับ client-side variables

### ปัญหา: Railway Credit หมด

**อาการ:**
- Service หยุดทำงาน
- ได้ notification จาก Railway

**วิธีแก้ไข:**
1. Upgrade เป็น Paid plan ($5-20/month)
2. หรือใช้ service อื่น (Render, Fly.io)

---

## เปรียบเทียบ Railway vs Render

| Feature | Railway (Paid) | Railway (Trial) | Render (Free) |
|---------|----------------|-----------------|---------------|
| Sleep | ❌ ไม่ sleep | ❌ ไม่ sleep | ⚠️ Sleep หลัง idle 15 นาที |
| Cold Start | ✅ ไม่มี | ✅ ไม่มี | ⚠️ 30-60 วินาที |
| Cost | 💰 $5/month (Hobby) | ✅ Free (5-7 วัน) | ✅ Free (แต่ sleep) |
| Trial Period | - | ⚠️ 5-7 วัน หรือ $5 credit | - |
| Auto Deploy | ✅ | ✅ | ✅ |
| SSL/HTTPS | ✅ | ✅ | ✅ |
| Monitoring | ✅ ดี | ✅ ดี | ✅ ดี |
| Logs | ✅ ดี | ✅ ดี | ✅ ดี |

**สรุป**: 
- **Railway Paid** เหมาะกับ production มากที่สุด (ไม่ sleep, stable)
- **Railway Trial** ดีสำหรับทดสอบ แต่ต้อง upgrade หลัง trial หมด
- **Render Free** ฟรีแต่ sleep (ไม่เหมาะกับ production)

---

## ข้อมูลเพิ่มเติม

- **Vercel Documentation**: https://vercel.com/docs
- **Railway Documentation**: https://docs.railway.app
- **Next.js Environment Variables**: https://nextjs.org/docs/basic-features/environment-variables
- **FastAPI CORS**: https://fastapi.tiangolo.com/tutorial/cors/
- **Railway Pricing**: https://railway.app/pricing
