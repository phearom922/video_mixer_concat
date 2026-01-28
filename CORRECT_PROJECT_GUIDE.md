# ⚠️ สำคัญ: คุณกำลังดู Project ผิด!

## ปัญหา

คุณกำลังดู Supabase Dashboard ของ **project ผิด**:
- ❌ Project ที่คุณกำลังดู: `zipuyqkqaktbaddsdrhc`
- ✅ Project ที่ถูกต้อง: `ajeudhzebocbwzbifebb`

## วิธีแก้ไข

### ขั้นตอนที่ 1: ไปที่ Project ที่ถูกต้อง

1. **เปิด Supabase Dashboard:**
   ```
   https://supabase.com/dashboard
   ```

2. **เลือก Project ที่ถูกต้อง:**
   - หา project ที่มีชื่อ **"FlowMix"** หรือ
   - Project URL: `https://ajeudhzebocbwzbifebb.supabase.co`
   - Project Ref: `ajeudhzebocbwzbifebb`

3. **ตรวจสอบว่าเป็น Project ถูกต้อง:**
   - ดูที่ URL ใน browser
   - ต้องมี: `/project/ajeudhzebocbwzbifebb/`
   - **ไม่ใช่**: `/project/zipuyqkqaktbaddsdrhc/`

### ขั้นตอนที่ 2: Copy Service Role Key จาก Project ที่ถูกต้อง

1. หลังจากเข้า project `ajeudhzebocbwzbifebb` แล้ว

2. ไปที่ **Settings → API**

3. เลือกแท็บ **"Legacy anon, service_role API keys"**

4. คลิก **"Reveal"** ที่ **service_role secret key**

5. **Copy key** (ต้องเป็นของ project `ajeudhzebocbwzbifebb`)

6. เปิดไฟล์ `license_server/.env`

7. แทนที่ Service Role Key:
   ```
   SUPABASE_SERVICE_ROLE_KEY=<paste-key-from-ajeudhzebocbwzbifebb>
   ```

8. **บันทึกไฟล์**

### ขั้นตอนที่ 3: ตรวจสอบอีกครั้ง

```bash
python verify_and_fix.py
```

ต้องเห็น:
- ✅ SUPABASE_SERVICE_ROLE_KEY: Correct (project: **ajeudhzebocbwzbifebb**)

### ขั้นตอนที่ 4: สร้าง User

```bash
python test_and_create_user.py
```

## วิธีตรวจสอบว่าเป็น Project ถูกต้อง

### วิธีที่ 1: ดูที่ URL
- ✅ ถูกต้อง: `https://supabase.com/dashboard/project/ajeudhzebocbwzbifebb/...`
- ❌ ผิด: `https://supabase.com/dashboard/project/zipuyqkqaktbaddsdrhc/...`

### วิธีที่ 2: ดูที่ Project URL ในหน้า Settings → API
- ✅ ถูกต้อง: `https://ajeudhzebocbwzbifebb.supabase.co`
- ❌ ผิด: `https://zipuyqkqaktbaddsdrhc.supabase.co`

### วิธีที่ 3: ตรวจสอบ Key หลังจาก Copy
```bash
python check_key.py
```

ต้องเห็น:
- Project Ref: **ajeudhzebocbwzbifebb** (ไม่ใช่ zipuyqkqaktbaddsdrhc)

## หมายเหตุ

- ⚠️ คุณอาจมีหลาย projects ใน Supabase
- ⚠️ ต้องเลือก project ที่ถูกต้อง (`ajeudhzebocbwzbifebb`)
- ✅ ตรวจสอบ URL ใน browser เสมอ
