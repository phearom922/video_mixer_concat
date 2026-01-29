# Quick Deploy Guide - License Server

## Quick Start (Copy & Paste)

```bash
# 1. SSH เข้า VPS
ssh ubuntu@157.10.73.171
# Password: 4f@7K3%qRaTNQdBC#)O*Sy&o2mskJ!

# 2. Check Docker (ไม่ต้องติดตั้ง Python 3.11!)
docker --version
docker-compose --version

# ถ้ายังไม่มี Docker:
# curl -fsSL https://get.docker.com -o get-docker.sh
# sudo sh get-docker.sh
# sudo apt-get update
# sudo apt-get install docker-compose-plugin -y

# 3. Clone Repository
# Option 1: Clone to /opt (ต้องใช้ sudo)
cd /opt
sudo git clone https://github.com/phearom922/video_mixer_concat.git license-server
sudo chown -R ubuntu:ubuntu license-server
cd license-server/license_server

# Option 2: Clone to home directory (ง่ายกว่า)
# cd ~
# git clone https://github.com/phearom922/video_mixer_concat.git license-server
# cd license-server/license_server

# 4. Setup .env file
cp env.example .env
nano .env
# ⚠️ แก้ไข values ให้ถูกต้อง:
#   - SUPABASE_URL
#   - SUPABASE_SERVICE_ROLE_KEY
#   - JWT_SIGNING_SECRET
#   - ADMIN_EMAILS
#   - CORS_ORIGINS

# 5. Deploy
chmod +x deploy.sh
./deploy.sh

# หรือใช้ docker-compose โดยตรง:
docker-compose build
docker-compose up -d

# 6. Check status
docker-compose ps
docker-compose logs -f license-server

# 6. Test API
curl http://localhost:8001/docs
curl http://157.10.73.171:8001/docs
```

## Important Notes

- **Port**: License Server ใช้ port **8001** (ไม่ชนกับ payment-service ที่ port 8000)
- **Resource Limits**: ตั้งค่าแล้ว (CPU 50%, Memory 512MB)
- **Health Check**: ตั้งค่าแล้ว (ตรวจสอบทุก 30 วินาที)

## After Deployment

1. เก็บ URL: `http://157.10.73.171:8001` หรือ domain name
2. ใช้ URL นี้ใน `NEXT_PUBLIC_API_BASE_URL` ของ Admin Dashboard
3. อัพเดท `CORS_ORIGINS` ใน `.env` ให้รวม Vercel URL
4. Restart: `docker-compose restart`
