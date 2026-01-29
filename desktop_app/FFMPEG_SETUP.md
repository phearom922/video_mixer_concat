# การ Setup FFmpeg สำหรับ Bundle

เอกสารนี้อธิบายวิธีการดาวน์โหลดและวาง FFmpeg เพื่อให้ bundle เข้าไปใน executable

## ขั้นตอนการ Setup

### 1. ดาวน์โหลด FFmpeg

1. ไปที่ https://www.gyan.dev/ffmpeg/builds/
2. ดาวน์โหลด **"ffmpeg-release-essentials.zip"** (หรือเวอร์ชั่นล่าสุด)
3. Extract ไฟล์ zip

### 2. วาง FFmpeg ในโปรเจค

1. สร้างโฟลเดอร์ `ffmpeg` ใน `desktop_app/` (ถ้ายังไม่มี)
2. Copy โฟลเดอร์ `bin` จาก FFmpeg ที่ extract มา ไปไว้ใน `desktop_app/ffmpeg/bin/`
3. โครงสร้างควรเป็น:
   ```
   desktop_app/
   ├── ffmpeg/
   │   └── bin/
   │       ├── ffmpeg.exe
   │       ├── ffprobe.exe
   │       └── ... (ไฟล์อื่นๆ ใน bin)
   ├── app/
   ├── pyinstaller.spec
   └── ...
   ```

### 3. ตรวจสอบ

ตรวจสอบว่าไฟล์ `desktop_app/ffmpeg/bin/ffmpeg.exe` มีอยู่จริง

### 4. Build

เมื่อ build ด้วย PyInstaller, FFmpeg จะถูก bundle เข้าไปใน executable อัตโนมัติ

## หมายเหตุ

- FFmpeg จะถูก extract ไปที่ temporary folder เมื่อรัน executable
- โค้ดจะหา FFmpeg จาก bundled location ก่อน แล้วค่อย fallback ไปหาใน PATH
- ถ้าไม่ต้องการ bundle FFmpeg สามารถลบโฟลเดอร์ `ffmpeg` ออกได้ (แอปจะหา FFmpeg จาก PATH แทน)
