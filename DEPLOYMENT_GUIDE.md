# คู่มือการ Deploy License Server

เอกสารนี้อธิบายวิธีการ deploy License Server เพื่อให้ Desktop App สามารถ activate license ได้

## ภาพรวม

**Desktop App ต้องการ License Server เพื่อ:**
- Activate license (เมื่อผู้ใช้ใส่ license key)
- Validate license (ตรวจสอบว่า license ยังใช้งานได้)
- Check for updates (ตรวจสอบเวอร์ชั่นใหม่)
- Deactivate license (เมื่อต้องการยกเลิกการใช้งาน)

**License Server ต้อง deploy บน server ที่:**
- สามารถเข้าถึงได้จาก internet (public URL)
- มี Supabase database ที่ตั้งค่าแล้ว
- รองรับ HTTPS (แนะนำ)

---

## ส่วนที่ 1: สำหรับ Admin - การ Deploy License Server

### ขั้นตอนที่ 1: เตรียม Supabase Database

#### 1.1 สร้าง Supabase Project

1. ไปที่ https://supabase.com
2. สร้าง project ใหม่
3. เก็บ **Project URL** และ **Service Role Key** ไว้

#### 1.2 Run Database Migration

1. ไปที่ Supabase Dashboard → SQL Editor
2. Copy เนื้อหาจาก `supabase/migrations/001_initial_schema.sql`
3. Paste และ Run ใน SQL Editor
4. ตรวจสอบว่า tables ถูกสร้างแล้ว:
   - `licenses`
   - `activations`
   - `app_releases`
   - `admin_audit_logs`

### ขั้นตอนที่ 2: Deploy License Server

เลือกวิธีใดวิธีหนึ่ง:

#### วิธีที่ 1: Deploy บน VPS/Cloud Server (แนะนำ)

> **📖 ดูรายละเอียดเพิ่มเติม**: สำหรับการ deploy บน VPS พร้อม resource requirements ดูที่ `VPS_DEPLOYMENT_GUIDE.md`

**ตัวอย่าง: AWS EC2, DigitalOcean, Linode, Vultr, etc.**

