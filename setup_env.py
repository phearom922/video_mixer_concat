#!/usr/bin/env python3
"""
Script to help setup environment files for the Video Mixer Licensing System.
"""
import os
import secrets
from pathlib import Path

# Supabase configuration (already retrieved)
SUPABASE_URL = "https://ajeudhzebocbwzbifebb.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFqZXVkaHplYm9jYnd6YmlmZWJiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njg3MjUxNjksImV4cCI6MjA4NDMwMTE2OX0.fHgr4gq5_Zv6Ry6kEjkV_eaHSkx0tt-AIpVkNCtAW7o"
JWT_SECRET = "2dp-y1XYn7kfm3cnWNEFUTPHLq8vbvCr-iOvdkv0C6o"

def create_license_server_env():
    """Create .env file for license server."""
    env_path = Path("license_server/.env")
    
    if env_path.exists():
        print(f"⚠️  {env_path} already exists. Skipping...")
        return
    
    print("📝 Creating license_server/.env...")
    
    service_role_key = input("Enter Supabase Service Role Key (from Supabase Dashboard → Settings → API): ").strip()
    admin_email = input("Enter admin email address: ").strip()
    
    content = f"""# Supabase Configuration
SUPABASE_URL={SUPABASE_URL}
SUPABASE_SERVICE_ROLE_KEY={service_role_key}

# JWT Configuration
JWT_SIGNING_SECRET={JWT_SECRET}
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=8760

# Device Hashing (optional)
DEVICE_HASH_SALT=

# Admin Configuration
ADMIN_EMAILS={admin_email}

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

def create_admin_dashboard_env():
    """Create .env.local file for admin dashboard."""
    env_path = Path("admin_dashboard/.env.local")
    
    if env_path.exists():
        print(f"⚠️  {env_path} already exists. Skipping...")
        return
    
    print("📝 Creating admin_dashboard/.env.local...")
    
    admin_email = input("Enter admin email address (same as license server): ").strip()
    
    content = f"""# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL={SUPABASE_URL}
NEXT_PUBLIC_SUPABASE_ANON_KEY={SUPABASE_ANON_KEY}

# Admin Configuration
NEXT_PUBLIC_ADMIN_EMAILS={admin_email}

# API Configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
"""
    
    env_path.write_text(content, encoding='utf-8')
    print(f"✅ Created {env_path}")

def main():
    """Main setup function."""
    print("=" * 60)
    print("Video Mixer Licensing System - Environment Setup")
    print("=" * 60)
    print()
    
    print("This script will help you create environment files.")
    print("You'll need:")
    print("  1. Supabase Service Role Key (from Supabase Dashboard)")
    print("  2. Your admin email address")
    print()
    
    response = input("Continue? (y/n): ").strip().lower()
    if response != 'y':
        print("Cancelled.")
        return
    
    print()
    create_license_server_env()
    print()
    create_admin_dashboard_env()
    print()
    print("=" * 60)
    print("✅ Setup complete!")
    print()
    print("Next steps:")
    print("  1. Install dependencies:")
    print("     - license_server: pip install -r requirements.txt")
    print("     - admin_dashboard: npm install")
    print("     - desktop_app: pip install -r requirements.txt")
    print()
    print("  2. Create admin user in Supabase:")
    print("     - Go to Supabase Dashboard → Authentication → Users")
    print("     - Click 'Add user' → 'Create new user'")
    print("     - Use the same email you entered above")
    print()
    print("  3. Run the services:")
    print("     - License Server: cd license_server && uvicorn app.main:app --reload")
    print("     - Admin Dashboard: cd admin_dashboard && npm run dev")
    print("     - Desktop App: cd desktop_app && python -m app.main")
    print("=" * 60)

if __name__ == "__main__":
    main()
