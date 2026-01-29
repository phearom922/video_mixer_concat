# คู่มือการส่งไฟล์ให้ลูกค้า (Distribution Guide)

เอกสารนี้อธิบายกระบวนการส่งไฟล์แอปพลิเคชันให้ลูกค้าตั้งแต่การ build, package, upload จนถึงการติดตั้งและใช้งาน

## ส่วนที่ 1: สำหรับ Admin

### ขั้นตอนที่ 1: เตรียม Build Desktop App

#### 1.1 อัพเดทเวอร์ชั่นในโค้ด

1. เปิดไฟล์ `desktop_app/app/__init__.py`
2. แก้ไข `APP_VERSION` เป็นเวอร์ชั่นใหม่ (เช่น `"2.0.0"`)
   ```python
   APP_VERSION = "2.0.0"
   ```
3. บันทึกไฟล์

#### 1.2 Build Executable ด้วย PyInstaller

1. เปิด Command Prompt หรือ PowerShell
2. ไปที่โฟลเดอร์ `desktop_app`:
   ```bash
   cd desktop_app
   ```

3. ติดตั้ง PyInstaller (ถ้ายังไม่ได้ติดตั้ง):
   ```bash
   pip install pyinstaller
   ```

4. Build executable:
   
   **วิธีที่ 1**: ใช้คำสั่ง `pyinstaller` (ถ้าอยู่ใน PATH):
   ```bash
   pyinstaller pyinstaller.spec
   ```
   
   **วิธีที่ 2**: ใช้ `python -m PyInstaller` (แนะนำสำหรับ Windows):
   ```bash
   python -m PyInstaller pyinstaller.spec
   ```
   
   > **หมายเหตุ**: ถ้าเห็น warning ว่า scripts ไม่อยู่ใน PATH ให้ใช้วิธีที่ 2 แทน

5. รอให้ build เสร็จ (อาจใช้เวลาหลายนาที)
6. ไฟล์ executable จะอยู่ที่ `desktop_app/dist/VideoMixerConcat.exe`

#### 1.3 ทดสอบ Executable

1. เปิดไฟล์ `dist/VideoMixerConcat.exe` เพื่อทดสอบ
2. ตรวจสอบว่า:
   - แอปเปิดได้ปกติ
   - License activation ทำงานได้
   - ฟีเจอร์หลักทำงานได้
3. ถ้ามีปัญหา ให้แก้ไขและ build ใหม่

#### 1.4 ตั้งชื่อไฟล์ตามเวอร์ชั่น (แนะนำ)

1. เปลี่ยนชื่อไฟล์เป็น `VideoMixerConcat-v2.0.0.exe` (หรือชื่อที่เหมาะสม)
2. เก็บไฟล์ไว้ในโฟลเดอร์ที่เข้าถึงได้ง่าย

### ขั้นตอนที่ 2: อัพโหลดไฟล์ไปยัง Hosting

เลือกวิธีใดวิธีหนึ่ง:

#### วิธีที่ 1: GitHub Releases (แนะนำ)

1. ไปที่ GitHub repository ของคุณ
2. คลิก **"Releases"** → **"Create a new release"**
3. กรอกข้อมูล:
   - **Tag version**: `v2.0.0` (ต้องตรงกับ APP_VERSION)
   - **Release title**: `VideoMixerConcat v2.0.0`
   - **Description**: ใส่ Release Notes
4. อัพโหลดไฟล์ `VideoMixerConcat-v2.0.0.exe` ในส่วน **"Attach binaries"**
5. คลิก **"Publish release"**
6. คัดลอก **Direct download URL** (เช่น `https://github.com/username/repo/releases/download/v2.0.0/VideoMixerConcat-v2.0.0.exe`)

#### วิธีที่ 2: Google Drive

1. อัพโหลดไฟล์ไปยัง Google Drive
2. คลิกขวาที่ไฟล์ → **"Get link"** → เลือก **"Anyone with the link"**
3. คัดลอก link
4. แปลงเป็น Direct download URL:
   - เปลี่ยนจาก `https://drive.google.com/file/d/FILE_ID/view?usp=sharing`
   - เป็น `https://drive.google.com/uc?export=download&id=FILE_ID`
   - (FILE_ID คือ ID ที่อยู่ใน URL เดิม)

#### วิธีที่ 3: Server ของคุณเอง

1. อัพโหลดไฟล์ไปยัง web server
2. เก็บ URL เช่น `https://yourdomain.com/downloads/VideoMixerConcat-v2.0.0.exe`
3. ตรวจสอบว่า URL สามารถดาวน์โหลดได้โดยตรง

#### วิธีที่ 4: Cloud Storage อื่นๆ

