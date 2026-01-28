# Fix PostgREST Schema Cache Issue

## Problem
PostgREST schema cache ไม่ได้ refresh หลังจากสร้างตารางใหม่ ทำให้เกิด error:
```
Could not find the table 'public.licenses' in the schema cache
```

## Solution
ได้รันคำสั่ง SQL เพื่อ refresh PostgREST schema cache แล้ว:
```sql
NOTIFY pgrst, 'reload schema';
```

## Verification
1. รอสักครู่ (2-3 วินาที) เพื่อให้ PostgREST reload schema
2. ทดสอบ API endpoint:
   ```bash
   curl http://localhost:8000/admin/licenses
   ```

## If Still Not Working
1. ตรวจสอบว่า FastAPI server ยังรันอยู่
2. Restart FastAPI server:
   ```bash
   cd license_server
   python -m uvicorn app.main:app --reload
   ```
3. ตรวจสอบ Supabase Dashboard > SQL Editor และรัน:
   ```sql
   NOTIFY pgrst, 'reload schema';
   ```

## CORS Configuration
CORS ได้ตั้งค่าให้รองรับ `localhost:3001` แล้ว:
```
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```
