#!/bin/bash

# License Server Deployment Script
# This script helps deploy the License Server on VPS with Docker

set -e

echo "=========================================="
echo "License Server Deployment Script"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found!${NC}"
    echo "Creating .env from env.example..."
    if [ -f env.example ]; then
        cp env.example .env
        echo -e "${GREEN}✅ Created .env file${NC}"
        echo -e "${YELLOW}⚠️  Please edit .env file with your actual values!${NC}"
        echo ""
        echo "Required variables:"
        echo "  - SUPABASE_URL"
        echo "  - SUPABASE_SERVICE_ROLE_KEY"
        echo "  - JWT_SIGNING_SECRET"
        echo "  - ADMIN_EMAILS"
        echo "  - CORS_ORIGINS"
        echo ""
        read -p "Press Enter to continue after editing .env file..."
    else
        echo -e "${RED}❌ env.example not found!${NC}"
        exit 1
    fi
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed!${NC}"
    echo ""
    echo "⚠️  IMPORTANT: You don't need to install Python 3.11 on the host!"
    echo "   Docker will handle Python and all dependencies."
    echo ""
    echo "Please install Docker first:"
    echo "  curl -fsSL https://get.docker.com -o get-docker.sh"
    echo "  sudo sh get-docker.sh"
    echo "  sudo apt-get update"
    echo "  sudo apt-get install docker-compose-plugin -y"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed!${NC}"
    echo "Please install Docker Compose first:"
    echo "  sudo apt-get update"
    echo "  sudo apt-get install docker-compose-plugin"
    exit 1
fi

echo -e "${GREEN}✅ Docker and Docker Compose are installed${NC}"
echo ""

# Build Docker image
echo "Building Docker image..."
docker-compose build

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Docker image built successfully${NC}"
else
    echo -e "${RED}❌ Docker build failed!${NC}"
    exit 1
fi

# Start services
echo ""
echo "Starting License Server..."
docker-compose up -d

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ License Server started successfully${NC}"
else
    echo -e "${RED}❌ Failed to start License Server!${NC}"
    exit 1
fi

# Wait a bit for service to start
echo ""
echo "Waiting for service to start..."
sleep 5

# Check service status
echo ""
echo "Service Status:"
docker-compose ps

# Check if service is healthy
echo ""
echo "Checking service health..."
if curl -f http://localhost:8001/docs > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Service is healthy and accessible${NC}"
    echo ""
    echo "License Server is running at:"
    echo "  - Local: http://localhost:8001"
    echo "  - External: http://$(hostname -I | awk '{print $1}'):8001"
    echo "  - API Docs: http://$(hostname -I | awk '{print $1}'):8001/docs"
else
    echo -e "${YELLOW}⚠️  Service may still be starting...${NC}"
    echo "Check logs with: docker-compose logs -f license-server"
fi

echo ""
echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo ""
echo "Useful commands:"
echo "  - View logs: docker-compose logs -f license-server"
echo "  - Stop service: docker-compose down"
echo "  - Restart service: docker-compose restart"
echo "  - Check status: docker-compose ps"
echo "  - Check resources: docker stats license-server"
echo ""
