# คู่มือการ Deploy ด้วย Vercel + Render

เอกสารนี้อธิบายวิธีการ deploy Admin Dashboard บน Vercel และ License Server บน Render พร้อมข้อควรระวังและวิธีแก้ไขปัญหา

## ภาพรวม

**Architecture:**
```
┌─────────────────┐         ┌──────────────┐         ┌─────────────┐
│  Admin Dashboard│────────▶│  License     │────────▶│  Supabase   │
│  (Vercel)       │         │  Server      │         │  (Database) │
│  Next.js        │         │  (Render)    │         │             │
└─────────────────┘         └──────────────┘         └─────────────┘
       │                            │
       │                            │
       └────────────────────────────┘
              Desktop App
```

---

## ส่วนที่ 1: Deploy License Server บน Render

### ขั้นตอนที่ 1: สร้าง Web Service บน Render

1. **สร้าง Account และ Login:**
   - ไปที่ https://render.com
   - สร้าง account (หรือ login)

2. **สร้าง New Web Service:**
   - คลิก **"New +"** → **"Web Service"**
   - Connect GitHub repository (หรือใช้ Public Git repository)

3. **ตั้งค่า Build และ Start Commands:**
   - **Name**: `license-server` (หรือชื่อที่ต้องการ)
   - **Region**: เลือก region ที่ใกล้ที่สุด (เช่น Singapore)
   - **Branch**: `main` (หรือ branch ที่ต้องการ)
   - **Root Directory**: `license_server` (ถ้า repo มีหลาย folders)
   - **Runtime**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```bash
     uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```
   - **Plan**: เลือก plan ที่ต้องการ (Free tier มีข้อจำกัด)

4. **ตั้งค่า Environment Variables:**
   - ไปที่ **"Environment"** tab
   - เพิ่ม environment variables:
     ```
     SUPABASE_URL=https://your-project.supabase.co
     SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
     JWT_SIGNING_SECRET=your-very-long-secret-key-min-32-chars
     ADMIN_EMAILS=admin@example.com
     CORS_ORIGINS=https://your-admin-dashboard.vercel.app,https://your-custom-domain.com
     ```
   - ⚠️ **สำคัญ**: ต้องเพิ่ม Vercel URL ใน `CORS_ORIGINS` (ดู URL จาก Vercel deployment)

5. **Deploy:**
   - คลิก **"Create Web Service"**
   - Render จะ build และ deploy อัตโนมัติ
   - รอให้ deploy เสร็จ (ประมาณ 2-5 นาที)

6. **เก็บ URL:**
   - หลังจาก deploy สำเร็จ จะได้ URL เช่น `https://license-server.onrender.com`
   - เก็บ URL นี้ไว้เพื่อใช้ใน Admin Dashboard

### ขั้นตอนที่ 2: ตั้งค่า Custom Domain (Optional)

1. ไปที่ **"Settings"** → **"Custom Domains"**
2. เพิ่ม custom domain (เช่น `api.yourdomain.com`)
3. ตั้งค่า DNS records ตามที่ Render แนะนำ
4. Render จะออก SSL certificate อัตโนมัติ

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
   - **Root Directory**: `admin_dashboard` (ถ้า repo มีหลาย folders)
   - **Build Command**: `npm run build` (default)
   - **Output Directory**: `.next` (default)

4. **ตั้งค่า Environment Variables:**
   - ไปที่ **"Environment Variables"**
   - เพิ่ม environment variables:
     ```
     NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
     NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
     NEXT_PUBLIC_ADMIN_EMAILS=admin@example.com
     NEXT_PUBLIC_API_BASE_URL=https://license-server.onrender.com
     ```
   - ⚠️ **สำคัญ**: `NEXT_PUBLIC_API_BASE_URL` ต้องชี้ไปที่ Render URL ที่ได้จากขั้นตอนที่ 1