- **Dropbox**: ใช้ Public link
- **OneDrive**: ใช้ Direct download link
- **AWS S3**: ใช้ Public URL
- **อื่นๆ**: ตรวจสอบว่า URL เป็น Direct download link

### ขั้นตอนที่ 3: สร้าง Release ใน Admin Dashboard

#### 3.1 เข้าสู่ระบบ Admin Dashboard

1. เปิดเบราว์เซอร์ไปที่ Admin Dashboard (เช่น `http://localhost:3000`)
2. Login ด้วยบัญชี Admin

#### 3.2 ไปที่หน้า Releases

1. คลิกที่เมนู **"Releases"** ใน Sidebar

#### 3.3 สร้าง Release ใหม่

1. คลิกปุ่ม **"Create Release"**
2. กรอกข้อมูลในฟอร์ม:
   - **Platform**: เลือก `windows`
   - **Version**: ใส่เวอร์ชั่นใหม่ (เช่น `2.0.0`)
     - ⚠️ **สำคัญ**: ต้องตรงกับ `APP_VERSION` ในโค้ด
     - ใช้รูปแบบ SemVer: `MAJOR.MINOR.PATCH`
   - **Download URL**: วาง URL ที่ได้จากขั้นตอนที่ 2
     - ตัวอย่าง: `https://github.com/username/repo/releases/download/v2.0.0/VideoMixerConcat-v2.0.0.exe`
   - **Release Notes**: ใส่รายละเอียดการเปลี่ยนแปลง
     - ตัวอย่าง:
       ```
       Version 2.0.0
       
       New Features:
       - เพิ่ม Dark Mode theme
       - เพิ่ม Sidebar ใน Admin Dashboard
       - ปรับปรุง UI/UX
       
       Bug Fixes:
       - แก้ไขปัญหา timezone ใน license expiration
       - แก้ไขปัญหา infinite loop ใน license detail page
       ```
   - **Set as latest release**: ✅ ติ๊กถูกเพื่อตั้งเป็นเวอร์ชั่นล่าสุด
3. คลิกปุ่ม **"Save"**

#### 3.4 ตรวจสอบ Release

1. ตรวจสอบว่า Release ถูกสร้างแล้วในตาราง
2. ตรวจสอบว่า **"LATEST"** column แสดง **"Latest"** tag (สีเขียว)
3. ถ้ายังไม่เป็น Latest:
   - คลิกปุ่ม **"Set Latest"** ในคอลัมน์ Actions

### ขั้นตอนที่ 4: ทดสอบการแจ้งเตือนอัพเดท

#### 4.1 ทดสอบด้วย Desktop App เวอร์ชั่นเก่า

1. เปิด Desktop App เวอร์ชั่นเก่า (เช่น v1.0.0)
2. ตรวจสอบว่า:
   - แอปแสดง Update Dialog
   - แสดงเวอร์ชั่นใหม่ (2.0.0)
   - แสดง Release Notes
   - ปุ่ม Download ทำงานได้

#### 4.2 ตรวจสอบ Log (ถ้าจำเป็น)

