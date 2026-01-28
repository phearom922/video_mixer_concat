#!/usr/bin/env python3
"""
Test Service Role Key and create user.
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
                # Remove quotes if present
                key = key.strip('"').strip("'")
                if key and key != "YOUR_SERVICE_ROLE_KEY_HERE":
                    return key
    return None

def main():
    print("=" * 60)
    print("Testing Service Role Key and Creating User")
    print("=" * 60)
    print()
    
    service_role_key = get_service_role_key()
    
    if not service_role_key:
        print("❌ Service Role Key not found!")
        return
    
    print(f"✅ Service Role Key found")
    print(f"   Key length: {len(service_role_key)} characters")
    print(f"   Key starts with: {service_role_key[:20]}...")
    print()
    
    # Test the key by checking users
    print("🔍 Testing Service Role Key...")
    test_url = f"{SUPABASE_URL}/auth/v1/admin/users"
    headers = {
        "apikey": service_role_key,
        "Authorization": f"Bearer {service_role_key}",
        "Content-Type": "application/json"
    }
    
    try:
        # First, try to list users to test the key
        test_response = requests.get(test_url, headers=headers, timeout=10)
        
        if test_response.status_code == 200:
            print("✅ Service Role Key is valid!")
            users = test_response.json()
            print(f"   Found {len(users.get('users', []))} existing users")
            
            # Check if user already exists
            for user in users.get('users', []):
                if user.get('email') == ADMIN_EMAIL:
                    print()
                    print(f"ℹ️  User already exists: {ADMIN_EMAIL}")
                    print(f"   User ID: {user.get('id')}")
                    print()
                    print("You can login with:")
                    print(f"   Email: {ADMIN_EMAIL}")
                    print(f"   Password: {ADMIN_PASSWORD}")
                    return
            
            print()
            print(f"📧 Creating new user: {ADMIN_EMAIL}")
            
        elif test_response.status_code == 401:
            print("❌ Service Role Key is invalid!")
            print()
            print("Please check:")
            print("  1. The key is correct (copy from Supabase Dashboard)")
            print("  2. The key is the 'service_role' key, not 'anon' key")
            print("  3. There are no extra spaces or quotes in the .env file")
            print()
            print(f"   Current key (first 50 chars): {service_role_key[:50]}...")
            return
        else:
            print(f"⚠️  Unexpected status: {test_response.status_code}")
            print(f"   Response: {test_response.text[:200]}")
            print()
            print("Trying to create user anyway...")
    
    except Exception as e:
        print(f"⚠️  Error testing key: {e}")
        print("Trying to create user anyway...")
    
    # Create user
    print()
    print(f"🔑 Creating user...")
    create_url = f"{SUPABASE_URL}/auth/v1/admin/users"
    payload = {
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD,
        "email_confirm": True,
        "user_metadata": {}
    }
    
    try:
        response = requests.post(create_url, json=payload, headers=headers, timeout=10)
        
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
                if 'msg' in error_data:
                    print(f"   Details: {error_data.get('msg')}")
        
        else:
            print(f"❌ Failed to create user (Status: {response.status_code})")
            try:
                error_data = response.json()
                print(f"   Error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"   Response: {response.text[:500]}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")

if __name__ == "__main__":
    main()
