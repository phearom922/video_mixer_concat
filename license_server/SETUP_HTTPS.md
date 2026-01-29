# ตั้งค่า HTTPS สำหรับ License Server

## ภาพรวม

ตั้งค่า Nginx reverse proxy พร้อม SSL certificate เพื่อให้ License Server ทำงานผ่าน HTTPS

**ประโยชน์:**
- ✅ แก้ปัญหา Mixed Content (HTTPS → HTTPS)
- ✅ ปลอดภัยกว่า HTTP
- ✅ Browser ไม่บล็อก requests

---

## Prerequisites

- VPS ที่มี root/sudo access
- Domain name (เช่น `api.mixer.camboskill.com`)
- Docker และ Docker Compose ติดตั้งแล้ว
- License Server ทำงานอยู่แล้วที่ port 8001

---

## Step 1: ติดตั้ง Nginx

```bash
ssh ubuntu@157.10.73.171

# Update package list
sudo apt update

# ติดตั้ง Nginx
sudo apt install nginx -y

# ตรวจสอบสถานะ
sudo systemctl status nginx
```

**ควรเห็น:** `active (running)`

---

## Step 2: ตั้งค่า Domain DNS

เพิ่ม A record ใน DNS provider (Namecheap):

```
Type: A Record
Host: api.mixer
Value: 157.10.73.171
TTL: Automatic (หรือ 3600)
```

**ตัวอย่าง (ตามภาพ Namecheap):**
- Domain: `camboskill.com`
- Host: `api.mixer` (subdomain)
- Full domain: `api.mixer.camboskill.com` → `157.10.73.171`

**หมายเหตุ:** 
- ใน Namecheap Host field ให้ใส่ `api.mixer` (ไม่ใช่แค่ `api`)
- Full domain จะเป็น `api.mixer.camboskill.com`

**รอ DNS propagate** (ประมาณ 5-30 นาที)

**ตรวจสอบ DNS:**
```bash
dig api.mixer.camboskill.com
# หรือ
nslookup api.mixer.camboskill.com
```

---

## Step 3: ติดตั้ง Certbot (Let's Encrypt)

```bash
# ติดตั้ง Certbot
sudo apt install certbot python3-certbot-nginx -y

# ตรวจสอบการติดตั้ง
certbot --version
```

---

## Step 4: สร้าง Nginx Configuration

### 4.1 สร้างไฟล์ config

```bash
sudo nano /etc/nginx/sites-available/license-server
```

### 4.2 ใส่เนื้อหาดังนี้

**แทนที่ `api.mixer.camboskill.com` ด้วย domain ของคุณ:**

**⚠️ หมายเหตุ:** ใส่แค่ HTTP (port 80) ก่อน แล้ว Certbot จะเพิ่ม HTTPS (port 443) ให้อัตโนมัติ

```nginx
server {
    listen 80;
    server_name api.mixer.camboskill.com;

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Proxy to License Server
    location / {
        proxy_pass http://localhost:8001;
        proxy_http_version 1.1;
        
        # Headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Port $server_port;
        
        # WebSocket support (ถ้าจำเป็น)
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Health check endpoint
    location /health {
        proxy_pass http://localhost:8001/health;
        access_log off;
    }
}
```

**หมายเหตุ:** 
- ใส่แค่ HTTP (port 80) ก่อน
- Certbot จะเพิ่ม HTTPS (port 443) และ redirect HTTP → HTTPS ให้อัตโนมัติ
- ไม่ต้องใส่ SSL configuration เอง

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # CORS Headers (optional, License Server จัดการเอง)
    # add_header Access-Control-Allow-Origin "https://mixer.camboskill.com" always;
    # add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
    # add_header Access-Control-Allow-Headers "Content-Type, Authorization" always;

    # Proxy to License Server
    location / {
        proxy_pass http://localhost:8001;
        proxy_http_version 1.1;
        
        # Headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Port $server_port;
        
        # WebSocket support (ถ้าจำเป็น)
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Health check endpoint
    location /health {
        proxy_pass http://localhost:8001/health;
        access_log off;
    }
}
```

### 4.3 บันทึกและออก

`Ctrl+X` → `Y` → `Enter`

---

## Step 5: Enable Nginx Site

```bash
# สร้าง symbolic link
sudo ln -s /etc/nginx/sites-available/license-server /etc/nginx/sites-enabled/

