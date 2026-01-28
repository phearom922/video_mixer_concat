#!/usr/bin/env python3
"""
Script to create admin user in Supabase with provided credentials.
"""
import sys
from pathlib import Path

try:
    from supabase import create_client, Client
except ImportError:
    print("Installing supabase-py...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "supabase", "-q"])
    from supabase import create_client, Client

# Configuration
SUPABASE_URL = "https://ajeudhzebocbwzbifebb.supabase.co"
ADMIN_EMAIL = "ronphearom056@gmail.com"
ADMIN_PASSWORD = "Phearom090790"

def get_service_role_key():
    """Get service role key from .env file."""
    env_path = Path("license_server/.env")
    if not env_path.exists():
        return None
    
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith("SUPABASE_SERVICE_ROLE_KEY="):
                key = line.split("=", 1)[1].strip()
                if key and key != "YOUR_SERVICE_ROLE_KEY_HERE":
                    return key
    return None

def main():
    print("=" * 60)
    print("Creating Admin User in Supabase")
    print("=" * 60)
    print()
    
    service_role_key = get_service_role_key()
    
    if not service_role_key:
        print("❌ Service Role Key not found!")
        print()
        print("Please add SUPABASE_SERVICE_ROLE_KEY to license_server/.env")
        print("Get it from: https://ajeudhzebocbwzbifebb.supabase.co → Settings → API")
        return
    
    print(f"📧 Email: {ADMIN_EMAIL}")
    print(f"🔑 Creating user...")
    print()
    
    # Create Supabase client with service role
    try:
        supabase: Client = create_client(SUPABASE_URL, service_role_key)
        
        # Check if user exists
        try:
            users = supabase.auth.admin.list_users()
            for user in users.users:
                if user.email == ADMIN_EMAIL:
                    print(f"✅ User already exists!")
                    print(f"   Email: {user.email}")
                    print(f"   User ID: {user.id}")
                    print(f"   Created: {user.created_at}")
                    return
        except Exception as e:
            print(f"⚠️  Could not check existing users: {e}")
            print("   Continuing with user creation...")
        
        # Create user
        result = supabase.auth.admin.create_user({
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD,
            "email_confirm": True  # Auto-confirm email
        })
        
        print(f"✅ User created successfully!")
        print(f"   Email: {result.user.email}")
        print(f"   User ID: {result.user.id}")
        print()
        print("You can now login to the admin dashboard!")
        print("   URL: http://localhost:3000")
        print(f"   Email: {ADMIN_EMAIL}")
        print(f"   Password: {ADMIN_PASSWORD}")
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Failed to create user: {error_msg}")
        print()
        
        if "already registered" in error_msg.lower() or "user already exists" in error_msg.lower():
            print("ℹ️  User might already exist. Trying to verify...")
            try:
                # Try to sign in to verify
                test_client = create_client(SUPABASE_URL, SUPABASE_URL.split("//")[1].split(".")[0])
                # This won't work with anon key for admin, but let's check differently
                print("   Please check Supabase Dashboard → Authentication → Users")
            except:
                pass
        else:
            print("Alternative: Create user manually in Supabase Dashboard:")
            print("  1. Go to https://ajeudhzebocbwzbifebb.supabase.co")
            print("  2. Authentication → Users")
            print("  3. Add user → Create new user")
            print(f"  4. Email: {ADMIN_EMAIL}")
            print(f"  5. Password: {ADMIN_PASSWORD}")

if __name__ == "__main__":
    main()
