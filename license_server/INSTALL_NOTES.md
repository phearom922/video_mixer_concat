# Installation Notes

## Dependency Issues Resolved

The `pyroaring` package requires C++ compiler (Microsoft Visual C++ 14.0+), but it's only needed for `storage3` which we don't use in the license server.

### What was installed:
- ✅ FastAPI, Uvicorn, Pydantic (core dependencies)
- ✅ Supabase client (postgrest, auth, realtime)
- ✅ Python-JOSE, Passlib (security)
- ⚠️ storage3 and pyiceberg (installed but pyroaring dependency missing - not used)

### What's missing but not needed:
- ❌ pyroaring (only needed for storage3, which we don't use)

## Running the Server

The server should work fine even with the missing pyroaring dependency because:
1. We only use Supabase Postgrest (database queries)
2. We only use Supabase Auth (for admin JWT verification)
3. We don't use Storage functionality

To run:
```bash
cd license_server
uvicorn app.main:app --reload
```

If you encounter any import errors related to storage3, you can safely ignore them or install Microsoft Visual C++ Build Tools to compile pyroaring.
