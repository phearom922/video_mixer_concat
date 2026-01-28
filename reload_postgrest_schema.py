#!/usr/bin/env python3
"""
Script to reload PostgREST schema cache in Supabase.
This fixes the PGRST205 error: "Could not find the table in the schema cache"
"""
import os
import sys
from supabase import create_client

# Load environment variables
from dotenv import load_dotenv
load_dotenv('license_server/.env')

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    print("❌ Error: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in license_server/.env")
    sys.exit(1)

print("🔄 Reloading PostgREST schema cache...")
print(f"   Project: {SUPABASE_URL}")

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    
    # Execute NOTIFY command to reload schema
    result = supabase.rpc('exec_sql', {
        'query': "NOTIFY pgrst, 'reload schema';"
    }).execute()
    
    print("✅ Schema reload command sent")
    print("\n⏳ Waiting 5 seconds for PostgREST to reload...")
    
    import time
    time.sleep(5)
    
    # Test if it works
    print("\n🧪 Testing PostgREST connection...")
    try:
        response = supabase.table('licenses').select('id').limit(1).execute()
        print("✅ PostgREST is working! Tables are accessible.")
        print(f"   Response: {response.data}")
    except Exception as e:
        if 'PGRST205' in str(e):
            print("⚠️  Schema cache still not refreshed. Try:")
            print("   1. Go to Supabase Dashboard > SQL Editor")
            print("   2. Run: NOTIFY pgrst, 'reload schema';")
            print("   3. Wait 10-30 seconds")
            print("   4. Restart FastAPI server")
        else:
            print(f"❌ Error: {e}")
            
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n💡 Alternative: Go to Supabase Dashboard > SQL Editor")
    print("   and run: NOTIFY pgrst, 'reload schema';")
