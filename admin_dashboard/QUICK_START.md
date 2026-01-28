# Quick Start Guide - Admin Dashboard

## ✅ Dependencies Installed!

All npm packages have been installed successfully (368 packages).

## Running the Dashboard

### Start Development Server

```bash
cd admin_dashboard
npm run dev
```

The dashboard will be available at:
- **URL**: http://localhost:3000

### Login Credentials

- **Email**: `ronphearom056@gmail.com`
- **Password**: `Phearom090790`

## Features

### License Management
- Create new licenses
- Search and filter licenses
- View license details
- Revoke licenses
- View activations for each license

### Release Management
- Create app releases
- Set latest version
- Add release notes
- Configure download URLs

## Security Notes

⚠️ There are some npm warnings about deprecated packages and vulnerabilities. These are mostly in dev dependencies and don't affect production functionality. You can:

1. **Ignore for now** (safe for development)
2. **Update later** when you have time to test breaking changes
3. **Run audit fix** (may require code changes):
   ```bash
   npm audit fix
   ```

## Troubleshooting

### Port 3000 already in use
Change the port:
```bash
npm run dev -- -p 3001
```

### Environment variables not loading
Make sure `.env.local` exists in `admin_dashboard/` directory with:
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `NEXT_PUBLIC_ADMIN_EMAILS`
- `NEXT_PUBLIC_API_BASE_URL`

### Build errors
Clear Next.js cache:
```bash
rm -rf .next
npm run dev
```
