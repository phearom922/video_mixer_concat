# คู่มือตั้งค่าแบบเร็ว (Quick Setup Guide)

## ✅ สิ่งที่ทำแล้ว

1. ✅ SQL Migration รันสำเร็จ - ตารางทั้งหมดถูกสร้างแล้ว
2. ✅ ไฟล์ `.env` ถูกสร้างแล้วสำหรับ:
   - `license_server/.env`
   - `admin_dashboard/.env.local`

## ⚠️ สิ่งที่ต้องทำต่อ

### ขั้นตอนที่ 1: เพิ่ม Service Role Key

**สำคัญมาก!** ต้องเพิ่ม Service Role Key ก่อนสร้าง user

1. ไปที่ Supabase Dashboard:
   https://ajeudhzebocbwzbifebb.supabase.co

2. ไปที่ Settings → API

3. หา **service_role** key (⚠️ อย่าเปิดเผย key นี้!)

4. เปิดไฟล์ `license_server/.env`

5. แทนที่บรรทัดนี้:
   ```
   SUPABASE_SERVICE_ROLE_KEY=YOUR_SERVICE_ROLE_KEY_HERE
   ```
   
   ด้วย:
   ```
   SUPABASE_SERVICE_ROLE_KEY=your-actual-service-role-key-here
   ```

### ขั้นตอนที่ 2: สร้าง Admin User

หลังจากเพิ่ม Service Role Key แล้ว รัน:

```bash
python create_user_direct.py
```

หรือสร้าง user ผ่าน Dashboard:

1. ไปที่ https://ajeudhzebocbwzbifebb.supabase.co
2. **Authentication** → **Users**
3. คลิก **"Add user"** → **"Create new user"**
4. ใส่ข้อมูล:
   - **Email**: `ronphearom056@gmail.com`
   - **Password**: `Phearom090790`
   - ✅ **Auto Confirm User** (เลือก checkbox)
5. คลิก **"Create user"**

### ขั้นตอนที่ 3: ทดสอบระบบ

#### 1. รัน FastAPI License Server

```bash
cd license_server
pip install -r requirements.txt
uvicorn app.main:app --reload
```

ตรวจสอบ: เปิด http://localhost:8000/docs

#### 2. รัน Next.js Admin Dashboard

```bash
cd admin_dashboard
npm install
npm run dev
```

ตรวจสอบ: เปิด http://localhost:3000 และ login ด้วย:
- Email: `ronphearom056@gmail.com`
- Password: `Phearom090790`

#### 3. ทดสอบ Desktop App

```bash
cd desktop_app
pip install -r requirements.txt
python -m app.main
```

## สรุปข้อมูลที่ตั้งค่าแล้ว

- **Supabase URL**: `https://ajeudhzebocbwzbifebb.supabase.co`
- **Admin Email**: `ronphearom056@gmail.com`
- **Admin Password**: `Phearom090790`
- **JWT Secret**: `2dp-y1XYn7kfm3cnWNEFUTPHLq8vbvCr-iOvdkv0C6o`

## หมายเหตุ

- ⚠️ Service Role Key ต้องเก็บเป็นความลับ อย่า commit ลง git
- ⚠️ ตรวจสอบว่า `.env` และ `.env.local` อยู่ใน `.gitignore`
- ✅ Email ตั้งค่าแล้วในทั้ง FastAPI และ Next.js config
