# ตรวจสอบ DNS Configuration

## การตั้งค่า DNS ใน Namecheap

✅ **ถูกต้องแล้ว!**

**จากภาพที่เห็น:**
- **Type:** A Record
- **Host:** `api.mixer`
- **Value:** `157.10.73.171`
- **TTL:** Automatic

**ผลลัพธ์:**
- Full domain: `api.mixer.camboskill.com` → `157.10.73.171`

---

## ตรวจสอบ DNS Propagation

### วิธีที่ 1: ใช้ dig (บน Linux/Mac)

```bash
dig api.mixer.camboskill.com
```

**ผลลัพธ์ที่ควรเห็น:**
```
;; ANSWER SECTION:
api.mixer.camboskill.com. 3600 IN A 157.10.73.171
```

### วิธีที่ 2: ใช้ nslookup (Windows/Linux/Mac)

```bash
nslookup api.mixer.camboskill.com
```

**ผลลัพธ์ที่ควรเห็น:**
```
Name:    api.mixer.camboskill.com
Address: 157.10.73.171
```

### วิธีที่ 3: ใช้ Online Tools

1. ไปที่ https://dnschecker.org/
2. ใส่ domain: `api.mixer.camboskill.com`
3. เลือก Record Type: `A`
4. คลิก "Search"
5. ตรวจสอบว่า IP address เป็น `157.10.73.171` ทุกที่

### วิธีที่ 4: ใช้ curl (ทดสอบจาก VPS)

```bash
# SSH เข้า VPS
ssh ubuntu@157.10.73.171

# ทดสอบ DNS resolution
curl -I http://api.mixer.camboskill.com
```

---

## ขั้นตอนถัดไป

หลังจาก DNS propagate แล้ว (ประมาณ 5-30 นาที):

1. ✅ **ตรวจสอบ DNS** (ตามวิธีด้านบน)
2. ⏭️ **ติดตั้ง Nginx** (Step 3 ใน SETUP_HTTPS.md)
3. ⏭️ **ติดตั้ง Certbot** (Step 4 ใน SETUP_HTTPS.md)
4. ⏭️ **สร้าง Nginx config** (Step 5 ใน SETUP_HTTPS.md)
5. ⏭️ **รับ SSL certificate** (Step 6 ใน SETUP_HTTPS.md)

---

## Troubleshooting

### DNS ยังไม่ propagate

**รอสักครู่:**
- DNS propagation ใช้เวลา 5-30 นาที (บางครั้งนานถึง 48 ชั่วโมง)
- ตรวจสอบจากหลาย location (ใช้ dnschecker.org)

### DNS ชี้ไปที่ IP ผิด

**แก้ไข:**
1. ไปที่ Namecheap DNS settings
2. แก้ไข A Record สำหรับ `api.mixer`
3. เปลี่ยน Value เป็น `157.10.73.171`
4. Save และรอ propagation

### ไม่สามารถ resolve domain ได้

**ตรวจสอบ:**
- Host name ถูกต้องหรือไม่ (`api.mixer`)
- Domain ถูกต้องหรือไม่ (`camboskill.com`)
- TTL ตั้งค่าเป็น Automatic หรือไม่

---

## หมายเหตุ

- DNS record ที่ตั้งค่าไว้ถูกต้องแล้ว
- รอ DNS propagate ก่อนทำขั้นตอนถัดไป
- ตรวจสอบ DNS ก่อนขอ SSL certificate