5. **Deploy:**
   - คลิก **"Deploy"**
   - Vercel จะ build และ deploy อัตโนมัติ
   - รอให้ deploy เสร็จ (ประมาณ 1-3 นาที)

6. **เก็บ URL:**
   - หลังจาก deploy สำเร็จ จะได้ URL เช่น `https://admin-dashboard.vercel.app`
   - เก็บ URL นี้ไว้เพื่อใช้ใน `CORS_ORIGINS` ของ License Server

### ขั้นตอนที่ 2: อัพเดท CORS ใน License Server

หลังจากได้ Vercel URL แล้ว:

1. ไปที่ Render Dashboard → License Server → **"Environment"**
2. แก้ไข `CORS_ORIGINS`:
   ```
   CORS_ORIGINS=https://admin-dashboard.vercel.app,https://your-custom-domain.com
   ```
3. **Redeploy** License Server (Render จะ auto-redeploy เมื่อแก้ไข environment variables)

### ขั้นตอนที่ 3: ตั้งค่า Custom Domain (Optional)

1. ไปที่ Vercel Project → **"Settings"** → **"Domains"**
2. เพิ่ม custom domain (เช่น `admin.yourdomain.com`)
3. ตั้งค่า DNS records ตามที่ Vercel แนะนำ
4. Vercel จะออก SSL certificate อัตโนมัติ

---

## ส่วนที่ 3: ตั้งค่า Desktop App

### ตั้งค่า API URL ใน Desktop App

Desktop App ต้องชี้ไปที่ Render URL ของ License Server:

**วิธีที่ 1: Hardcode ในโค้ด (แนะนำสำหรับ Production)**

แก้ไข `desktop_app/app/services/config_service.py`:

```python
def get_api_base_url(self) -> str:
    """Get API base URL."""
    # Production URL - change this before building
    return self.get("api_base_url", "https://license-server.onrender.com")
```

**วิธีที่ 2: ใช้ Environment Variable**

```python
import os

def get_api_base_url(self) -> str:
    """Get API base URL."""
    return os.getenv("API_BASE_URL") or self.get("api_base_url") or "https://license-server.onrender.com"
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

2. **Render:**
   - รองรับ Python/FastAPI ได้ดี
   - Auto SSL/HTTPS
   - Auto deployment จาก GitHub
   - Free tier มี (แต่มีข้อจำกัด)

### ⚠️ ข้อควรระวัง

1. **Render Free Tier:**
   - **Service จะ sleep หลังจาก idle 15 นาที**
   - **เมื่อ sleep แล้ว request แรกจะช้า (cold start ~30-60 วินาที)**
   - **วิธีแก้**: Upgrade เป็น Paid plan ($7/month) หรือใช้ service อื่น

2. **CORS Configuration:**
   - ต้องตั้งค่า `CORS_ORIGINS` ใน License Server ให้รวม Vercel URL
   - ถ้าใช้ custom domain ต้องเพิ่มทั้ง Vercel URL และ custom domain

3. **Environment Variables:**
   - ต้องตั้งค่าทั้งสองฝั่ง (Vercel และ Render)
   - `NEXT_PUBLIC_API_BASE_URL` ใน Vercel ต้องชี้ไปที่ Render URL

4. **Network Latency:**
   - Vercel และ Render อาจอยู่คนละ region
   - อาจมี latency สูงขึ้นเล็กน้อย (แต่ปกติไม่เป็นปัญหา)

5. **Rate Limiting:**
   - Render free tier อาจมี rate limiting
   - ตรวจสอบ Render documentation

### 🔧 วิธีแก้ปัญหา Render Sleep (Free Tier)

**Option 1: Upgrade เป็น Paid Plan**
- $7/month - ไม่มี sleep
- เหมาะสำหรับ production

**Option 2: ใช้ External Monitoring**
- ตั้งค่า uptime monitoring (เช่น UptimeRobot, Pingdom)
- ให้ ping service ทุก 5-10 นาที เพื่อป้องกัน sleep

**Option 3: ใช้ Service อื่น**
- Railway (มี free tier, ไม่ sleep)
- Fly.io (มี free tier, ไม่ sleep)
- DigitalOcean App Platform
- AWS/GCP/Azure

---

## Checklist สำหรับ Deploy

### License Server (Render):

- [ ] สร้าง Web Service บน Render
- [ ] ตั้งค่า Build Command: `pip install -r requirements.txt`
- [ ] ตั้งค่า Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [ ] ตั้งค่า Environment Variables:
  - [ ] `SUPABASE_URL`
  - [ ] `SUPABASE_SERVICE_ROLE_KEY`
  - [ ] `JWT_SIGNING_SECRET`
  - [ ] `ADMIN_EMAILS`
  - [ ] `CORS_ORIGINS` (เพิ่ม Vercel URL หลังจาก deploy)
- [ ] Deploy สำเร็จ
- [ ] ทดสอบ API: `https://license-server.onrender.com/docs`
- [ ] เก็บ URL ไว้

