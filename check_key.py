#!/usr/bin/env python3
"""
Check if the key is a service_role key by decoding JWT.
"""
import base64
import json
from pathlib import Path

def decode_jwt_payload(token):
    """Decode JWT payload without verification."""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
        
        # Decode payload (second part)
        payload = parts[1]
        # Add padding if needed
        padding = 4 - len(payload) % 4
        if padding != 4:
            payload += '=' * padding
        
        decoded = base64.urlsafe_b64decode(payload)
        return json.loads(decoded)
    except Exception as e:
        return None

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
    key = get_service_role_key()
    if not key:
        print("❌ Key not found")
        return
    
    print("=" * 60)
    print("Analyzing Service Role Key")
    print("=" * 60)
    print()
    print(f"Key length: {len(key)} characters")
    print()
    
    payload = decode_jwt_payload(key)
    if payload:
        print("JWT Payload:")
        print(json.dumps(payload, indent=2))
        print()
        
        role = payload.get('role', 'unknown')
        ref = payload.get('ref', 'unknown')
        
        print(f"Role: {role}")
        print(f"Project Ref: {ref}")
        print()
        
        if role == 'service_role':
            print("✅ This IS a service_role key")
        else:
            print(f"❌ This is NOT a service_role key (role: {role})")
            print("   Please copy the 'service_role' key from Supabase Dashboard")
    else:
        print("❌ Could not decode JWT")
        print("   Key might be invalid or corrupted")

if __name__ == "__main__":
    main()