# ตรวจสอบ syntax
sudo nginx -t
```

**ควรเห็น:**
```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

---

## Step 6: ตั้งค่า SSL Certificate

### 6.1 รับ SSL Certificate จาก Let's Encrypt

```bash
sudo certbot --nginx -d api.mixer.camboskill.com
```

**คำถามที่ Certbot จะถาม:**

1. **Email address:** ใส่ email ของคุณ (สำหรับการแจ้งเตือน)
2. **Terms of Service:** กด `A` เพื่อ Agree
3. **Share email:** เลือก `Y` หรือ `N` ตามต้องการ
4. **Redirect HTTP to HTTPS:** เลือก `2` (Redirect)

**ผลลัพธ์:**
```
Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/api.mixer.camboskill.com/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/api.mixer.camboskill.com/privkey.pem
```

### 6.2 ตรวจสอบ Nginx config อัตโนมัติ

Certbot จะอัพเดทไฟล์ config อัตโนมัติ:

```bash
# ดู config ที่อัพเดทแล้ว
sudo cat /etc/nginx/sites-available/license-server
```

**ควรเห็น SSL configuration:**
```nginx
ssl_certificate /etc/letsencrypt/live/api.mixer.camboskill.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/api.mixer.camboskill.com/privkey.pem;
```

---

## Step 7: Restart Nginx

```bash
# Reload Nginx (ไม่ต้อง restart)
sudo systemctl reload nginx

# หรือ restart
sudo systemctl restart nginx

# ตรวจสอบสถานะ
sudo systemctl status nginx
```

---

## Step 8: ตั้งค่า Auto-Renewal

SSL certificate จะหมดอายุทุก 90 วัน ตั้งค่า auto-renewal:

```bash
# ทดสอบ renewal
sudo certbot renew --dry-run

# ตั้งค่า cron job (อัพเดททุกวัน)
sudo crontab -e
```

**เพิ่มบรรทัดนี้:**
```
0 0 * * * certbot renew --quiet && systemctl reload nginx
```

**บันทึก:** `Ctrl+X` → `Y` → `Enter`

---

## Step 9: เปิด Firewall Ports

```bash
# ตรวจสอบ firewall status
sudo ufw status

# เปิด port 80 และ 443
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# ตรวจสอบ
sudo ufw status
```

**ควรเห็น:**
```
80/tcp                     ALLOW       Anywhere
443/tcp                    ALLOW       Anywhere
```

---

## Step 10: อัพเดท CORS_ORIGINS

อัพเดท `.env` บน License Server:

```bash
cd ~/license-server/license_server

# แก้ไข .env
nano .env
```

**อัพเดท CORS_ORIGINS:**
```env
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,https://mixer.camboskill.com,https://api.mixer.camboskill.com
```

**บันทึก:** `Ctrl+X` → `Y` → `Enter`

**Restart Docker container:**
```bash
docker-compose restart
```

---

## Step 11: อัพเดท Vercel Environment Variables

1. ไปที่ Vercel Dashboard
2. เลือก Project: `admin_dashboard`
3. ไปที่ **Settings** → **Environment Variables**
4. แก้ไข `NEXT_PUBLIC_API_BASE_URL`:

**เปลี่ยนจาก:**
```
http://157.10.73.171:8001
```

**เป็น:**
```
https://api.mixer.camboskill.com
```

5. **Redeploy** project

---

## Step 12: ทดสอบ

### 12.1 ทดสอบ HTTPS

```bash
# ทดสอบจาก server
curl https://api.mixer.camboskill.com/health

# ควรเห็น:
# {"status":"healthy"}
```

### 12.2 ทดสอบจาก Browser

