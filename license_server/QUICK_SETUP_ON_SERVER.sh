#!/bin/bash

# Quick Setup Script - สร้างไฟล์ที่จำเป็นบน server

echo "=========================================="
echo "License Server Quick Setup"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found!"
    echo "Please run this script from license_server directory"
    exit 1
fi

# Create Dockerfile
echo "Creating Dockerfile..."
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

echo "✅ Dockerfile created"

# Create docker-compose.yml
echo "Creating docker-compose.yml..."
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

echo "✅ docker-compose.yml created"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  .env file not found!"
    if [ -f "env.example" ]; then
        echo "Creating .env from env.example..."
        cp env.example .env
        echo "✅ .env created"
        echo "⚠️  Please edit .env file with your actual values!"
    else
        echo "❌ env.example not found!"
    fi
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file: nano .env"
echo "2. Build: docker-compose build"
echo "3. Start: docker-compose up -d"
echo "4. Check: docker-compose ps"
echo ""
