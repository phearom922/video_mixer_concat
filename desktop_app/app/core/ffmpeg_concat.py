"""FFmpeg concatenation handling."""
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Optional
from app.services.logging_service import logger

# Windows-specific: Hide console window for subprocess
if sys.platform == 'win32':
    CREATE_NO_WINDOW = 0x08000000
else:
    CREATE_NO_WINDOW = 0


class FFmpegConcat:
    """FFmpeg concatenation handler."""
    
    def __init__(self, ffmpeg_path: Optional[str] = None):
        self.ffmpeg_path = ffmpeg_path or "ffmpeg"
    
    def concat_videos(
        self,
        input_files: List[Path],
        output_file: Path,
        use_copy: bool = True,
        progress_callback: Optional[callable] = None
    ) -> bool:
        """
        Concatenate video files using FFmpeg.
        
        Args:
            input_files: List of input video file paths
            output_file: Output file path
            use_copy: Try to use stream copy (fast) first, fallback to re-encode
            progress_callback: Optional callback for progress updates
        
        Returns:
            True if successful, False otherwise
        """
        if use_copy:
            # Try copy mode first
            if self._concat_with_copy(input_files, output_file, progress_callback):
                return True
            logger.info("Copy mode failed, falling back to re-encode")
        
        # Fallback to re-encode
        return self._concat_with_reencode(input_files, output_file, progress_callback)
    
    def _concat_with_copy(
        self,
        input_files: List[Path],
        output_file: Path,
        progress_callback: Optional[callable] = None
    ) -> bool:
        """Concatenate using stream copy (fast)."""
        # Create concat list file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            list_file = Path(f.name)
            for input_file in input_files:
                # Use absolute paths and escape single quotes
                abs_path = input_file.resolve()
                f.write(f"file '{abs_path}'\n")
        
        try:
            cmd = [
                self.ffmpeg_path,
                "-f", "concat",
                "-safe", "0",
                "-i", str(list_file),
                "-c", "copy",
                "-y",  # Overwrite output
                str(output_file)
            ]
            
            if progress_callback:
                progress_callback(f"Starting concat (copy mode): {len(input_files)} files")
            
            # Hide console window on Windows
            startupinfo = None
            if sys.platform == 'win32':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=3600,  # 1 hour timeout
                creationflags=CREATE_NO_WINDOW if sys.platform == 'win32' else 0,
                startupinfo=startupinfo
            )
            
            if result.returncode == 0:
                if progress_callback:
                    progress_callback(f"Successfully created: {output_file.name}")
                return True
            else:
                logger.error(f"FFmpeg copy failed: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            logger.error("FFmpeg timeout")
            return False
        except Exception as e:
            logger.error(f"FFmpeg error: {e}")
            return False
        finally:
            # Clean up list file
            try:
                list_file.unlink()
            except:
                pass
    
    def _concat_with_reencode(
        self,
        input_files: List[Path],
        output_file: Path,
        progress_callback: Optional[callable] = None
    ) -> bool:
        """Concatenate with re-encoding (slower but more compatible)."""
        # Create concat list file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            list_file = Path(f.name)
            for input_file in input_files:
                abs_path = input_file.resolve()
                f.write(f"file '{abs_path}'\n")
        
        try:
            cmd = [
                self.ffmpeg_path,
                "-f", "concat",
                "-safe", "0",
                "-i", str(list_file),
                "-c:v", "libx264",
                "-c:a", "aac",
                "-y",
                str(output_file)
            ]
            
            if progress_callback:
                progress_callback(f"Starting concat (re-encode mode): {len(input_files)} files")
            
            # Hide console window on Windows
            startupinfo = None
            if sys.platform == 'win32':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=7200,  # 2 hour timeout
                creationflags=CREATE_NO_WINDOW if sys.platform == 'win32' else 0,
                startupinfo=startupinfo
            )
            
            if result.returncode == 0:
                if progress_callback:
                    progress_callback(f"Successfully created: {output_file.name}")
                return True
            else:
                logger.error(f"FFmpeg re-encode failed: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            logger.error("FFmpeg timeout")
            return False
        except Exception as e:
            logger.error(f"FFmpeg error: {e}")
            return False
        finally:
            # Clean up list file
            try:
                list_file.unlink()
            except:
                pass