1. **เตรียม Server:**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python 3.11+
   sudo apt install python3.11 python3.11-venv python3-pip -y
   
   # Install nginx (optional, for reverse proxy)
   sudo apt install nginx -y
   ```

2. **Clone หรือ Upload Code:**
   ```bash
   # Clone repository หรือ upload code
   cd /opt
   git clone <your-repo> license-server
   cd license-server/license_server
   ```

3. **Setup Environment:**
   ```bash
   # Create virtual environment
   python3.11 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Create .env file
   cp env.example .env
   nano .env  # Edit with your values
   ```

4. **Configure .env:**
   ```env
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
   JWT_SIGNING_SECRET=your-very-long-secret-key-min-32-chars
   ADMIN_EMAILS=admin@example.com
   CORS_ORIGINS=https://your-admin-dashboard.com,https://your-domain.com
   ```

5. **Run with systemd (Production):**
   ```bash
   # Create systemd service file
   sudo nano /etc/systemd/system/license-server.service
   ```
   
   เนื้อหา service file:
   ```ini
   [Unit]
   Description=License Server
   After=network.target
   
   [Service]
   Type=simple
   User=www-data
   WorkingDirectory=/opt/license-server/license_server
   Environment="PATH=/opt/license-server/license_server/venv/bin"
   ExecStart=/opt/license-server/license_server/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```
   
   ```bash
   # Enable and start service
   sudo systemctl daemon-reload
   sudo systemctl enable license-server
   sudo systemctl start license-server
   sudo systemctl status license-server
   ```

6. **Setup Nginx Reverse Proxy (Optional but recommended):**
   ```bash
   sudo nano /etc/nginx/sites-available/license-server
   ```
   
   เนื้อหา:
   ```nginx
   server {
       listen 80;
       server_name api.yourdomain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```
   
   ```bash
   # Enable site
   sudo ln -s /etc/nginx/sites-available/license-server /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

7. **Setup SSL with Let's Encrypt (Recommended):**
   ```bash
   sudo apt install certbot python3-certbot-nginx -y
   sudo certbot --nginx -d api.yourdomain.com
   ```

#### วิธีที่ 2: Deploy บน Railway, Render, Fly.io (Platform as a Service)

**ตัวอย่าง: Railway**

1. สร้าง account ที่ https://railway.app
2. สร้าง New Project
3. Deploy from GitHub หรือ upload code
4. ตั้งค่า Environment Variables:
   - `SUPABASE_URL`
   - `SUPABASE_SERVICE_ROLE_KEY`
   - `JWT_SIGNING_SECRET`
   - `ADMIN_EMAILS`
   - `CORS_ORIGINS`
5. Deploy → จะได้ public URL เช่น `https://your-app.railway.app`

**ตัวอย่าง: Render**

1. สร้าง account ที่ https://render.com
2. สร้าง New Web Service
3. Connect GitHub repository
4. ตั้งค่า:
   - **Build Command**: `pip install -r license_server/requirements.txt`
   - **Start Command**: `cd license_server && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. ตั้งค่า Environment Variables
6. Deploy → จะได้ public URL

> **⚠️ หมายเหตุ**: Render Free Tier จะ sleep หลังจาก idle 15 นาที ทำให้ request แรกช้า (cold start ~30-60 วินาที) แนะนำให้ upgrade เป็น Paid plan ($7/month) หรือใช้ service อื่น

> **📖 ดูรายละเอียดเพิ่มเติม**: 
> - สำหรับการ deploy Admin Dashboard บน Vercel + License Server บน Render ดูที่ `VERCEL_RENDER_DEPLOYMENT.md`
> - สำหรับการ deploy Admin Dashboard บน Vercel + License Server บน Railway (แนะนำ - ไม่ sleep) ดูที่ `VERCEL_RAILWAY_DEPLOYMENT.md`

#### วิธีที่ 3: Deploy บน Docker

1. **Create Dockerfile:**
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY license_server/requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY license_server/ .
   
   EXPOSE 8000
   
   CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Create docker-compose.yml:**
   ```yaml
   version: '3.8'
   services:
     license-server:
       build: .
       ports:
         - "8000:8000"
       env_file:
         - .env
       restart: unless-stopped
   ```

3. **Deploy:**
   ```bash
   docker-compose up -d
   ```

### ขั้นตอนที่ 3: ตั้งค่า API URL ใน Desktop App

#### 3.1 วิธีที่ 1: Hardcode ใน Executable (แนะนำสำหรับ Production)

แก้ไข `desktop_app/app/services/config_service.py`:

```python
def get_api_base_url(self) -> str:
    """Get API base URL."""
    # Production URL - change this before building
    return self.get("api_base_url", "https://api.yourdomain.com")
```

หรือสร้าง environment variable:

```python
import os

def get_api_base_url(self) -> str:
    """Get API base URL."""
    # Check environment variable first, then config, then default
    return os.getenv("API_BASE_URL") or self.get("api_base_url") or "https://api.yourdomain.com"
```

#### 3.2 วิธีที่ 2: ตั้งค่าใน Config File (Flexible)

Desktop App จะอ่าน `api_base_url` จาก config file (`%APPDATA%\VideoMixerConcat\config.json`)

ผู้ใช้สามารถแก้ไขได้เอง หรือ Admin สามารถสร้าง installer ที่ตั้งค่าให้อัตโนมัติ

### ขั้นตอนที่ 4: Deploy Admin Dashboard (Optional)

ถ้าต้องการใช้ Admin Dashboard:

1. Deploy Admin Dashboard บน hosting (Vercel, Netlify, หรือ server ของคุณเอง)
2. ตั้งค่า Environment Variables:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - `NEXT_PUBLIC_ADMIN_EMAILS`
   - `NEXT_PUBLIC_API_BASE_URL` (URL ของ License Server)
3. Build และ Deploy

---

## ส่วนที่ 2: สำหรับ User - การใช้งาน

### Desktop App จะเชื่อมต่อกับ License Server อัตโนมัติ

เมื่อผู้ใช้:
1. เปิด Desktop App
2. ใส่ License Key และคลิก "Activate"
3. Desktop App จะส่ง request ไปที่ License Server:
   - `POST https://api.yourdomain.com/api/v1/activate`
4. License Server จะตรวจสอบและส่ง activation token กลับมา
5. Desktop App จะเก็บ token ไว้และใช้งานต่อไป

**หมายเหตุ:**
- Desktop App ต้องมี internet connection เพื่อ activate
- หลังจาก activate แล้ว สามารถใช้งาน offline ได้ 7 วัน (grace period)
- Desktop App จะ validate license ทุก 24 ชั่วโมง

---

## Checklist สำหรับ Admin

ก่อนส่ง Desktop App ให้ลูกค้า ตรวจสอบ:

- [ ] Supabase Database setup แล้ว
- [ ] License Server deploy แล้วและทำงานได้
- [ ] License Server มี public URL (HTTPS แนะนำ)
- [ ] ตั้งค่า API URL ใน Desktop App แล้ว (hardcode หรือ config)
- [ ] ทดสอบ activation จาก Desktop App แล้ว
- [ ] ทดสอบ validation จาก Desktop App แล้ว
- [ ] ทดสอบ update check จาก Desktop App แล้ว
- [ ] CORS ตั้งค่าถูกต้อง (ถ้าใช้ Admin Dashboard)
- [ ] SSL Certificate ตั้งค่าแล้ว (HTTPS)

---

## Troubleshooting

### ปัญหา: Desktop App ไม่สามารถ activate ได้

**สาเหตุที่เป็นไปได้:**

1. **License Server ไม่ได้ deploy หรือไม่ทำงาน**
   - **วิธีแก้ไข**: ตรวจสอบว่า License Server ทำงานอยู่และสามารถเข้าถึงได้จาก internet

2. **API URL ไม่ถูกต้อง**
   - **วิธีแก้ไข**: ตรวจสอบว่า API URL ใน Desktop App ถูกต้อง
   - ทดสอบ URL ในเบราว์เซอร์: `https://api.yourdomain.com/docs`

3. **CORS Error**
   - **วิธีแก้ไข**: ตรวจสอบว่า `CORS_ORIGINS` ใน License Server ตั้งค่าถูกต้อง

4. **Network/Firewall Block**
   - **วิธีแก้ไข**: ตรวจสอบว่า firewall ไม่ได้ block port 8000 หรือ HTTPS

### ปัญหา: License Server ไม่สามารถเชื่อมต่อ Supabase ได้

**สาเหตุที่เป็นไปได้:**

1. **Supabase URL หรือ Service Role Key ผิด**
   - **วิธีแก้ไข**: ตรวจสอบ `.env` file

2. **Supabase Project ไม่มี tables**
   - **วิธีแก้ไข**: Run migration ใน Supabase SQL Editor

3. **Network Issue**
   - **วิธีแก้ไข**: ตรวจสอบว่า server สามารถเข้าถึง internet ได้

---

## ข้อมูลเพิ่มเติม

- **License Server README**: ดูที่ `license_server/README.md`
- **Supabase Documentation**: https://supabase.com/docs
- **FastAPI Documentation**: https://fastapi.tiangolo.com
- **Uvicorn Documentation**: https://www.uvicorn.org