1. ตรวจสอบ log ใน Desktop App:
   - ไปที่ `%APPDATA%\VideoMixerConcat\logs\`
   - เปิดไฟล์ log ล่าสุด
   - ตรวจสอบว่ามี log "Checking for updates" และ "Update available"

### ขั้นตอนที่ 5: แจ้งลูกค้า (ถ้าจำเป็น)

ถ้าต้องการแจ้งลูกค้าโดยตรง:

1. ส่งอีเมลหรือข้อความแจ้งว่ามีเวอร์ชั่นใหม่
2. แนบ Release Notes
3. แจ้งว่าแอปจะแจ้งเตือนอัตโนมัติเมื่อเปิดแอป

---

## ส่วนที่ 2: สำหรับ User (ลูกค้า)

### ขั้นตอนที่ 1: รับการแจ้งเตือนอัพเดท

#### 1.1 การแจ้งเตือนอัตโนมัติ

- Desktop App จะตรวจสอบอัพเดทอัตโนมัติ:
  - **เมื่อเปิดแอปครั้งแรก** (หลังจาก 12 ชั่วโมง)
  - **ทุก 12 ชั่วโมง** หลังจากเปิดแอป
- ถ้ามีเวอร์ชั่นใหม่ จะแสดง **Update Dialog** อัตโนมัติ

#### 1.2 Update Dialog

Dialog จะแสดง:

- **Version**: เวอร์ชั่นใหม่ (เช่น `2.0.0`)
- **Release Notes**: รายละเอียดการเปลี่ยนแปลง
- **ปุ่ม Download**: เปิด URL ดาวน์โหลดในเบราว์เซอร์
- **ปุ่ม Later**: ปิด dialog (จะแจ้งอีกครั้งใน 12 ชั่วโมง)
- **ปุ่ม Skip This Version**: ข้ามเวอร์ชั่นนี้ (จะไม่แจ้งอีก)

### ขั้นตอนที่ 2: ดาวน์โหลดไฟล์

#### 2.1 คลิกปุ่ม Download

1. ใน Update Dialog คลิกปุ่ม **"Download"**
2. เบราว์เซอร์จะเปิดไปที่ Download URL อัตโนมัติ

#### 2.2 ดาวน์โหลดไฟล์

1. ไฟล์จะเริ่มดาวน์โหลดอัตโนมัติ
2. รอให้ดาวน์โหลดเสร็จ
3. ไฟล์จะถูกบันทึกที่โฟลเดอร์ Downloads (หรือตามที่ตั้งค่าในเบราว์เซอร์)

### ขั้นตอนที่ 3: ติดตั้งเวอร์ชั่นใหม่

#### 3.1 ปิดแอปเวอร์ชั่นเก่า (ถ้ายังเปิดอยู่)

1. ปิด Desktop App เวอร์ชั่นเก่าทั้งหมด
2. ตรวจสอบว่าไม่มี process ทำงานอยู่

#### 3.2 ติดตั้งเวอร์ชั่นใหม่

1. เปิดไฟล์ที่ดาวน์โหลดมา (เช่น `VideoMixerConcat-v2.0.0.exe`)
2. ถ้ามี Windows Defender SmartScreen warning:
   - คลิก **"More info"**
   - คลิก **"Run anyway"** (ถ้าแน่ใจว่าไฟล์ปลอดภัย)
3. ติดตั้งทับเวอร์ชั่นเก่า:
   - ไฟล์จะถูกแทนที่อัตโนมัติ
   - หรือติดตั้งในโฟลเดอร์เดิม

#### 3.3 เปิดแอปเวอร์ชั่นใหม่

1. เปิด Desktop App ใหม่
2. ตรวจสอบว่า:
   - แอปเปิดได้ปกติ
   - แสดงเวอร์ชั่นใหม่ใน title bar
   - License ยังใช้งานได้ (ถ้าเป็น update)
   - ฟีเจอร์หลักทำงานได้

### ขั้นตอนที่ 4: เปิดใช้งาน (สำหรับการติดตั้งครั้งแรก)

#### 4.1 เปิดแอปครั้งแรก

1. เปิด Desktop App
2. จะแสดง **Activation Window** อัตโนมัติ

#### 4.2 ใส่ License Key

1. ใส่ **License Key** ที่ได้รับจาก Admin
2. (Optional) ใส่ **Device Label** (เช่น "Office-PC-1")
3. คลิกปุ่ม **"Activate License"**

#### 4.3 ตรวจสอบการ Activate

1. ถ้าสำเร็จ จะแสดงข้อความ "Activation successful"
2. แอปจะเปิด Main Window
3. ตรวจสอบว่า License Status แสดง "Active"

---

## Troubleshooting

### สำหรับ Admin

#### ปัญหา: Build ไม่สำเร็จ

**สาเหตุที่เป็นไปได้**:

- PyInstaller ไม่ได้ติดตั้ง
- Python version ไม่ถูกต้อง
- Dependencies ไม่ครบ

**วิธีแก้ไข**:

1. ตรวจสอบ Python version: `python --version` (ต้องเป็น 3.11+)
2. ติดตั้ง dependencies: `pip install -r requirements.txt`
3. ติดตั้ง PyInstaller: `pip install pyinstaller`
4. ถ้า `pyinstaller` command ไม่ทำงาน ให้ใช้ `python -m PyInstaller` แทน:
   ```bash
   python -m PyInstaller pyinstaller.spec
   ```
5. ลอง build ใหม่

#### ปัญหา: Executable ไม่ทำงาน

**สาเหตุที่เป็นไปได้**:

- Build ไม่สมบูรณ์
- Missing dependencies
- Path issues

**วิธีแก้ไข**:

1. ตรวจสอบ log ใน console (ถ้า build ด้วย `console=True`)
2. ทดสอบด้วย `python -m app.main` ก่อน
3. ตรวจสอบว่าไฟล์ assets ถูก include ครบ

#### ปัญหา: Download URL ไม่ทำงาน

**สาเหตุที่เป็นไปได้**:

- URL ผิดพลาด
- ไฟล์ถูกลบหรือย้าย
- Server ไม่สามารถเข้าถึงได้

**วิธีแก้ไข**:

1. ทดสอบ URL ในเบราว์เซอร์ก่อน
2. ตรวจสอบว่าไฟล์ยังอยู่ที่เดิม
3. แก้ไข URL ใน Admin Dashboard:
   - ไปที่ Releases → คลิก "Edit" → แก้ไข Download URL → คลิก "Update"

#### ปัญหา: User ไม่ได้รับแจ้งเตือน

**สาเหตุที่เป็นไปได้**:

- Release ยังไม่ได้ตั้งเป็น Latest
- เวอร์ชั่นใหม่ไม่ใหม่กว่าเวอร์ชั่นปัจจุบัน
- ยังไม่ครบ 12 ชั่วโมง

**วิธีแก้ไข**:

1. ตรวจสอบว่า Release ตั้งเป็น Latest แล้ว
2. ตรวจสอบว่า Version ใหม่กว่าเวอร์ชั่นปัจจุบันจริงๆ
3. รอให้ครบ 12 ชั่วโมง หรือบังคับตรวจสอบอัพเดท

### สำหรับ User

#### ปัญหา: ไม่ได้รับแจ้งเตือนอัพเดท

**สาเหตุที่เป็นไปได้**:

- ยังไม่ครบ 12 ชั่วโมง
- ข้ามเวอร์ชั่นนี้ไปแล้ว
- ไม่มี internet connection

**วิธีแก้ไข**:

1. รอให้ครบ 12 ชั่วโมง
2. ตรวจสอบ internet connection
3. เปิดแอปใหม่ (จะตรวจสอบอัพเดทอัตโนมัติ)

#### ปัญหา: ดาวน์โหลดไม่สำเร็จ

**สาเหตุที่เป็นไปได้**:

- URL ไม่ถูกต้อง
- Server ไม่สามารถเข้าถึงได้
- ไฟล์ถูกลบ

**วิธีแก้ไข**:

1. ตรวจสอบ internet connection
2. ลองดาวน์โหลดใหม่
3. ติดต่อ Admin เพื่อตรวจสอบ URL

#### ปัญหา: ติดตั้งไม่สำเร็จ

**สาเหตุที่เป็นไปได้**:

- ไฟล์เสียหาย
- ไม่มีสิทธิ์เขียนไฟล์
- Antivirus block

**วิธีแก้ไข**:

1. ดาวน์โหลดไฟล์ใหม่
2. ตรวจสอบสิทธิ์ในโฟลเดอร์ติดตั้ง
3. ปิด Antivirus ชั่วคราว (ถ้าจำเป็น)
4. Run as Administrator

#### ปัญหา: License ไม่ทำงานหลังอัพเดท

**สาเหตุที่เป็นไปได้**:

- License หมดอายุ
- Activation token ถูก clear

**วิธีแก้ไข**:

1. ตรวจสอบ License Status ในแอป
2. Activate ใหม่ด้วย License Key เดิม
3. ติดต่อ Admin ถ้ายังไม่ได้

---

## Checklist สำหรับ Admin

ก่อนส่งไฟล์ให้ลูกค้า ตรวจสอบ:

- [ ] อัพเดท `APP_VERSION` ในโค้ดแล้ว
- [ ] Build executable สำเร็จแล้ว
- [ ] ทดสอบ executable แล้ว (เปิดได้, ทำงานได้)
- [ ] อัพโหลดไฟล์ไปยัง hosting แล้ว
- [ ] ทดสอบ Download URL แล้ว (ดาวน์โหลดได้)
- [ ] สร้าง Release ใน Admin Dashboard แล้ว
- [ ] ตั้ง Release เป็น Latest แล้ว
- [ ] ทดสอบการแจ้งเตือนอัพเดทแล้ว (ด้วยเวอร์ชั่นเก่า)
- [ ] Release Notes ถูกต้องและครบถ้วน

---

## Checklist สำหรับ User

ก่อนติดตั้งเวอร์ชั่นใหม่ ตรวจสอบ:

- [ ] ได้รับการแจ้งเตือนอัพเดทแล้ว
- [ ] ดาวน์โหลดไฟล์สำเร็จแล้ว
- [ ] ตรวจสอบไฟล์ว่าเป็นเวอร์ชั่นที่ถูกต้อง
- [ ] ปิดแอปเวอร์ชั่นเก่าแล้ว
- [ ] มี License Key (สำหรับการติดตั้งครั้งแรก)
- [ ] มี internet connection (สำหรับ activation)

---

## ข้อมูลเพิ่มเติม

- **SemVer Specification**: https://semver.org/
- **Admin Dashboard**: `http://localhost:3000/releases`
- **API Documentation**: ดูที่ `license_server/app/routers/admin.py` และ `license_server/app/routers/public.py`
- **Update Version Guide**: ดูที่ `UPDATE_VERSION_GUIDE.md`
