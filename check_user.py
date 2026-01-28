#!/usr/bin/env python3
"""
Check if admin user exists and can login.
"""
import requests
from pathlib import Path

SUPABASE_URL = "https://zipuyqkqaktbaddsdrhc.supabase.co"
ADMIN_EMAIL = "ronphearom056@gmail.com"

def get_service_role_key():
    """Get service role key from .env file."""
    env_path = Path("license_server/.env")
    if not env_path.exists():
        return None
    
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith("SUPABASE_SERVICE_ROLE_KEY="):
                key = line.split("=", 1)[1].strip()
                key = key.strip('"').strip("'")
                if key and key != "YOUR_SERVICE_ROLE_KEY_HERE":
                    return key
    return None

def main():
    print("=" * 60)
    print("Checking Admin User")
    print("=" * 60)
    print()
    
    service_role_key = get_service_role_key()
    if not service_role_key:
        print("❌ Service Role Key not found!")
        return
    
    # List users
    url = f"{SUPABASE_URL}/auth/v1/admin/users"
    headers = {
        "apikey": service_role_key,
        "Authorization": f"Bearer {service_role_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            users = data.get('users', [])
            
            print(f"Found {len(users)} user(s) in the system")
            print()
            
            admin_user = None
            for user in users:
                if user.get('email') == ADMIN_EMAIL:
                    admin_user = user
                    break
            
            if admin_user:
                print(f"✅ Admin user found!")
                print(f"   Email: {admin_user.get('email')}")
                print(f"   User ID: {admin_user.get('id')}")
                print(f"   Created: {admin_user.get('created_at', 'N/A')}")
                print(f"   Email Confirmed: {admin_user.get('email_confirmed_at') is not None}")
                print()
                print("You can now login to the admin dashboard!")
                print("   URL: http://localhost:3000")
                print(f"   Email: {ADMIN_EMAIL}")
                print(f"   Password: Phearom090790")
            else:
                print(f"❌ Admin user not found: {ADMIN_EMAIL}")
                print()
                print("Available users:")
                for user in users:
                    print(f"   - {user.get('email')}")
        else:
            print(f"❌ Failed to list users (Status: {response.status_code})")
            print(f"   Response: {response.text[:200]}")
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
