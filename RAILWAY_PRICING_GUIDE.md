# Railway Pricing Guide

เอกสารนี้อธิบายเกี่ยวกับ Railway pricing, trial period, และวิธี upgrade

---

## Railway Pricing Overview

### Trial Period

- **Duration**: 5-7 วัน หรือ $5 credit (แล้วแต่ว่าอะไรหมดก่อน)
- **Features**: 
  - ✅ ไม่ sleep (service ทำงานตลอดเวลา)
  - ✅ Auto SSL/HTTPS
  - ✅ Auto deployment
  - ✅ Monitoring และ logs
- **Limitation**: 
  - ⚠️ **เมื่อ trial หมดแล้วต้อง upgrade ถึงจะ deploy ได้**

### Paid Plans

#### Hobby Plan - $5/month

**เหมาะสำหรับ:**
- Personal projects
- Small production applications
- Development/staging environments

**Features:**
- ✅ ไม่ sleep
- ✅ $5 credit/month (พอสำหรับ service เล็กๆ)
- ✅ Auto SSL/HTTPS
- ✅ Auto deployment
- ✅ Monitoring และ logs
- ✅ Custom domains

**Resource Limits:**
- Memory: 512MB per service
- CPU: Shared
- Bandwidth: Included

#### Pro Plan - $20/month

**เหมาะสำหรับ:**
- Production applications
- High-traffic services
- Multiple services

**Features:**
- ✅ ทุกอย่างใน Hobby plan
- ✅ $20 credit/month
- ✅ Priority support
- ✅ Higher resource limits
- ✅ Team collaboration

**Resource Limits:**
- Memory: 8GB per service
- CPU: Dedicated
- Bandwidth: Higher limits

---

## เมื่อ Trial หมดแล้ว

### Error Message

เมื่อ trial หมดแล้ว Railway จะแสดง error:

```
Unable to deploy
Your trial has expired. Please select a plan to continue using Railway.
```

### วิธีแก้ไข

#### Option 1: Upgrade เป็น Paid Plan (แนะนำ)

1. **ไปที่ Railway Dashboard:**
   - Login ที่ https://railway.app
   - ไปที่ Project ที่ต้องการ

2. **Upgrade Plan:**
   - คลิก **"Settings"** → **"Billing"**
   - หรือคลิกที่ notification ที่แสดง error
   - เลือก plan:
     - **Hobby Plan**: $5/month (แนะนำสำหรับเริ่มต้น)
     - **Pro Plan**: $20/month (สำหรับ production)

3. **Payment:**
   - ใส่ payment method (Credit Card, PayPal)
   - Confirm payment
   - หลังจาก upgrade แล้วจะสามารถ deploy ได้ทันที

4. **Verify:**
   - ตรวจสอบว่า service deploy ได้แล้ว
   - ตรวจสอบ billing ใน Settings

#### Option 2: ใช้ Service อื่น (Free Tier)

ถ้าไม่ต้องการจ่ายเงิน สามารถใช้ service อื่นได้:

**Render (Free Tier):**
- ✅ Free forever
- ⚠️ Sleep หลัง idle 15 นาที (cold start 30-60 วินาที)
- เหมาะสำหรับ: Development, testing
- ไม่เหมาะสำหรับ: Production (เพราะ sleep)

**Fly.io (Free Tier):**
- ✅ Free tier (มี resource limits)
- ⚠️ มีข้อจำกัดบางอย่าง
- เหมาะสำหรับ: Small projects

**VPS (Paid):**
- DigitalOcean: $5-6/month
- Vultr: $5-6/month
- Linode: $5/month
- เหมาะสำหรับ: Full control, production

---

## เปรียบเทียบ Options

| Service | Cost | Sleep | Cold Start | เหมาะสำหรับ |
|---------|------|-------|------------|-------------|
| **Railway (Paid)** | $5/month | ❌ ไม่ sleep | ✅ ไม่มี | ✅ Production |
| **Railway (Trial)** | Free (5-7 วัน) | ❌ ไม่ sleep | ✅ ไม่มี | ⚠️ Testing only |
| **Render (Free)** | Free | ⚠️ Sleep | ⚠️ 30-60s | ⚠️ Development |
| **Render (Paid)** | $7/month | ❌ ไม่ sleep | ✅ ไม่มี | ✅ Production |
| **Fly.io (Free)** | Free | ❌ ไม่ sleep | ✅ ไม่มี | ⚠️ Limited resources |
| **VPS** | $5-6/month | ❌ ไม่ sleep | ✅ ไม่มี | ✅ Full control |

---

## คำแนะนำ

### สำหรับ Production

**แนะนำ: Railway Hobby Plan ($5/month)**
- ✅ ไม่ sleep
- ✅ Stable และ reliable
- ✅ Easy deployment
- ✅ Good monitoring

### สำหรับ Development/Testing

**แนะนำ: Render Free Tier**
- ✅ Free
- ⚠️ Sleep (แต่ไม่เป็นปัญหาสำหรับ testing)
- ✅ Easy setup

### สำหรับ Budget Limited

**แนะนำ: VPS (DigitalOcean, Vultr)**
- ✅ $5-6/month
- ✅ Full control
- ✅ No sleep
- ⚠️ ต้อง setup เอง (ใช้ Docker หรือ systemd)

---

## FAQ

### Q: Railway Trial หมดแล้วต้องจ่ายเงินเลยไหม?

**A:** ใช่ ต้อง upgrade เป็น Paid plan ($5/month) ถึงจะ deploy ได้ แต่ถ้าไม่ต้องการจ่ายสามารถใช้ Render Free Tier แทนได้ (แต่จะ sleep)

### Q: Railway Hobby Plan ($5/month) พอไหมสำหรับ License Server?

**A:** พอมาก สำหรับ License Server ที่มี traffic ไม่สูง Hobby Plan ($5 credit/month) พอใช้งานได้

### Q: ถ้าใช้เกิน $5 credit/month จะเกิดอะไรขึ้น?

**A:** Railway จะ charge เพิ่มตาม usage หรือคุณสามารถ upgrade เป็น Pro Plan ($20/month) ได้

### Q: Render Free Tier ดีกว่า Railway Paid ไหม?

**A:** สำหรับ Production: **ไม่ดีกว่า** เพราะ Render Free Tier จะ sleep ทำให้ request แรกช้า (30-60 วินาที) ไม่เหมาะกับ production

### Q: มีวิธีใช้ Railway ฟรีได้ไหม?

**A:** ไม่มี Railway ไม่มี free tier แบบถาวร มีแค่ trial period เท่านั้น หลังจากหมดแล้วต้อง upgrade

---

## Links

- **Railway Pricing**: https://railway.app/pricing
- **Railway Billing**: https://railway.app/account/billing
- **Render Pricing**: https://render.com/pricing
- **Fly.io Pricing**: https://fly.io/docs/about/pricing/

---

## สรุป

- **Railway Trial**: ดีสำหรับทดสอบ แต่ต้อง upgrade หลังหมด
- **Railway Paid ($5/month)**: เหมาะกับ production (ไม่ sleep, stable)
- **Render Free**: ฟรีแต่ sleep (ไม่เหมาะกับ production)
- **VPS**: ถูกกว่าแต่ต้อง setup เอง

**คำแนะนำ**: สำหรับ production ใช้ **Railway Hobby Plan ($5/month)** เป็นตัวเลือกที่ดีที่สุด
