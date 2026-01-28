#!/usr/bin/env python3
"""
Script to create admin user and environment files.
"""
from pathlib import Path

# Configuration
ADMIN_EMAIL = "ronphearom056@gmail.com"
SUPABASE_URL = "https://ajeudhzebocbwzbifebb.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFqZXVkaHplYm9jYnd6YmlmZWJiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njg3MjUxNjksImV4cCI6MjA4NDMwMTE2OX0.fHgr4gq5_Zv6Ry6kEjkV_eaHSkx0tt-AIpVkNCtAW7o"
JWT_SECRET = "2dp-y1XYn7kfm3cnWNEFUTPHLq8vbvCr-iOvdkv0C6o"

def create_license_server_env():
    """Create .env file for license server."""
    env_path = Path("license_server/.env")
    
    content = f"""# Supabase Configuration
SUPABASE_URL={SUPABASE_URL}
SUPABASE_SERVICE_ROLE_KEY=YOUR_SERVICE_ROLE_KEY_HERE

# JWT Configuration
JWT_SIGNING_SECRET={JWT_SECRET}
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=8760

# Device Hashing (optional)
DEVICE_HASH_SALT=

# Admin Configuration
ADMIN_EMAILS={ADMIN_EMAIL}

# CORS Origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Rate Limiting
RATE_LIMIT_ACTIVATE_PER_MINUTE=5
RATE_LIMIT_VALIDATE_PER_MINUTE=60

# Grace Period (days)
GRACE_DAYS=7
"""
    
    env_path.write_text(content, encoding='utf-8')
    print(f"✅ Created {env_path}")
    print(f"   ⚠️  Please add your SUPABASE_SERVICE_ROLE_KEY from Supabase Dashboard")

def create_admin_dashboard_env():
    """Create .env.local file for admin dashboard."""
    env_path = Path("admin_dashboard/.env.local")
    
    content = f"""# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL={SUPABASE_URL}
NEXT_PUBLIC_SUPABASE_ANON_KEY={SUPABASE_ANON_KEY}

# Admin Configuration
NEXT_PUBLIC_ADMIN_EMAILS={ADMIN_EMAIL}

# API Configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
"""
    
    env_path.write_text(content, encoding='utf-8')
    print(f"✅ Created {env_path}")

def main():
    print("=" * 60)
    print("Creating environment files...")
    print("=" * 60)
    print()
    
    create_license_server_env()
    print()
    create_admin_dashboard_env()
    print()
    print("=" * 60)
    print("✅ Environment files created!")
    print()
    print("⚠️  IMPORTANT: You need to:")
    print("   1. Get Supabase Service Role Key:")
    print("      - Go to https://ajeudhzebocbwzbifebb.supabase.co")
    print("      - Settings → API → service_role key")
    print("      - Add it to license_server/.env")
    print()
    print("   2. Create admin user in Supabase:")
    print("      - Go to Supabase Dashboard → Authentication → Users")
    print("      - Click 'Add user' → 'Create new user'")
    print(f"      - Email: {ADMIN_EMAIL}")
    print("      - Set a password")
    print("=" * 60)

if __name__ == "__main__":
    main()
