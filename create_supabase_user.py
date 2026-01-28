#!/usr/bin/env python3
"""
Script to create admin user in Supabase.
Note: This requires Supabase service role key to create users.
"""
import sys
from pathlib import Path

try:
    from supabase import create_client, Client
except ImportError:
    print("❌ supabase-py not installed. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "supabase"])
    from supabase import create_client, Client

# Configuration
SUPABASE_URL = "https://ajeudhzebocbwzbifebb.supabase.co"
ADMIN_EMAIL = "ronphearom056@gmail.com"

def main():
    print("=" * 60)
    print("Create Admin User in Supabase")
    print("=" * 60)
    print()
    
    # Read service role key from .env
    env_path = Path("license_server/.env")
    if not env_path.exists():
        print("❌ license_server/.env not found!")
        print("   Please run create_admin_user.py first")
        return
    
    service_role_key = None
    with open(env_path, 'r') as f:
        for line in f:
            if line.startswith("SUPABASE_SERVICE_ROLE_KEY="):
                service_role_key = line.split("=", 1)[1].strip()
                break
    
    if not service_role_key or service_role_key == "YOUR_SERVICE_ROLE_KEY_HERE":
        print("❌ Service Role Key not found in license_server/.env")
        print()
        print("Please:")
        print("  1. Go to https://ajeudhzebocbwzbifebb.supabase.co")
        print("  2. Settings → API")
        print("  3. Copy the 'service_role' key")
        print("  4. Add it to license_server/.env as SUPABASE_SERVICE_ROLE_KEY")
        return
    
    print(f"📧 Creating user: {ADMIN_EMAIL}")
    print()
    
    # Create Supabase client with service role
    supabase: Client = create_client(SUPABASE_URL, service_role_key)
    
    # Check if user exists
    try:
        users = supabase.auth.admin.list_users()
        existing_user = None
        for user in users.users:
            if user.email == ADMIN_EMAIL:
                existing_user = user
                break
        
        if existing_user:
            print(f"✅ User already exists: {ADMIN_EMAIL}")
            print(f"   User ID: {existing_user.id}")
            return
    except Exception as e:
        print(f"⚠️  Could not check existing users: {e}")
    
    # Create user
    password = input("Enter password for admin user: ").strip()
    if not password:
        print("❌ Password cannot be empty")
        return
    
    try:
        result = supabase.auth.admin.create_user({
            "email": ADMIN_EMAIL,
            "password": password,
            "email_confirm": True  # Auto-confirm email
        })
        
        print(f"✅ User created successfully!")
        print(f"   Email: {ADMIN_EMAIL}")
        print(f"   User ID: {result.user.id}")
        print()
        print("You can now login to the admin dashboard with this email and password.")
        
    except Exception as e:
        print(f"❌ Failed to create user: {e}")
        print()
        print("Alternative: Create user manually in Supabase Dashboard:")
        print("  1. Go to https://ajeudhzebocbwzbifebb.supabase.co")
        print("  2. Authentication → Users")
        print("  3. Add user → Create new user")
        print(f"  4. Email: {ADMIN_EMAIL}")

if __name__ == "__main__":
    main()
