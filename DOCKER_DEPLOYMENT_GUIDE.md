# คู่มือการ Deploy License Server ด้วย Docker

เอกสารนี้อธิบายวิธีการ deploy License Server ด้วย Docker บน VPS ที่มี services อื่นรันอยู่แล้ว

---

## Resource Analysis สำหรับ Multiple Services

### VPS Specs ของคุณ:
- **CPU**: 1 Core
- **Memory**: 2 GB
- **Disk Storage**: 20 GB

### Services ที่รันอยู่:
- **Payment Service** (FastAPI + PostgreSQL)
  - App: ~100-200MB RAM
  - PostgreSQL: ~100-150MB RAM
  - **Total**: ~250-350MB RAM

### License Server Requirements:
- **FastAPI App**: ~100-200MB RAM
- **Total**: ~100-200MB RAM

### Total Resource Usage:

**Memory:**
- OS (Ubuntu): ~300-400MB
- Payment Service: ~250-350MB
- License Server: ~100-200MB
- **Total**: ~650-950MB / 2GB
- **เหลือ**: ~1-1.3GB (พอมาก!)

**CPU:**
- 1 Core พอสำหรับ services 2 ตัว (ถ้า traffic ไม่สูงมาก)
- FastAPI เป็น async framework ใช้ CPU น้อย

**Disk:**
- Payment Service: ~2-3GB
- License Server: ~500MB-1GB
- **Total**: ~3-4GB / 20GB
- **เหลือ**: ~16GB (พอมาก!)

---

## สรุป: VPS Specs พอใช้งานได้

**✅ Memory**: 2GB พอมาก (เหลือ ~1GB+)
**✅ CPU**: 1 Core พอใช้งานได้ (สำหรับ traffic ปานกลาง)
**✅ Disk**: 20GB พอมาก (เหลือ ~16GB)

**⚠️ ข้อควรระวัง:**
- ถ้า traffic สูงมาก อาจต้อง upgrade CPU เป็น 2 Cores
- Monitor memory usage เป็นประจำ
- ตั้งค่า resource limits ใน Docker

---

## ขั้นตอนการ Deploy ด้วย Docker

### Step 1: สร้าง Dockerfile

สร้างไฟล์ `license_server/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
```

**หมายเหตุ**: ใช้ `--workers 1` สำหรับ 1 Core CPU

### Step 2: สร้าง docker-compose.yml

สร้างไฟล์ `license_server/docker-compose.yml`:

```yaml
version: '3.8'

services:
  license-server:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: license-server
    restart: unless-stopped
    ports:
      - "8001:8000"  # ใช้ port 8001 เพื่อไม่ชนกับ payment-service (8000)
    environment:
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_SERVICE_ROLE_KEY=${SUPABASE_SERVICE_ROLE_KEY}
      - JWT_SIGNING_SECRET=${JWT_SIGNING_SECRET}
      - ADMIN_EMAILS=${ADMIN_EMAILS}
      - CORS_ORIGINS=${CORS_ORIGINS}
    env_file:
      - .env
    networks:
      - license-network
    # Resource limits (สำคัญ!)
    deploy:
      resources:
        limits:
          cpus: '0.5'      # ใช้ CPU 50% (เหลือ 50% สำหรับ payment-service)
          memory: 512M    # Limit memory 512MB
        reservations:
          cpus: '0.25'    # Reserve CPU 25%
          memory: 256M    # Reserve memory 256MB
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/docs"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

networks:
  license-network:
    driver: bridge
```

### Step 3: สร้าง .env file

```bash
cd /opt/license-server/license_server
cp env.example .env
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

### Step 4: Build และ Run

```bash
# Navigate to license_server directory
cd /opt/license-server/license_server

# Build image
docker-compose build

# Run in background
docker-compose up -d

# Check status
docker-compose ps

# Check logs
docker-compose logs -f license-server
```

---

## Resource Management

### ตั้งค่า Resource Limits

**สำคัญ**: ตั้งค่า resource limits เพื่อป้องกัน service หนึ่งใช้ resources มากเกินไป

**ใน docker-compose.yml:**
```yaml
deploy:
  resources:
    limits:
      cpus: '0.5'      # ใช้ CPU สูงสุด 50%
      memory: 512M     # ใช้ Memory สูงสุด 512MB
    reservations:
      cpus: '0.25'     # Reserve CPU 25%
      memory: 256M     # Reserve Memory 256MB
