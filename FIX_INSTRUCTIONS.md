# คำแนะนำการแก้ไข (Fix Instructions)

## สรุปปัญหา

1. ❌ **license_server/.env**: Service Role Key เป็นของ project อื่น
   - Current: `zipuyqkqaktbaddsdrhc`
   - ต้องเป็น: `ajeudhzebocbwzbifebb`

2. ⚠️ **admin_dashboard/.env**: ต้องตรวจสอบว่า key ถูกต้องหรือไม่

## วิธีแก้ไข

### ขั้นตอนที่ 1: แก้ไข license_server/.env

1. ไปที่ **Supabase Dashboard**:
   ```
   https://ajeudhzebocbwzbifebb.supabase.co
   ```

2. ไปที่ **Settings → API**

3. เลือกแท็บ **"Legacy anon, service_role API keys"**

4. คลิก **"Reveal"** ที่ **service_role secret key**

5. **Copy key ที่ถูกต้อง** (ต้องเป็นของ project `ajeudhzebocbwzbifebb`)

6. เปิดไฟล์ `license_server/.env`

7. หาบรรทัด:
   ```
   SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InppcHV5cWtxYWt0YmFkZHNkcmhjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2OTU3NTU1NywiZXhwIjoyMDg1MTUxNTU3fQ.zJBNmh_AH7j0bh1jvmD6q6esn4p6JKRNdp1YyohWCJ8
   ```

8. แทนที่ด้วย key ใหม่ที่ copy มา:
   ```
   SUPABASE_SERVICE_ROLE_KEY=<paste-new-key-here>
   ```

9. **บันทึกไฟล์**

### ขั้นตอนที่ 2: ตรวจสอบ admin_dashboard/.env

1. เปิดไฟล์ `admin_dashboard/.env`

2. ตรวจสอบว่า:
   - `NEXT_PUBLIC_SUPABASE_URL` = `https://ajeudhzebocbwzbifebb.supabase.co`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY` ต้องเป็น anon key ของ project `ajeudhzebocbwzbifebb`

3. ถ้า key ผิด project:
   - ไปที่ Supabase Dashboard → Settings → API
   - Copy **"anon public"** key (ไม่ใช่ service_role)
   - แทนที่ในไฟล์ `.env`

### ขั้นตอนที่ 3: ตรวจสอบอีกครั้ง

รันสคริปต์ตรวจสอบ:
```bash
python verify_and_fix.py
```

ต้องเห็น:
- ✅ license_server/.env is correct!
- ✅ admin_dashboard/.env is correct!

### ขั้นตอนที่ 4: สร้าง Admin User

หลังจากแก้ไข key แล้ว:
```bash
python test_and_create_user.py
```

## หมายเหตุสำคัญ

- ⚠️ **Service Role Key** ต้องเป็นของ project `ajeudhzebocbwzbifebb`
- ⚠️ **Anon Key** ใน admin_dashboard ต้องเป็นของ project `ajeudhzebocbwzbifebb` เช่นกัน
- ✅ ตรวจสอบ project ref ใน JWT payload ว่าเป็น `ajeudhzebocbwzbifebb`
