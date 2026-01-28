#!/usr/bin/env python3
"""
Update configuration files to use the correct project: zipuyqkqaktbaddsdrhc
"""
from pathlib import Path

CORRECT_PROJECT_REF = "zipuyqkqaktbaddsdrhc"
CORRECT_SUPABASE_URL = f"https://{CORRECT_PROJECT_REF}.supabase.co"

def update_license_server_env():
    """Update license_server/.env"""
    env_path = Path("license_server/.env")
    if not env_path.exists():
        print("❌ license_server/.env not found")
        return False
    
    print("📝 Updating license_server/.env...")
    
    with open(env_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update SUPABASE_URL
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if line.startswith("SUPABASE_URL="):
            new_lines.append(f"SUPABASE_URL={CORRECT_SUPABASE_URL}")
        else:
            new_lines.append(line)
    
    new_content = '\n'.join(new_lines)
    
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Updated SUPABASE_URL to {CORRECT_SUPABASE_URL}")
    print("   ⚠️  Please update SUPABASE_SERVICE_ROLE_KEY manually from Supabase Dashboard")
    return True

def update_admin_dashboard_env():
    """Update admin_dashboard/.env or create .env.local"""
    env_path = Path("admin_dashboard/.env.local")
    env_path_alt = Path("admin_dashboard/.env")
    
    # Check which file exists
    target_path = env_path if env_path.exists() else env_path_alt
    
    if not target_path.exists():
        print("📝 Creating admin_dashboard/.env.local...")
        target_path = Path("admin_dashboard/.env.local")
    
    print(f"📝 Updating {target_path}...")
    
    # Read existing content if exists
    content = ""
    if target_path.exists():
        with open(target_path, 'r', encoding='utf-8') as f:
            content = f.read()
    
    lines = content.split('\n') if content else []
    new_lines = []
    updated_url = False
    updated_anon = False
    
    for line in lines:
        if line.startswith("NEXT_PUBLIC_SUPABASE_URL="):
            new_lines.append(f"NEXT_PUBLIC_SUPABASE_URL={CORRECT_SUPABASE_URL}")
            updated_url = True
        elif line.startswith("NEXT_PUBLIC_SUPABASE_ANON_KEY="):
            # Keep existing anon key, just note that it needs to be from correct project
            new_lines.append(line)
            updated_anon = True
        else:
            new_lines.append(line)
    
    # Add missing lines
    if not updated_url:
        new_lines.insert(0, f"NEXT_PUBLIC_SUPABASE_URL={CORRECT_SUPABASE_URL}")
    
    if not any("NEXT_PUBLIC_ADMIN_EMAILS" in line for line in new_lines):
        new_lines.append("")
        new_lines.append("# Admin Configuration")
        new_lines.append("NEXT_PUBLIC_ADMIN_EMAILS=ronphearom056@gmail.com")
    
    if not any("NEXT_PUBLIC_API_BASE_URL" in line for line in new_lines):
        new_lines.append("")
        new_lines.append("# API Configuration")
        new_lines.append("NEXT_PUBLIC_API_BASE_URL=http://localhost:8000")
    
    new_content = '\n'.join(new_lines)
    
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Updated {target_path}")
    if not updated_anon:
        print("   ⚠️  Please add NEXT_PUBLIC_SUPABASE_ANON_KEY from Supabase Dashboard")
    
    return True

def main():
    print("=" * 60)
    print("Updating Configuration to Use Correct Project")
    print("=" * 60)
    print()
    print(f"Correct Project: {CORRECT_PROJECT_REF}")
    print(f"Correct URL: {CORRECT_SUPABASE_URL}")
    print()
    
    update_license_server_env()
    print()
    update_admin_dashboard_env()
    print()
    print("=" * 60)
    print("✅ Configuration updated!")
    print()
    print("Next steps:")
    print(f"  1. Go to {CORRECT_SUPABASE_URL}")
    print("  2. Settings → API")
    print("  3. Copy service_role key → Update license_server/.env")
    print("  4. Copy anon key → Update admin_dashboard/.env.local")
    print("  5. Run: python verify_and_fix.py")
    print("=" * 60)

if __name__ == "__main__":
    main()