```

### Resource Allocation แนะนำ

**สำหรับ 1 Core CPU, 2GB RAM:**

| Service | CPU Limit | Memory Limit | CPU Reserve | Memory Reserve |
|---------|----------|--------------|-------------|---------------|
| **Payment Service** | 0.5 (50%) | 512M | 0.25 (25%) | 256M |
| **License Server** | 0.5 (50%) | 512M | 0.25 (25%) | 256M |
| **OS + Buffer** | - | ~1GB | - | ~1GB |

**สรุป**: แต่ละ service ได้ CPU 50% และ Memory 512MB (พอใช้งานได้)

---

## Port Management

### Port Allocation

- **Payment Service**: Port 8000 (ตามภาพ)
- **License Server**: Port 8001 (แนะนำ)
- **Nginx**: Port 80, 443 (ถ้าใช้ reverse proxy)

### ตั้งค่า Nginx Reverse Proxy (Optional)

ถ้าต้องการใช้ domain name เดียวกัน:

```nginx
# /etc/nginx/sites-available/license-server
server {
    listen 80;
    server_name api-license.yourdomain.com;  # หรือ api2.yourdomain.com

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## Monitoring

### Check Resource Usage

```bash
# Check Docker containers
docker stats

# Check specific container
docker stats license-server

# Check system resources
htop
# หรือ
free -h
df -h
```

### Check Logs

```bash
# License Server logs
docker-compose -f docker-compose.yml logs -f license-server

# All services logs
docker-compose -f docker-compose.yml logs -f
```

### Check Service Status

```bash
# Check containers
docker-compose ps

# Check health
docker inspect license-server | grep Health -A 10
```

---

## Performance Optimization

### สำหรับ 1 Core CPU

1. **ลด Workers:**
   ```dockerfile
   CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
   ```

2. **ใช้ Resource Limits:**
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '0.5'
         memory: 512M
   ```

3. **Monitor และ Adjust:**
   - ตรวจสอบ `docker stats` เป็นประจำ
   - ปรับ limits ตาม actual usage

### สำหรับ Memory Management

1. **Set Memory Limits:**
   ```yaml
   deploy:
     resources:
       limits:
         memory: 512M
   ```

2. **Monitor Memory:**
   ```bash
   docker stats --no-stream
   free -h
   ```

3. **Restart ถ้าจำเป็น:**
   ```bash
   docker-compose restart license-server
   ```

---

## Troubleshooting

### ปัญหา: Container ไม่ start

**ตรวจสอบ:**
```bash
# Check logs
docker-compose logs license-server

# Check container status
docker-compose ps

# Check resource usage
docker stats
```

### ปัญหา: Memory หมด

**แก้ไข:**
1. ลด memory limit ใน docker-compose.yml
2. Restart container: `docker-compose restart license-server`
3. Check system memory: `free -h`

### ปัญหา: CPU 100%

**แก้ไข:**
1. ลด CPU limit ใน docker-compose.yml
2. ลด workers: `--workers 1`
3. Check logs สำหรับ errors

### ปัญหา: Port conflict

**แก้ไข:**
1. เปลี่ยน port ใน docker-compose.yml:
   ```yaml
   ports:
     - "8001:8000"  # ใช้ port 8001 แทน 8000
   ```
2. Restart: `docker-compose restart license-server`

---

## Best Practices

### 1. ใช้ Resource Limits เสมอ

```yaml
deploy:
  resources:
    limits:
      cpus: '0.5'
      memory: 512M
```

### 2. ใช้ Health Checks

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/docs"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### 3. ใช้ Restart Policy

```yaml
restart: unless-stopped
```

### 4. ใช้ .env file สำหรับ Secrets

```yaml
env_file:
  - .env
```

### 5. Monitor เป็นประจำ

```bash
# Setup monitoring script
#!/bin/bash
docker stats --no-stream > /tmp/docker-stats.txt
free -h >> /tmp/docker-stats.txt
```

---

## Comparison: Docker vs Systemd

| Feature | Docker | Systemd |
|---------|--------|---------|
| **Isolation** | ✅ ดี (container isolation) | ❌ ไม่มี |
| **Resource Limits** | ✅ ง่าย (docker-compose) | ⚠️ ต้องตั้งค่าเอง |
| **Port Management** | ✅ ง่าย | ⚠️ ต้องตั้งค่าเอง |
| **Deployment** | ✅ ง่าย (docker-compose) | ⚠️ ต้อง setup เอง |
| **Resource Overhead** | ⚠️ ~50-100MB per container | ✅ น้อยกว่า |
| **Management** | ✅ ง่าย (docker commands) | ⚠️ systemctl commands |

**สรุป**: Docker ดีกว่าเพราะ:
- ✅ Isolation ดีกว่า
- ✅ Resource management ง่ายกว่า
- ✅ Deployment ง่ายกว่า
- ✅ Consistent environment

---

## Checklist

### Before Deploy:

- [ ] VPS specs พอใช้งาน (1 Core, 2GB RAM) ✅
- [ ] Docker และ Docker Compose ติดตั้งแล้ว
- [ ] Port 8001 ว่าง (หรือเปลี่ยนเป็น port อื่น)
- [ ] .env file ตั้งค่าครบถ้วน

### After Deploy:

- [ ] Docker image build สำเร็จ
- [ ] Container ทำงานแล้ว
- [ ] Resource limits ตั้งค่าแล้ว
- [ ] Health check ทำงาน
- [ ] API ทำงานได้ (http://your-vps-ip:8001/docs)
- [ ] Monitoring setup แล้ว

---

## สรุป

**VPS specs ของคุณ (1 Core, 2GB RAM) พอสำหรับ run License Server ด้วย Docker เพิ่มเติมได้!**

- ✅ **Memory**: 2GB พอมาก (เหลือ ~1GB+ หลัง payment-service)
- ✅ **CPU**: 1 Core พอใช้งานได้ (ใช้ resource limits)
- ✅ **Disk**: 20GB พอมาก (เหลือ ~16GB)
- ✅ **Docker**: ดีกว่า systemd (isolation, resource management)

**ข้อควรระวัง:**
- ตั้งค่า resource limits เสมอ
- Monitor resource usage เป็นประจำ
- ใช้ `--workers 1` สำหรับ 1 Core CPU

**แนะนำ**: ใช้ Docker เพราะ:
- ✅ Isolation ดีกว่า
- ✅ Resource management ง่ายกว่า
- ✅ Deployment ง่ายกว่า
- ✅ Consistent environment

---

## ข้อมูลเพิ่มเติม

- **Docker Documentation**: https://docs.docker.com/
- **Docker Compose**: https://docs.docker.com/compose/
- **FastAPI Deployment**: https://fastapi.tiangolo.com/deployment/
- **Uvicorn Workers**: https://www.uvicorn.org/settings/#workers
