# ปัญหา Service Role Key

## สาเหตุ

Key ที่ใช้อยู่เป็นของ **project อื่น**:
- Key ref: `zipuyqkqaktbaddsdrhc`
- Project ของเรา: `ajeudhzebocbwzbifebb`

## วิธีแก้ไข

### 1. ไปที่ Supabase Dashboard

เปิด: https://ajeudhzebocbwzbifebb.supabase.co

### 2. ไปที่ Settings → API

### 3. หา "Legacy anon, service_role API keys" tab

### 4. คลิก "Reveal" ที่ service_role secret key

### 5. Copy key ที่ถูกต้อง (ต้องเป็นของ project `ajeudhzebocbwzbifebb`)

### 6. เปิดไฟล์ `license_server/.env`

### 7. แทนที่บรรทัด:

```
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InppcHV5cWtxYWt0YmFkZHNkcmhjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2OTU3NTU1NywiZXhwIjoyMDg1MTUxNTU3fQ.zJBNmh_AH7j0bh1jvmD6q6esn4p6JKRNdp1YyohWCJ8
```

ด้วย key ใหม่ที่ copy มา

### 8. บันทึกไฟล์

### 9. รันสคริปต์อีกครั้ง:

```bash
python test_and_create_user.py
```

## ตรวจสอบว่า Key ถูกต้อง

หลังจากเปลี่ยน key แล้ว รัน:

```bash
python check_key.py
```

ตรวจสอบว่า:
- Role: `service_role` ✅
- Project Ref: `ajeudhzebocbwzbifebb` ✅ (ไม่ใช่ zipuyqkqaktbaddsdrhc)
