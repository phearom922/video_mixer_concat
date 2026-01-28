# Admin Dashboard (Next.js)

Admin dashboard for managing licenses and releases for the Video Mixer desktop application.

## Features

- Supabase Auth integration
- License management (create, search, revoke)
- Activation viewing and revocation
- Release management (create, set latest)
- Modern UI with Tailwind CSS

## Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

Copy `env.example` to `.env.local` and fill in the values:

```bash
cp env.example .env.local
```

Required environment variables:
- `NEXT_PUBLIC_SUPABASE_URL`: Your Supabase project URL
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`: Supabase anonymous key
- `NEXT_PUBLIC_ADMIN_EMAILS`: Comma-separated list of admin email addresses
- `NEXT_PUBLIC_API_BASE_URL`: FastAPI license server URL (default: http://localhost:8000)

### 3. Run the Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### 4. Build for Production

```bash
npm run build
npm start
```

## Usage

1. Navigate to `/login` and sign in with a Supabase account
2. Your email must be in the `NEXT_PUBLIC_ADMIN_EMAILS` list
3. After login, you'll be redirected to the licenses page
4. Create licenses, manage activations, and create releases

## Pages

- `/login` - Admin login page
- `/licenses` - License management (list, search, create)
- `/licenses/[id]` - License detail view with activations
- `/releases` - Release management
