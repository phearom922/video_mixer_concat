# ตรวจสอบการ Deploy

## Deployment สำเร็จแล้ว! ✅

จาก terminal output:
- ✅ Docker image build สำเร็จ
- ✅ Container สร้างสำเร็จ
- ✅ Network สร้างสำเร็จ
- ✅ Service ทำงานแล้ว

---

## Warnings (ไม่เป็นปัญหา)

### 1. Version Attribute Warning

```
WARN[0000] the attribute `version` is obsolete
```

**ไม่เป็นปัญหา**: Docker Compose v2 ไม่ต้องการ `version` แล้ว แต่ยังทำงานได้ปกติ

**แก้ไข (optional)**: ลบ `version: '3.8'` ออกจาก docker-compose.yml

### 2. Swap Limit Warning

```
Your kernel does not support swap limit capabilities or the cgroup is not mounted. 
Memory limited without swap.
```

**ไม่เป็นปัญหา**: Memory limits ยังทำงานได้ แต่ไม่มี swap limit (ไม่เป็นปัญหาใหญ่)

---

## ตรวจสอบ Service

### 1. Check Container Status

```bash
docker-compose ps
```

**ควรเห็น:**
```
NAME                STATUS              PORTS
license-server      Up X seconds       0.0.0.0:8001->8000/tcp
```

### 2. Check Logs

```bash
# View logs
docker-compose logs license-server

# Follow logs (real-time)
docker-compose logs -f license-server
```

### 3. Test API

```bash
# Test from localhost
curl http://localhost:8001/docs

# Test from external (replace with your VPS IP)
curl http://157.10.73.171:8001/docs

# Test API endpoint
curl http://localhost:8001/api/v1/releases/latest?platform=windows&current_version=0.0.0
```

### 4. Check Resource Usage

```bash
# Check Docker stats
docker stats license-server --no-stream

# Check system resources
free -h
df -h
```

---

## Troubleshooting

### Service ไม่ start

```bash
# Check logs
docker-compose logs license-server

# Check container status
docker-compose ps -a

# Restart service
docker-compose restart
```

### API ไม่ตอบสนอง

```bash
# Check if port is listening
sudo netstat -tulpn | grep 8001

# Check container logs
docker-compose logs license-server

# Check if .env is correct
cat .env | grep -v "KEY\|SECRET"  # Don't show secrets
```

### Memory Issues

```bash
# Check memory usage
docker stats license-server

# Check system memory
free -h

# Restart if needed
docker-compose restart
```

---

## Next Steps

1. ✅ **Deploy License Server** (เสร็จแล้ว!)
2. ⏭️ **Deploy Admin Dashboard** บน Vercel
3. ⏭️ **อัพเดท CORS_ORIGINS** ใน `.env` ให้รวม Vercel URL
4. ⏭️ **Restart License Server**: `docker-compose restart`
5. ⏭️ **ทดสอบ API connection** จาก Admin Dashboard

---

## Useful Commands

```bash
# Service management
docker-compose ps              # Check status
docker-compose logs -f         # View logs
docker-compose restart         # Restart service
docker-compose down            # Stop service
docker-compose up -d           # Start service

# Update service
cd ~/license-server/license_server
git pull
docker-compose up -d --build   # Rebuild and restart

# Monitoring
docker stats license-server    # Resource usage
docker-compose logs -f         # Real-time logs
```

---

## API Endpoints

หลังจาก deploy สำเร็จ API จะอยู่ที่:

- **Local**: `http://localhost:8001`
- **External**: `http://157.10.73.171:8001`
- **API Docs**: `http://157.10.73.171:8001/docs`

**Endpoints:**
- `POST /api/v1/activate` - Activate license
- `POST /api/v1/validate` - Validate license
- `POST /api/v1/deactivate` - Deactivate license
- `GET /api/v1/releases/latest` - Get latest release

---

## สรุป

✅ **Deployment สำเร็จ!**

- Service ทำงานที่ port **8001**
- API accessible: `http://157.10.73.171:8001`
- Warnings ไม่เป็นปัญหา (optional fixes available)

**Next**: Deploy Admin Dashboard และอัพเดท CORS_ORIGINS
