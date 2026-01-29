#!/bin/bash

# Quick Fix CORS Issue
# รันคำสั่งนี้บน VPS เพื่ออัพเดท CORS_ORIGINS และ restart container

echo "🔧 Fixing CORS configuration..."

cd ~/license-server/license_server || exit 1

# Backup .env
if [ -f .env ]; then
    cp .env .env.backup.$(date +%Y%m%d_%H%M%S)
    echo "✅ Backed up .env file"
fi

# อัพเดท CORS_ORIGINS
if grep -q "CORS_ORIGINS" .env; then
    # อัพเดท CORS_ORIGINS ให้รวม https://mixer.camboskill.com
    sed -i 's|CORS_ORIGINS=.*|CORS_ORIGINS=http://localhost:3000,http://localhost:3001,https://mixer.camboskill.com|' .env
    echo "✅ Updated CORS_ORIGINS in .env"
else
    # เพิ่ม CORS_ORIGINS ถ้ายังไม่มี
    echo "" >> .env
    echo "# CORS Origins (comma-separated)" >> .env
    echo "CORS_ORIGINS=http://localhost:3000,http://localhost:3001,https://mixer.camboskill.com" >> .env
    echo "✅ Added CORS_ORIGINS to .env"
fi

# แสดง CORS_ORIGINS ที่อัพเดทแล้ว
echo ""
echo "📋 Current CORS_ORIGINS:"
grep "CORS_ORIGINS" .env

# Restart Docker container
echo ""
echo "🔄 Restarting Docker container..."
docker-compose restart

# ตรวจสอบ logs
echo ""
echo "📊 Checking container status..."
docker-compose ps

echo ""
echo "✅ Done! Check logs with: docker-compose logs -f license-server"
echo ""
echo "⚠️  Note: Mixed Content Issue"
echo "   Dashboard (HTTPS) → API (HTTP) จะถูก browser บล็อก"
echo "   ควรตั้งค่า HTTPS สำหรับ License Server หรือใช้ Proxy"
