# Docker Setup Guide

## ⚠️ สำคัญ: ไม่ต้องติดตั้ง Python 3.11 บน Host!

เมื่อใช้ Docker คุณ**ไม่ต้องติดตั้ง Python 3.11** บน VPS เพราะ:
- ✅ Docker image จะมี Python 3.11 อยู่แล้ว
- ✅ Docker จัดการ dependencies ทั้งหมดให้
- ✅ ไม่ต้องกังวลเรื่อง Python version conflicts

---

## สิ่งที่ต้องมี

### 1. Docker (เท่านั้น!)

```bash
# Check if Docker is installed
docker --version

# ถ้ายังไม่มี ให้ติดตั้ง:
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### 2. Docker Compose

```bash
# Check if Docker Compose is installed
docker-compose --version
# หรือ
docker compose version

# ถ้ายังไม่มี ให้ติดตั้ง:
sudo apt-get update
sudo apt-get install docker-compose-plugin -y
```

---

## Error ที่เจอ

ถ้าเจอ error:
```
E: Unable to locate package python3.11
```

**ไม่เป็นไร!** เพราะ:
- ❌ ไม่ต้องติดตั้ง Python 3.11 บน host
- ✅ Docker จะจัดการให้เอง

---

## ขั้นตอนที่ถูกต้อง

### 1. ติดตั้ง Docker (ถ้ายังไม่มี)

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt-get update
sudo apt-get install docker-compose-plugin -y

# Verify installation
docker --version
docker-compose --version
```

### 2. Clone Repository

```bash
cd /opt
git clone https://github.com/your-username/FlowMix.git license-server
cd license-server/license_server
```

### 3. Setup .env

```bash
cp env.example .env
nano .env
# แก้ไข values ให้ถูกต้อง
```

### 4. Deploy

```bash
# Build และ Start
docker-compose build
docker-compose up -d

# Check status
docker-compose ps
docker-compose logs -f license-server
```

---

## เปรียบเทียบ: Docker vs System Python

| Feature | Docker | System Python |
|---------|--------|---------------|
| **Python Version** | ✅ 3.11 (ใน image) | ⚠️ ต้องติดตั้งเอง |
| **Dependencies** | ✅ จัดการโดย Docker | ⚠️ ต้องติดตั้งเอง |
| **Isolation** | ✅ แยกจาก system | ❌ ใช้ system Python |
| **Portability** | ✅ ทำงานเหมือนกันทุกที่ | ⚠️ ขึ้นกับ system |
| **Setup** | ✅ ง่าย (แค่ Docker) | ⚠️ ซับซ้อนกว่า |

**สรุป**: Docker ง่ายกว่าและดีกว่า!

---

## Troubleshooting

### Docker ไม่ทำงาน

```bash
# Check Docker service
sudo systemctl status docker

# Start Docker
sudo systemctl start docker

# Enable Docker on boot
sudo systemctl enable docker
```

### Permission Denied

```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Logout and login again
exit
# SSH เข้าใหม่
```

### Port Already in Use

```bash
# Check what's using port 8001
sudo netstat -tulpn | grep 8001

# หรือเปลี่ยน port ใน docker-compose.yml
# ports:
#   - "8002:8000"  # ใช้ port 8002 แทน
```

---

## สรุป

**ไม่ต้องติดตั้ง Python 3.11 บน host!**

แค่:
1. ✅ ติดตั้ง Docker
2. ✅ ติดตั้ง Docker Compose
3. ✅ Clone repository
4. ✅ Setup .env
5. ✅ Run `docker-compose up -d`

Docker จะจัดการทุกอย่างให้เอง! 🐳
