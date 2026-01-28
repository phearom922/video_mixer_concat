# Quick Fix for PostgREST Schema Cache Issue

## ปัญหา
- ✅ CORS ทำงานแล้ว
- ❌ PostgREST schema cache ยังไม่ refresh (PGRST205 error)
- ❌ Dashboard แสดง 500 Internal Server Error

## วิธีแก้ (ทำตามลำดับ)

### ขั้นตอนที่ 1: Reload Schema ผ่าน Supabase Dashboard

1. เปิด browser ไปที่: **https://supabase.com/dashboard/project/zipuyqkqaktbaddsdrhc**
2. คลิก **SQL Editor** (เมนูด้านซ้าย)
3. วางโค้ดนี้:
   ```sql
   NOTIFY pgrst, 'reload schema';
   ```
4. คลิก **Run** (หรือกด Ctrl+Enter)
5. **รอ 30 วินาที**

### ขั้นตอนที่ 2: Restart FastAPI Server

1. หยุด server ปัจจุบัน:
   - ไปที่ terminal ที่รัน FastAPI server
   - กด **Ctrl+C**

2. รัน server ใหม่:
   ```bash
   cd license_server
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. รอให้เห็นข้อความ:
   ```
   INFO:     Application startup complete.
   ```

### ขั้นตอนที่ 3: ทดสอบ

1. เปิด browser ไปที่: **http://localhost:3001/licenses**
2. Refresh หน้า (F5)
3. Login ด้วย:
   - Email: `ronphearom056@gmail.com`
   - Password: `Phearom090790`

### ถ้ายังไม่ได้

ลองอีกครั้ง:
1. รอ **1-2 นาที** (ให้ Supabase auto-refresh)
2. Restart FastAPI server อีกครั้ง
3. Clear browser cache (Ctrl+Shift+Delete)

## สาเหตุ
PostgREST (PostgreSQL REST API) ของ Supabase ต้อง reload schema cache หลังจากสร้างตารางใหม่ ซึ่งอาจใช้เวลาหรือต้องทำ manual reload

## หมายเหตุ
- ตารางมีอยู่แล้วในฐานข้อมูล ✅
- CORS ตั้งค่าแล้ว ✅
- แค่ต้อง reload schema cache ⏳
