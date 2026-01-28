-- Video Mixer Licensing System - Initial Schema
-- This migration creates all required tables, indexes, and RLS policies

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- 1. LICENSES TABLE
-- ============================================
CREATE TABLE licenses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    license_key TEXT UNIQUE NOT NULL,
    customer_name TEXT,
    max_activations INTEGER DEFAULT 1 NOT NULL,
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'revoked', 'suspended')),
    expires_at TIMESTAMPTZ,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_licenses_license_key ON licenses(license_key);
CREATE INDEX idx_licenses_status ON licenses(status);
CREATE INDEX idx_licenses_expires_at ON licenses(expires_at);

-- ============================================
-- 2. ACTIVATIONS TABLE
-- ============================================
CREATE TABLE activations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    license_id UUID NOT NULL REFERENCES licenses(id) ON DELETE CASCADE,
    device_id_hash TEXT NOT NULL,
    device_label TEXT,
    first_activated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    last_seen_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'revoked')),
    activated_app_version TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    UNIQUE(license_id, device_id_hash)
);

CREATE INDEX idx_activations_license_id ON activations(license_id);
CREATE INDEX idx_activations_device_id_hash ON activations(device_id_hash);
CREATE INDEX idx_activations_status ON activations(status);
CREATE INDEX idx_activations_last_seen_at ON activations(last_seen_at);

-- ============================================
-- 3. ADMIN AUDIT LOGS TABLE
-- ============================================
CREATE TABLE admin_audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    admin_user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    action TEXT NOT NULL,
    payload JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_admin_audit_logs_admin_user_id ON admin_audit_logs(admin_user_id);
CREATE INDEX idx_admin_audit_logs_action ON admin_audit_logs(action);
CREATE INDEX idx_admin_audit_logs_created_at ON admin_audit_logs(created_at DESC);

-- ============================================
-- 4. APP RELEASES TABLE
-- ============================================
CREATE TABLE app_releases (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    platform TEXT NOT NULL DEFAULT 'windows',
    version TEXT NOT NULL,
    release_notes TEXT,
    download_url TEXT NOT NULL,
    is_latest BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    UNIQUE(platform, version)
);

CREATE INDEX idx_app_releases_platform ON app_releases(platform);
CREATE INDEX idx_app_releases_version ON app_releases(version);
CREATE INDEX idx_app_releases_is_latest ON app_releases(is_latest) WHERE is_latest = TRUE;

-- ============================================
-- TRIGGERS FOR updated_at
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_licenses_updated_at
    BEFORE UPDATE ON licenses
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_activations_updated_at
    BEFORE UPDATE ON activations
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- ============================================

-- Enable RLS on all tables
ALTER TABLE licenses ENABLE ROW LEVEL SECURITY;
ALTER TABLE activations ENABLE ROW LEVEL SECURITY;
ALTER TABLE admin_audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE app_releases ENABLE ROW LEVEL SECURITY;

-- Helper function to check if user is admin
-- Admin is determined by email in auth.users matching ADMIN_EMAILS env var
-- For now, we'll create a function that can be extended
-- In practice, the FastAPI server will handle admin verification
CREATE OR REPLACE FUNCTION is_admin_user(user_id UUID)
RETURNS BOOLEAN AS $$
BEGIN
    -- This will be checked server-side via Supabase Auth JWT
    -- For RLS, we allow service role to access everything
    -- Regular users (desktop app) should NOT access Supabase directly
    RETURN FALSE;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- RLS Policies: Only service role (server) can access
-- Desktop app will NOT use Supabase directly, only via FastAPI

-- Licenses: Admin only (via service role)
CREATE POLICY "Admin only access to licenses"
    ON licenses
    FOR ALL
    USING (auth.jwt() ->> 'role' = 'service_role')
    WITH CHECK (auth.jwt() ->> 'role' = 'service_role');

-- Activations: Admin only (via service role)
CREATE POLICY "Admin only access to activations"
    ON activations
    FOR ALL
    USING (auth.jwt() ->> 'role' = 'service_role')
    WITH CHECK (auth.jwt() ->> 'role' = 'service_role');

-- Admin Audit Logs: Admin only (via service role)
CREATE POLICY "Admin only access to admin_audit_logs"
    ON admin_audit_logs
    FOR ALL
    USING (auth.jwt() ->> 'role' = 'service_role')
    WITH CHECK (auth.jwt() ->> 'role' = 'service_role');

-- App Releases: Admin only (via service role)
CREATE POLICY "Admin only access to app_releases"
    ON app_releases
    FOR ALL
    USING (auth.jwt() ->> 'role' = 'service_role')
    WITH CHECK (auth.jwt() ->> 'role' = 'service_role');

-- ============================================
-- COMMENTS
-- ============================================
COMMENT ON TABLE licenses IS 'License keys and their configuration';
COMMENT ON TABLE activations IS 'Device activations for licenses';
COMMENT ON TABLE admin_audit_logs IS 'Audit trail of admin actions';
COMMENT ON TABLE app_releases IS 'App version releases and update information';