### Admin Dashboard (Vercel):

- [ ] Import project จาก GitHub
- [ ] ตั้งค่า Root Directory: `admin_dashboard`
- [ ] ตั้งค่า Environment Variables:
  - [ ] `NEXT_PUBLIC_SUPABASE_URL`
  - [ ] `NEXT_PUBLIC_SUPABASE_ANON_KEY`
  - [ ] `NEXT_PUBLIC_ADMIN_EMAILS`
  - [ ] `NEXT_PUBLIC_API_BASE_URL` (Render URL)
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
Access to fetch at 'https://license-server.onrender.com/...' from origin 'https://admin-dashboard.vercel.app' has been blocked by CORS policy
```

**วิธีแก้ไข:**
1. ตรวจสอบว่า `CORS_ORIGINS` ใน License Server รวม Vercel URL
2. ตรวจสอบว่า URL ตรงกันทุกตัวอักษร (รวม https://)
3. Redeploy License Server หลังจากแก้ไข

### ปัญหา: License Server Sleep (Free Tier)

**อาการ:**
- Request แรกหลังจาก idle 15 นาที จะช้ามาก (30-60 วินาที)
- Desktop App activation timeout

**วิธีแก้ไข:**
1. Upgrade เป็น Paid plan ($7/month)
2. ตั้งค่า uptime monitoring เพื่อป้องกัน sleep
3. ใช้ service อื่น (Railway, Fly.io)

### ปัญหา: API Connection Failed

**อาการ:**
- Desktop App ไม่สามารถ activate ได้
- Admin Dashboard ไม่สามารถเรียก API ได้

**วิธีแก้ไข:**
1. ตรวจสอบว่า License Server ทำงานอยู่ (ไปที่ Render Dashboard)
2. ตรวจสอบว่า URL ถูกต้อง
3. ตรวจสอบว่า CORS ตั้งค่าถูกต้อง
4. ตรวจสอบ logs ใน Render Dashboard

### ปัญหา: Environment Variables ไม่ทำงาน

**อาการ:**
- Admin Dashboard ไม่สามารถเรียก API ได้
- API URL ยังเป็น localhost

**วิธีแก้ไข:**
1. ตรวจสอบว่า environment variables ตั้งค่าใน Vercel แล้ว
2. Redeploy Admin Dashboard (Vercel จะ rebuild)
3. ตรวจสอบว่าใช้ `NEXT_PUBLIC_` prefix สำหรับ client-side variables

---

## ข้อมูลเพิ่มเติม

- **Vercel Documentation**: https://vercel.com/docs
- **Render Documentation**: https://render.com/docs
- **Next.js Environment Variables**: https://nextjs.org/docs/basic-features/environment-variables
- **FastAPI CORS**: https://fastapi.tiangolo.com/tutorial/cors/
