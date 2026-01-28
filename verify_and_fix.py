#!/usr/bin/env python3
"""
Verify project configuration and help fix key issues.
"""
import base64
import json
from pathlib import Path

CORRECT_PROJECT_REF = "zipuyqkqaktbaddsdrhc"
CORRECT_SUPABASE_URL = "https://zipuyqkqaktbaddsdrhc.supabase.co"

def decode_jwt_payload(token):
    """Decode JWT payload without verification."""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
        payload = parts[1]
        padding = 4 - len(payload) % 4
        if padding != 4:
            payload += '=' * padding
        decoded = base64.urlsafe_b64decode(payload)
        return json.loads(decoded)
    except:
        return None

def check_license_server_env():
    """Check license_server/.env"""
    env_path = Path("license_server/.env")
    if not env_path.exists():
        print("❌ license_server/.env not found")
        return False
    
    print("=" * 60)
    print("Checking license_server/.env")
    print("=" * 60)
    
    with open(env_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
        
        url_ok = False
        key_ok = False
        key_ref = None
        
        for line in lines:
            if line.startswith("SUPABASE_URL="):
                url = line.split("=", 1)[1].strip()
                if CORRECT_SUPABASE_URL in url:
                    print(f"✅ SUPABASE_URL: {url}")
                    url_ok = True
                else:
                    print(f"❌ SUPABASE_URL: {url}")
                    print(f"   Expected: {CORRECT_SUPABASE_URL}")
            
            if line.startswith("SUPABASE_SERVICE_ROLE_KEY="):
                key = line.split("=", 1)[1].strip()
                key = key.strip('"').strip("'")
                if key and key != "YOUR_SERVICE_ROLE_KEY_HERE":
                    payload = decode_jwt_payload(key)
                    if payload:
                        key_ref = payload.get('ref')
                        role = payload.get('role')
                        if role == 'service_role' and key_ref == CORRECT_PROJECT_REF:
                            print(f"✅ SUPABASE_SERVICE_ROLE_KEY: Correct (project: {key_ref})")
                            key_ok = True
                        else:
                            print(f"❌ SUPABASE_SERVICE_ROLE_KEY: Wrong project!")
                            print(f"   Current project ref: {key_ref}")
                            print(f"   Expected project ref: {CORRECT_PROJECT_REF}")
                            print(f"   Role: {role}")
                    else:
                        print(f"❌ SUPABASE_SERVICE_ROLE_KEY: Invalid JWT format")
                else:
                    print(f"❌ SUPABASE_SERVICE_ROLE_KEY: Not set")
        
        print()
        if url_ok and key_ok:
            print("✅ license_server/.env is correct!")
            return True
        else:
            print("❌ license_server/.env needs fixing")
            if not key_ok:
                print()
                print("To fix:")
                print(f"  1. Go to {CORRECT_SUPABASE_URL}")
                print("  2. Settings → API")
                print("  3. Tab: 'Legacy anon, service_role API keys'")
                print("  4. Click 'Reveal' on service_role secret key")
                print(f"  5. Copy the key (must be from project: {CORRECT_PROJECT_REF})")
                print("  6. Update license_server/.env")
            return False

def check_admin_dashboard_env():
    """Check admin_dashboard/.env.local"""
    env_path = Path("admin_dashboard/.env.local")
    if not env_path.exists():
        print("❌ admin_dashboard/.env.local not found")
        return False
    
    print()
    print("=" * 60)
    print("Checking admin_dashboard/.env.local")
    print("=" * 60)
    
    with open(env_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
        
        url_ok = False
        key_ok = False
        key_ref = None
        
        for line in lines:
            if line.startswith("NEXT_PUBLIC_SUPABASE_URL="):
                url = line.split("=", 1)[1].strip()
                if CORRECT_SUPABASE_URL in url:
                    print(f"✅ NEXT_PUBLIC_SUPABASE_URL: {url}")
                    url_ok = True
                else:
                    print(f"❌ NEXT_PUBLIC_SUPABASE_URL: {url}")
            
            if line.startswith("NEXT_PUBLIC_SUPABASE_ANON_KEY="):
                key = line.split("=", 1)[1].strip()
                key = key.strip('"').strip("'")
                if key:
                    payload = decode_jwt_payload(key)
                    if payload:
                        key_ref = payload.get('ref')
                        role = payload.get('role')
                        if key_ref == CORRECT_PROJECT_REF:
                            print(f"✅ NEXT_PUBLIC_SUPABASE_ANON_KEY: Correct (project: {key_ref}, role: {role})")
                            key_ok = True
                        else:
                            print(f"❌ NEXT_PUBLIC_SUPABASE_ANON_KEY: Wrong project!")
                            print(f"   Current project ref: {key_ref}")
                            print(f"   Expected project ref: {CORRECT_PROJECT_REF}")
                    else:
                        print(f"❌ NEXT_PUBLIC_SUPABASE_ANON_KEY: Invalid JWT format")
                else:
                    print(f"❌ NEXT_PUBLIC_SUPABASE_ANON_KEY: Not set")
        
        print()
        if url_ok and key_ok:
            print("✅ admin_dashboard/.env.local is correct!")
            return True
        else:
            print("❌ admin_dashboard/.env.local needs fixing")
            if not key_ok:
                print()
                print("To fix:")
                print(f"  1. Go to {CORRECT_SUPABASE_URL}")
                print("  2. Settings → API")
                print("  3. Copy the 'anon public' key (not service_role)")
                print(f"  4. Update admin_dashboard/.env.local")
            return False

def main():
    print("=" * 60)
    print("Project Configuration Verification")
    print("=" * 60)
    print()
    print(f"Correct Project: {CORRECT_PROJECT_REF}")
    print(f"Correct URL: {CORRECT_SUPABASE_URL}")
    print()
    
    server_ok = check_license_server_env()
    dashboard_ok = check_admin_dashboard_env()
    
    print()
    print("=" * 60)
    if server_ok and dashboard_ok:
        print("✅ All configuration files are correct!")
        print()
        print("You can now run:")
        print("  python test_and_create_user.py")
    else:
        print("❌ Configuration needs fixing")
        print()
        print("Please fix the issues above and run this script again.")

if __name__ == "__main__":
    main()
