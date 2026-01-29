# คู่มือการ Deploy License Server บน VPS

เอกสารนี้อธิบายวิธีการ deploy License Server บน VPS (Virtual Private Server) และ resource requirements

> **📖 สำหรับการ deploy ด้วย Docker**: ดูที่ `DOCKER_DEPLOYMENT_GUIDE.md` (แนะนำถ้ามี services อื่นรันอยู่แล้ว)

---

## Resource Requirements

### Minimum Requirements

สำหรับ License Server (FastAPI):

- **CPU**: 1 Core (พอใช้งานได้)
- **Memory**: 512MB - 1GB (แนะนำ 1GB+)
- **Disk Storage**: 5-10GB (แนะนำ 20GB+)
- **Network**: Public IP address
- **OS**: Ubuntu 20.04+ หรือ Debian 11+ (แนะนำ)

### Recommended Requirements

สำหรับ Production:

- **CPU**: 2 Cores (ดีกว่า)
- **Memory**: 2GB+ (แนะนำ)
- **Disk Storage**: 20GB+ (พอสำหรับ logs และ data)
- **Network**: Public IP + Domain name (optional)

---

## VPS Specs ที่คุณมี

จากภาพที่ส่งมา:
- **CPU**: 1 Core ✅ (พอใช้งานได้)
- **Memory**: 2 GB ✅ (มากกว่า minimum มาก - ดีมาก!)
- **Disk Storage**: 20 GB ✅ (พอใช้งาน)

**สรุป: VPS specs นี้พอใช้งาน License Server ได้ดีมาก!**

---

## ขั้นตอนการ Deploy บน VPS

### Step 1: เตรียม VPS

1. **SSH เข้า VPS:**
   ```bash
   ssh root@your-vps-ip
   ```

2. **Update System:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

3. **Install Python 3.11+:**
   ```bash
   sudo apt install python3.11 python3.11-venv python3-pip -y
   ```

4. **Install Git:**
   ```bash
   sudo apt install git -y
   ```

### Step 2: Clone Repository

```bash
# สร้าง directory
mkdir -p /opt/license-server
cd /opt/license-server

# Clone repository
git clone https://github.com/your-username/FlowMix.git .

# หรือ clone เฉพาะ license_server
git clone https://github.com/your-username/FlowMix.git temp
mv temp/license_server/* .
rm -rf temp
```

### Step 3: Setup Python Environment

```bash
cd /opt/license-server/license_server

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
# Copy env.example
cp env.example .env

# Edit .env file
nano .env
```

**ตั้งค่าใน `.env`:**
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
JWT_SIGNING_SECRET=your-very-long-secret-key-min-32-chars
ADMIN_EMAILS=admin@example.com
CORS_ORIGINS=https://your-admin-dashboard.vercel.app
```

### Step 5: Setup Systemd Service

```bash
# Create systemd service file
sudo nano /etc/systemd/system/license-server.service
```

**เนื้อหา service file:**
```ini
[Unit]
Description=License Server
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/license-server/license_server
Environment="PATH=/opt/license-server/license_server/venv/bin"
ExecStart=/opt/license-server/license_server/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**หมายเหตุ**: ใช้ `--workers 2` สำหรับ 1 Core CPU (ถ้าเป็น 2 Cores ใช้ `--workers 4`)

### Step 6: Start Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable license-server

# Start service
sudo systemctl start license-server

# Check status
sudo systemctl status license-server
```

### Step 7: Setup Nginx Reverse Proxy (Optional but Recommended)

```bash
# Install nginx
sudo apt install nginx -y

