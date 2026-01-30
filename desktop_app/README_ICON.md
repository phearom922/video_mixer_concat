# คู่มือการสร้าง Icon สำหรับ Desktop App

## ปัญหาที่พบ

Icon ไม่ชัดหลังจาก build เพราะ:
1. **Pillow ไม่รองรับหลายขนาดใน ICO** - ICO file ที่สร้างมีเพียง 1 size
2. **Windows Cache Icon เก่า** - Windows อาจจะ cache icon เก่าไว้

## วิธีแก้ไข

### Option 1: ใช้ ICO Files ที่มีอยู่แล้ว (แนะนำ)

คุณมี ICO files หลายขนาดอยู่ใน `app/ui/assets/` แล้ว:
- `16x16.ico`
- `24x24.ico`
- `32x32.ico`
- `48x48.ico`
- `64x64.ico`
- `128x128.ico`
- `256x256.ico`

**ขั้นตอน:**
```bash
cd desktop_app
python combine_ico.py
clear_icon_cache.bat
./build.sh
```

### Option 2: ใช้ ImageMagick (คุณภาพดีที่สุด)

1. ติดตั้ง ImageMagick จาก https://imagemagick.org/script/download.php
2. รัน:
```bash
cd desktop_app
magick convert app/ui/assets/logo128x128.png -define icon:auto-resize=256,128,96,64,48,32,24,16 icon.ico
clear_icon_cache.bat
./build.sh
```

### Option 3: ใช้ Online Converter

1. ไปที่ https://convertio.co/png-ico/ หรือ https://icoconvert.com/
2. อัปโหลด `app/ui/assets/logo128x128.png`
3. เลือกหลายขนาด: 16, 24, 32, 48, 64, 128, 256
4. ดาวน์โหลด `icon.ico` มาแทนที่ไฟล์เดิม
5. Clear icon cache และ build ใหม่

## Clear Windows Icon Cache

**วิธีที่ 1: ใช้ Script (ง่ายที่สุด)**
```bash
cd desktop_app
clear_icon_cache.bat
```

**วิธีที่ 2: ทำเอง**
1. กด `Ctrl + Shift + Esc` → หา "Windows Explorer" → End task
2. กด `Win + R` → พิมพ์ `%LOCALAPPDATA%` → Enter
3. ลบไฟล์ `IconCache.db` และ `Microsoft\Windows\Explorer\iconcache*.db`
4. กลับไปที่ Task Manager → File → Run new task → พิมพ์ `explorer` → OK

**วิธีที่ 3: Restart Computer**
- Restart Windows จะ clear icon cache อัตโนมัติ

## ตรวจสอบ ICO File

```bash
cd desktop_app
python test_ico_sizes.py
```

**หมายเหตุ:** Pillow อาจจะอ่านได้เพียง 1 size แต่ Windows ควรจะอ่านได้หลายขนาด

## Build Script

Build script จะ:
1. ตรวจสอบว่ามี ICO files หลายขนาดหรือไม่
2. ถ้ามี → ใช้ `combine_ico.py` เพื่อรวม ICO files
3. ถ้าไม่มี → ใช้ `create_icon.py` เพื่อสร้างจาก PNG

```bash
cd desktop_app
./build.sh
```

หรือ

```bash
build.bat
```

## Troubleshooting

**ถ้า icon ยังไม่ชัด:**
1. ตรวจสอบว่า `icon.ico` มีหลายขนาด (ใช้ ImageMagick หรือ online tool)
2. Clear icon cache อีกครั้ง
3. Restart Computer
4. Build ใหม่

**ถ้า ICO file มีเพียง 1 size:**
- ใช้ ImageMagick หรือ Online Converter แทน Pillow
- Pillow ไม่รองรับการสร้าง ICO หลายขนาดอย่างถูกต้อง
