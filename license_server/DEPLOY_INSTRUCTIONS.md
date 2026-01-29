# คำแนะนำการ Deploy License Server บน VPS

## VPS Information

- **IP**: 157.10.73.171
- **User**: ubuntu
- **Password**: 4f@7K3%qRaTNQdBC#)O*Sy&o2mskJ!

## ขั้นตอนการ Deploy

### Step 1: SSH เข้า VPS

```bash
ssh ubuntu@157.10.73.171
# Password: 4f@7K3%qRaTNQdBC#)O*Sy&o2mskJ!
```

### Step 2: Install Docker (ถ้ายังไม่มี)

**⚠️ สำคัญ**: ไม่ต้องติดตั้ง Python 3.11 บน host เพราะใช้ Docker! Docker image จะมี Python 3.11 อยู่แล้ว

```bash
# Check if Docker is installed
docker --version

# ถ้ายังไม่มี Docker ให้ติดตั้ง:
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt-get update
sudo apt-get install docker-compose-plugin -y

# Add user to docker group (optional, to run without sudo)
sudo usermod -aG docker $USER
# Logout and login again for this to take effect
```

### Step 3: Clone Repository

**Option 1: Clone to /opt (แนะนำ - ต้องใช้ sudo)**

```bash
# Navigate to /opt
cd /opt

# Clone repository with sudo
sudo git clone https://github.com/phearom922/video_mixer_concat.git license-server

# Change ownership to ubuntu user
sudo chown -R ubuntu:ubuntu license-server

# Navigate to license_server directory
cd license-server/license_server
```

**Option 2: Clone to home directory (ง่ายกว่า - ไม่ต้อง sudo)**

```bash
# Clone to home directory
cd ~
git clone https://github.com/phearom922/video_mixer_concat.git license-server

# Navigate to license_server directory
cd license-server/license_server
```

**⚠️ หมายเหตุ**: ถ้าใช้ Option 2 (home directory) path จะเป็น `~/license-server/license_server` แทน `/opt/license-server/license_server`

### Step 4: Navigate to License Server Directory

```bash
cd /opt/license-server/license_server
```

### Step 5: Setup Environment Variables

```bash
# Copy env.example to .env
cp env.example .env

# Edit .env file
nano .env
```

**ตั้งค่าใน `.env`:**

```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here

# JWT Configuration
JWT_SIGNING_SECRET=your-very-long-secret-key-min-32-chars
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=8760

# Device Hashing (optional)
DEVICE_HASH_SALT=

# Admin Configuration
ADMIN_EMAILS=admin@example.com

# CORS Origins (comma-separated)
# ⚠️ ต้องเพิ่ม Vercel URL หลังจาก deploy Admin Dashboard
CORS_ORIGINS=http://localhost:3000,https://your-admin-dashboard.vercel.app

# Rate Limiting
RATE_LIMIT_ACTIVATE_PER_MINUTE=5
RATE_LIMIT_VALIDATE_PER_MINUTE=60

# Grace Period (days)
GRACE_DAYS=7
```

**Save และ Exit**: `Ctrl+X`, `Y`, `Enter`

### Step 6: Make Deploy Script Executable

```bash
chmod +x deploy.sh
```

### Step 7: Run Deployment Script

```bash
./deploy.sh
```

หรือถ้าไม่ใช้ script:

```bash
# Build Docker image
docker-compose build

# Start service
docker-compose up -d

# Check status
docker-compose ps

# Check logs
docker-compose logs -f license-server
```

### Step 8: Verify Deployment

```bash
# Check if service is running
docker-compose ps

# Check service health
curl http://localhost:8001/docs

# Check from external (replace with your VPS IP)
curl http://157.10.73.171:8001/docs
```

### Step 9: Setup Nginx Reverse Proxy (Optional but Recommended)

```bash
# Install nginx (if not installed)
sudo apt update
sudo apt install nginx -y

# Create nginx config
sudo nano /etc/nginx/sites-available/license-server
```

**เนื้อหา nginx config:**

```nginx
server {
    listen 80;
    server_name api-license.yourdomain.com;  # หรือใช้ IP address

    location / {
        proxy_pass http://127.0.0.1:8001;
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

### Step 10: Setup SSL with Let's Encrypt (Recommended)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d api-license.yourdomain.com

# Auto-renewal (already set up by certbot)
sudo certbot renew --dry-run
```

---

## Useful Commands

### Check Service Status

```bash
# Check containers
docker-compose ps

# Check logs
docker-compose logs -f license-server

# Check resource usage
docker stats license-server
```

### Manage Service

```bash
# Stop service
docker-compose down

# Start service
docker-compose up -d

# Restart service
docker-compose restart

# Rebuild and restart
docker-compose up -d --build
```

### Update Service

```bash
# Pull latest code
cd /opt/license-server
git pull

# Rebuild and restart
cd license_server
docker-compose up -d --build
```

---

## Troubleshooting

### Service ไม่ start

```bash
# Check logs
docker-compose logs license-server

# Check container status
docker-compose ps

# Check resource usage
docker stats
```

### Port conflict

```bash
# Check if port 8001 is in use
sudo netstat -tulpn | grep 8001

# หรือ
sudo lsof -i :8001
```

### Memory issues

```bash
# Check memory usage
free -h

# Check Docker memory
docker stats --no-stream
```

---

## Security Notes

1. **Change SSH Password**: เปลี่ยน password หลังจาก deploy สำเร็จ
2. **Setup Firewall**: ตั้งค่า ufw หรือ firewall อื่น
3. **Keep Updated**: อัพเดท system และ Docker images เป็นประจำ
4. **Backup**: Backup `.env` file และ database เป็นประจำ

---

## Next Steps

1. ✅ Deploy License Server (เสร็จแล้ว)
2. ⏭️ Deploy Admin Dashboard บน Vercel
3. ⏭️ อัพเดท `CORS_ORIGINS` ใน `.env` ให้รวม Vercel URL
4. ⏭️ Restart License Server: `docker-compose restart`
5. ⏭️ ทดสอบ API connection จาก Admin Dashboard

---

## Support

ถ้ามีปัญหา:
1. ตรวจสอบ logs: `docker-compose logs -f license-server`
2. ตรวจสอบ resource usage: `docker stats`
3. ตรวจสอบ network: `curl http://localhost:8001/docs`
