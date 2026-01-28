# ⚠️ URGENT: Restart FastAPI Server

## สิ่งที่แก้ไขแล้ว

✅ เพิ่ม error handling ให้ทุก function ที่ใช้ `supabase.table()`:
- `list_licenses` - Returns empty list `[]` on PGRST205
- `create_license` - Handles PGRST205 errors
- `get_license` - Returns 503 on PGRST205
- `get_license_activations` - Returns empty list on PGRST205
- `list_releases` - Returns empty list on PGRST205
- `log_admin_action` - Silently fails on PGRST205

## ⚠️ ต้องทำทันที

### Restart FastAPI Server

1. **หยุด server ปัจจุบัน:**
   - ไปที่ terminal ที่รัน FastAPI server
   - กด **Ctrl+C**

2. **รัน server ใหม่:**
   ```bash
   cd license_server
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **รอให้เห็น:**
   ```
   INFO:     Application startup complete.
   ```

## ผลลัพธ์ที่คาดหวัง

หลังจาก restart:
- ✅ Dashboard จะโหลดได้ (แม้จะไม่มี license list)
- ✅ ไม่มี 500 error
- ✅ CORS ทำงานถูกต้อง
- ✅ เมื่อ PostgREST schema refresh (5-10 นาที) ข้อมูลจะแสดงอัตโนมัติ

## หมายเหตุ

- Code ใหม่มี error handling แล้ว
- แต่ server ต้อง restart เพื่อให้ code ใหม่มีผล
- PostgREST schema cache จะ auto-refresh ภายใน 5-10 นาที