# Create nginx config
sudo nano /etc/nginx/sites-available/license-server
```

**เนื้อหา nginx config:**
```nginx
server {
    listen 80;
    server_name api.yourdomain.com;  # หรือใช้ IP address

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

# Test nginx config
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

### Step 8: Setup SSL with Let's Encrypt (Recommended)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d api.yourdomain.com

# Auto-renewal (already set up by certbot)
sudo certbot renew --dry-run
```

---

## Resource Usage Estimation

### License Server (FastAPI + Uvicorn)

**Normal Operation:**
- **Memory**: ~100-200MB (base)
- **CPU**: Low (idle: <1%, active: 5-10%)
- **Disk**: ~500MB (code + dependencies)

**Under Load (100 requests/min):**
- **Memory**: ~200-300MB
- **CPU**: 10-20%
- **Disk**: ~1GB (with logs)

**Your VPS (1 Core, 2GB RAM, 20GB Disk):**
- ✅ **Memory**: 2GB พอมาก (เหลือ ~1.7GB สำหรับ OS และอื่นๆ)
- ✅ **CPU**: 1 Core พอใช้งานได้ (สำหรับ traffic ปานกลาง)
- ✅ **Disk**: 20GB พอมาก (เหลือ ~19GB)

**สรุป: VPS specs นี้พอใช้งานได้ดีมาก!**

---

## Performance Optimization

### สำหรับ 1 Core CPU

1. **ลด Workers:**
   ```ini
   ExecStart=... --workers 1  # หรือ 2 (ไม่เกิน 2)
   ```

2. **Limit Connections:**
   - Nginx: `worker_connections 512;` (default 1024)

3. **Enable Caching:**
   - ใช้ Redis (optional) สำหรับ rate limiting cache

### สำหรับ 2GB RAM

1. **Monitor Memory:**
   ```bash
   # Check memory usage
   free -h
   
   # Check service memory
   sudo systemctl status license-server
   ```

2. **Set Memory Limits (optional):**
   ```ini
   [Service]
   MemoryLimit=1G  # Limit to 1GB
   ```

---

## Monitoring

### Check Service Status

```bash
# Service status
sudo systemctl status license-server

# Service logs
sudo journalctl -u license-server -f

# Resource usage
htop  # หรือ top
```

### Check API

```bash
# Test API
curl http://localhost:8000/docs

# Test from external
curl https://api.yourdomain.com/docs
```

---

## Troubleshooting

### ปัญหา: Service ไม่ start

**ตรวจสอบ:**
```bash
# Check logs
sudo journalctl -u license-server -n 50

# Check Python path
which python3.11

# Check virtual environment
ls -la /opt/license-server/license_server/venv/bin/
```

### ปัญหา: Memory หมด

**แก้ไข:**
- ลด workers: `--workers 1`
- Restart service: `sudo systemctl restart license-server`
- Check memory: `free -h`

### ปัญหา: CPU 100%

**แก้ไข:**
- ลด workers
- Check logs สำหรับ errors
- Optimize database queries

---

## Security

### Firewall

```bash
# Install ufw
sudo apt install ufw -y

# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable
```

### Keep System Updated

```bash
# Auto-update security patches
sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure -plow unattended-upgrades
```

---

## Backup

### Backup Configuration

```bash
# Backup .env file
sudo cp /opt/license-server/license_server/.env /opt/license-server/license_server/.env.backup

# Backup service file
sudo cp /etc/systemd/system/license-server.service /etc/systemd/system/license-server.service.backup
```

---

## Cost Comparison

| Service | Cost | Specs | Sleep |
|---------|------|-------|-------|
| **VPS (STARTUP)** | ~$5-6/month | 1 Core, 2GB RAM, 20GB | ❌ ไม่ sleep |
| **Railway (Hobby)** | $5/month | Shared | ❌ ไม่ sleep |
| **Render (Free)** | Free | Shared | ⚠️ Sleep |
| **Render (Paid)** | $7/month | Shared | ❌ ไม่ sleep |

**สรุป**: VPS ถูกกว่าและให้ control มากกว่า แต่ต้อง setup เอง

---

## Checklist

### Before Deploy:

- [ ] VPS specs พอใช้งาน (1 Core, 2GB RAM, 20GB Disk) ✅
- [ ] SSH access พร้อม
- [ ] Domain name (optional แต่แนะนำ)

### After Deploy:

- [ ] Python 3.11+ ติดตั้งแล้ว
- [ ] Virtual environment สร้างแล้ว
- [ ] Dependencies ติดตั้งแล้ว
- [ ] .env ตั้งค่าครบถ้วน
- [ ] Systemd service ตั้งค่าแล้ว
- [ ] Service ทำงานแล้ว
- [ ] Nginx ตั้งค่าแล้ว (optional)
- [ ] SSL certificate ได้แล้ว (optional)
- [ ] Firewall ตั้งค่าแล้ว
- [ ] API ทำงานได้แล้ว

---

## ข้อมูลเพิ่มเติม

- **FastAPI Deployment**: https://fastapi.tiangolo.com/deployment/
- **Uvicorn Workers**: https://www.uvicorn.org/settings/#workers
- **Systemd Service**: https://www.freedesktop.org/software/systemd/man/systemd.service.html
- **Nginx Reverse Proxy**: https://nginx.org/en/docs/http/ngx_http_proxy_module.html

---

## สรุป

**VPS specs ของคุณ (1 Core, 2GB RAM, 20GB Disk) พอใช้งาน License Server ได้ดีมาก!**

- ✅ Memory 2GB พอมาก (เหลือ ~1.7GB หลัง OS)
- ✅ CPU 1 Core พอใช้งานได้ (สำหรับ traffic ปานกลาง)
- ✅ Disk 20GB พอมาก (เหลือ ~19GB)
- ✅ ไม่ sleep (ทำงานตลอดเวลา)
- ✅ Full control
- ✅ ถูกกว่า Railway/Render (ถ้าใช้ VPS ที่ถูก)

**แนะนำ**: ใช้ `--workers 1` หรือ `2` สำหรับ 1 Core CPU
