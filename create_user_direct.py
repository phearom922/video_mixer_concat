#!/usr/bin/env python3
"""
Create admin user in Supabase using Admin API directly.
"""
import json
import requests
from pathlib import Path

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
    print(f"🔑 Creating user via Supabase Admin API...")
    print()
    
    # Use Supabase Admin API
    url = f"{SUPABASE_URL}/auth/v1/admin/users"
    headers = {
        "apikey": service_role_key,
        "Authorization": f"Bearer {service_role_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD,
        "email_confirm": True,
        "user_metadata": {}
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ User created successfully!")
            print(f"   Email: {user_data.get('email', ADMIN_EMAIL)}")
            print(f"   User ID: {user_data.get('id', 'N/A')}")
            print()
            print("You can now login to the admin dashboard!")
            print("   URL: http://localhost:3000")
            print(f"   Email: {ADMIN_EMAIL}")
            print(f"   Password: {ADMIN_PASSWORD}")
        
        elif response.status_code == 422:
            error_data = response.json()
            error_msg = error_data.get('message', 'Unknown error')
            
            if 'already registered' in error_msg.lower() or 'already exists' in error_msg.lower():
                print(f"ℹ️  User already exists: {ADMIN_EMAIL}")
                print()
                print("You can login with:")
                print(f"   Email: {ADMIN_EMAIL}")
                print(f"   Password: {ADMIN_PASSWORD}")
            else:
                print(f"❌ Error: {error_msg}")
                print(f"   Response: {json.dumps(error_data, indent=2)}")
        
        else:
            print(f"❌ Failed to create user (Status: {response.status_code})")
            try:
                error_data = response.json()
                print(f"   Error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"   Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        print()
        print("Alternative: Create user manually in Supabase Dashboard:")
        print("  1. Go to https://ajeudhzebocbwzbifebb.supabase.co")
        print("  2. Authentication → Users")
        print("  3. Add user → Create new user")
        print(f"  4. Email: {ADMIN_EMAIL}")
        print(f"  5. Password: {ADMIN_PASSWORD}")

if __name__ == "__main__":
    main()
