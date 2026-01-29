# Setup Files on Server

ถ้าไฟล์ `Dockerfile` และ `docker-compose.yml` ยังไม่มีใน repository ให้สร้างบน server:

## สร้างไฟล์บน Server

### 1. สร้าง Dockerfile

```bash
cd ~/license-server/license_server
nano Dockerfile
```

**Copy เนื้อหานี้:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/docs || exit 1

# Run application with 1 worker for 1 Core CPU
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
```

**Save**: `Ctrl+X`, `Y`, `Enter`

### 2. สร้าง docker-compose.yml

```bash
nano docker-compose.yml
```

**Copy เนื้อหานี้:**

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
      - "8001:8000"  # Use port 8001 to avoid conflict with payment-service (8000)
    environment:
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_SERVICE_ROLE_KEY=${SUPABASE_SERVICE_ROLE_KEY}
      - JWT_SIGNING_SECRET=${JWT_SIGNING_SECRET}
      - JWT_ALGORITHM=${JWT_ALGORITHM:-HS256}
      - JWT_EXPIRATION_HOURS=${JWT_EXPIRATION_HOURS:-8760}
      - DEVICE_HASH_SALT=${DEVICE_HASH_SALT:-}
      - ADMIN_EMAILS=${ADMIN_EMAILS}
      - CORS_ORIGINS=${CORS_ORIGINS}
      - RATE_LIMIT_ACTIVATE_PER_MINUTE=${RATE_LIMIT_ACTIVATE_PER_MINUTE:-5}
      - RATE_LIMIT_VALIDATE_PER_MINUTE=${RATE_LIMIT_VALIDATE_PER_MINUTE:-60}
      - GRACE_DAYS=${GRACE_DAYS:-7}
    env_file:
      - .env
    networks:
      - license-network
    # Resource limits (important for 1 Core CPU, 2GB RAM)
    deploy:
      resources:
        limits:
          cpus: '0.5'      # Use max 50% CPU (leave 50% for payment-service)
          memory: 512M     # Limit memory to 512MB
        reservations:
          cpus: '0.25'     # Reserve 25% CPU
          memory: 256M     # Reserve 256MB memory
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

**Save**: `Ctrl+X`, `Y`, `Enter`

### 3. ตรวจสอบไฟล์

```bash
# Check if files exist
ls -la Dockerfile docker-compose.yml

# Check .env file
ls -la .env
```

### 4. Build และ Start

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

---

## Quick Commands (Copy & Paste)

```bash
# 1. Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/docs || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
EOF

# 2. Create docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  license-server:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: license-server
    restart: unless-stopped
    ports:
      - "8001:8000"
    env_file:
      - .env
    networks:
      - license-network
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/docs"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

networks:
  license-network:
    driver: bridge
EOF

# 3. Build and start
docker-compose build
docker-compose up -d
docker-compose ps
```