เปิด Browser และไปที่:
```
https://api.mixer.camboskill.com/docs
```

**ควรเห็น:**
- ✅ URL แสดง `https://` (ไม่ใช่ `http://`)
- ✅ มี padlock icon (🔒) ใน address bar
- ✅ API documentation แสดงปกติ

### 12.3 ทดสอบจาก Admin Dashboard

1. เปิด `https://mixer.camboskill.com/licenses`
2. ตรวจสอบ Browser Console (F12)
3. **ไม่ควรเห็น Mixed Content warnings**
4. ข้อมูลควรแสดงปกติ

---

## Troubleshooting

### Error: "certbot: command not found"

**แก้ไข:**
```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx -y
```

### Error: "Failed to obtain certificate"

**สาเหตุ:**
- DNS ยังไม่ propagate
- Domain ไม่ชี้มาที่ VPS IP
- Port 80 ถูกบล็อก

**แก้ไข:**
```bash
# ตรวจสอบ DNS
dig api.mixer.camboskill.com

# ตรวจสอบ port 80
sudo netstat -tulpn | grep :80

# ตรวจสอบ firewall
sudo ufw status
```

### Error: "502 Bad Gateway"

**สาเหตุ:**
- License Server ไม่ทำงาน
- Port 8001 ไม่ถูกต้อง

**แก้ไข:**
```bash
# ตรวจสอบ License Server
docker-compose ps

# ตรวจสอบ logs
docker-compose logs license-server

# ทดสอบ direct connection
curl http://localhost:8001/health
```

### Error: "SSL certificate expired"

**แก้ไข:**
```bash
# Renew certificate manually
sudo certbot renew

# Reload Nginx
sudo systemctl reload nginx
```

### Error: "Mixed Content" ยังมีอยู่

**แก้ไข:**
1. ตรวจสอบว่า Vercel Environment Variable ถูกต้อง
2. Clear browser cache
3. Hard refresh: `Ctrl+Shift+R` (Windows) หรือ `Cmd+Shift+R` (Mac)

---

## ตรวจสอบ Configuration

### ตรวจสอบ Nginx Config

```bash
# ตรวจสอบ syntax
sudo nginx -t

# ดู config
sudo cat /etc/nginx/sites-available/license-server
```

### ตรวจสอบ SSL Certificate

```bash
# ดู certificate info
sudo certbot certificates

# ตรวจสอบ expiration date
sudo openssl x509 -in /etc/letsencrypt/live/api.mixer.camboskill.com/fullchain.pem -noout -dates
```

### ตรวจสอบ Nginx Logs

```bash
# Access logs
sudo tail -f /var/log/nginx/access.log

# Error logs
sudo tail -f /var/log/nginx/error.log
```

---

## สรุป

**ขั้นตอนที่ทำแล้ว:**
1. ✅ ติดตั้ง Nginx
2. ✅ ตั้งค่า DNS
3. ✅ ติดตั้ง Certbot
4. ✅ สร้าง Nginx config
5. ✅ รับ SSL certificate
6. ✅ ตั้งค่า auto-renewal
7. ✅ เปิด firewall ports
8. ✅ อัพเดท CORS_ORIGINS
9. ✅ อัพเดท Vercel Environment Variables
10. ✅ ทดสอบ

**ผลลัพธ์:**
- ✅ License Server ทำงานผ่าน HTTPS
- ✅ แก้ปัญหา Mixed Content
- ✅ ปลอดภัยกว่า HTTP
- ✅ Browser ไม่บล็อก requests

---

## หมายเหตุ

- SSL certificate จะหมดอายุทุก 90 วัน (auto-renewal จะจัดการให้)
- ถ้าเปลี่ยน domain ต้องทำขั้นตอนใหม่
- ตรวจสอบ logs เป็นประจำเพื่อดู errors

**หลังจากตั้งค่าเสร็จแล้ว Admin Dashboard ควรจะทำงานได้ปกติโดยไม่มี Mixed Content warnings**
