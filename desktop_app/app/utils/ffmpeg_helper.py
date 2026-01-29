"""FFmpeg helper utilities for finding FFmpeg executable."""
import sys
import shutil
from pathlib import Path
from typing import Optional
from app.services.logging_service import logger


def get_bundled_ffmpeg_path() -> Optional[Path]:
    """
    Get path to bundled FFmpeg executable.
    
    Returns:
        Path to bundled FFmpeg if found, None otherwise
    """
    if getattr(sys, 'frozen', False):
        # Running as compiled executable (PyInstaller)
        # sys._MEIPASS is the temporary folder where PyInstaller extracts files
        base_path = Path(sys._MEIPASS)
    else:
        # Running as script
        base_path = Path(__file__).parent.parent.parent
    
    # FFmpeg should be in ffmpeg/bin/ffmpeg.exe
    ffmpeg_path = base_path / "ffmpeg" / "bin" / "ffmpeg.exe"
    if ffmpeg_path.exists():
        return ffmpeg_path
    return None


def find_ffmpeg() -> Optional[str]:
    """
    Try to find FFmpeg executable.
    
    Priority:
    1. Bundled FFmpeg (if running as executable)
    2. FFmpeg in PATH
    3. None
    
    Returns:
        Path to FFmpeg executable if found, None otherwise
    """
    # First, check bundled FFmpeg
    bundled_path = get_bundled_ffmpeg_path()
    if bundled_path:
        logger.info(f"Found bundled FFmpeg at: {bundled_path}")
        return str(bundled_path)
    
    # Fallback: try to find in PATH
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        logger.info(f"Found FFmpeg in PATH: {ffmpeg}")
        return ffmpeg
    
    logger.warning("FFmpeg not found in bundled location or PATH")
    return None
