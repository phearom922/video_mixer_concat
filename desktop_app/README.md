# Video Mixer Concat Desktop App

Windows desktop application for concatenating video files in groups using FFmpeg.

## Features

- License activation and validation
- Video file concatenation (concat only)
- Configurable grouping and sorting
- Custom output naming patterns
- Progress tracking and logging
- Automatic update notifications
- Offline grace period (7 days)

## Requirements

- Windows 10/11
- Python 3.11+
- FFmpeg (must be installed and in PATH, or configured manually)

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API URL

The app needs to know where the license server is running. By default, it uses the production server: `https://api.mixer.camboskill.com`

**For Development:**
- Set environment variable: `LICENSE_API_URL=http://localhost:8000`
- Or configure in the app settings/config file

**For Production:**
- Uses production URL by default (no configuration needed)

### 3. Install FFmpeg

**Option 1: Install FFmpeg globally**
- Download from https://ffmpeg.org/download.html
- Add to system PATH
- The app will detect it automatically

**Option 2: Manual configuration**
- Download FFmpeg and extract to a folder
- When the app starts, it will prompt you to browse for `ffmpeg.exe`
- The path will be saved in the config

**Option 3: Auto-download (optional)**
- The app can optionally download FFmpeg for you (feature to be implemented)

### 4. Run the Application

```bash
python -m app.main
```

## First Run

1. On first launch, you'll be prompted to activate your license
2. Enter your license key (provided by admin)
3. Optionally enter a device label (e.g., "Office-PC-1")
4. Click "Activate"

## Usage

1. **Select Folders**
   - Input Folder: Folder containing video files to concatenate
   - Output Folder: Where concatenated videos will be saved

2. **Configure Settings**
   - Group Size: Number of videos per group (minimum 2)
   - Sort Mode: How to sort files (Filename, Time, Random)
   - Remainder Behavior: What to do with leftover files
   - Output Naming: Pattern for output files (use `{group}` and `{count}` placeholders)

3. **Start Processing**
   - Click "Start" to begin concatenation
   - Monitor progress in the log panel
   - Click "Cancel" to stop processing

## Configuration

Configuration is stored in `%APPDATA%\VideoMixerConcat\config.json`:

- `activation_token`: Stored activation token
- `api_base_url`: License server URL
- `ffmpeg_path`: Path to FFmpeg executable
- `last_validation_time`: Last successful license validation
- `skipped_versions`: List of skipped update versions

## Building for Distribution

### Using PyInstaller

```bash
pip install pyinstaller
pyinstaller pyinstaller.spec
```

The executable will be in `dist/VideoMixerConcat.exe`

### Customization

Edit `pyinstaller.spec` to:
- Add an icon file
- Include additional data files
- Configure build options

## License Validation

- License is validated on startup
- Periodic validation every 24 hours
- 7-day offline grace period
- If validation fails, app will lock and require activation

## Update Notifications

- App checks for updates on launch and every 12 hours
- If an update is available, a popup will show:
  - Latest version number
  - Release notes
  - Download button (opens browser)
  - Option to skip the version

## Troubleshooting

**FFmpeg not found:**
- Ensure FFmpeg is installed and in PATH
- Or configure the path manually in settings

**License activation fails:**
- Check internet connection
- Verify license key is correct
- Ensure license server is running and accessible

**Video concatenation fails:**
- Check that input files are valid video files
- Ensure output folder is writable
- Try different output naming pattern
- Check FFmpeg logs for detailed errors

## Logs

Logs are stored in `%APPDATA%\VideoMixerConcat\logs\`
- Daily log files: `app_YYYYMMDD.log`
- Contains processing history and errors
