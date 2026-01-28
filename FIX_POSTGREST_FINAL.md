# Fix PostgREST Schema Cache - Final Solution

## Problem
PostgREST schema cache ไม่ได้ refresh หลังจากสร้างตารางใหม่ ทำให้เกิด error:
```
Could not find the table 'public.licenses' in the schema cache (PGRST205)
```

## Root Cause
Supabase PostgREST ต้อง reload schema cache หลังจากสร้างตารางใหม่ แต่การ reload อาจใช้เวลาหรือต้องทำผ่าน Dashboard

## Solution Options

### Option 1: Manual Reload (Recommended)
1. ไปที่ **Supabase Dashboard**: https://supabase.com/dashboard/project/zipuyqkqaktbaddsdrhc
2. เปิด **SQL Editor**
3. รันคำสั่ง:
   ```sql
   NOTIFY pgrst, 'reload schema';
   ```
4. รอ **10-30 วินาที**
5. **Restart FastAPI server**:
   ```bash
   # หยุด server (Ctrl+C)
   cd license_server
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Option 2: Wait for Auto-Refresh
Supabase จะ auto-refresh schema cache ภายใน **5-10 นาที** หลังจากสร้างตารางใหม่

### Option 3: Use Supabase MCP
```python
mcp_supabase_execute_sql("NOTIFY pgrst, 'reload schema';")
```

## Verification

ทดสอบว่า PostgREST ทำงานแล้ว:
```bash
cd license_server
python -c "
from app.database import get_supabase_client
supabase = get_supabase_client()
response = supabase.table('licenses').select('id').limit(1).execute()
print('✅ Working!', response.data)
"
```

## Current Status

- ✅ Tables exist in database (`licenses`, `activations`, `admin_audit_logs`, `app_releases`)
- ✅ CORS configured for `localhost:3001`
- ⏳ PostgREST schema cache needs manual reload

## Next Steps

1. **Reload schema** ผ่าน Supabase Dashboard (Option 1)
2. **Restart FastAPI server**
3. **Refresh browser** ที่ `http://localhost:3001/licenses`
4. **Login** และทดสอบสร้าง license
