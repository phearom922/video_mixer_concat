"""Background worker for video processing."""
from PySide6.QtCore import QThread, Signal
from pathlib import Path
from typing import List, Optional
from app.core.ffmpeg_concat import FFmpegConcat
from app.core.grouper import group_files, SortMode, RemainderBehavior
from app.services.logging_service import logger


class VideoProcessingWorker(QThread):
    """Worker thread for processing video groups."""
    
    # Signals
    progress = Signal(str)  # Progress message
    group_complete = Signal(int, int, bool)  # group_index, total_groups, success
    finished = Signal(bool)  # overall success
    
    def __init__(
        self,
        input_dir: Path,
        output_dir: Path,
        group_size: int,
        sort_mode: SortMode,
        remainder_behavior: RemainderBehavior,
        output_naming_pattern: str,
        ffmpeg_path: Optional[str] = None
    ):
        super().__init__()
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.group_size = group_size
        self.sort_mode = sort_mode
        self.remainder_behavior = remainder_behavior
        self.output_naming_pattern = output_naming_pattern
        self.ffmpeg_path = ffmpeg_path
        self._cancelled = False
    
    def cancel(self):
        """Cancel processing."""
        self._cancelled = True
    
    def run(self):
        """Run the processing."""
        try:
            # Scan files
            self.progress.emit("Scanning video files...")
            from app.core.grouper import scan_video_files
            files = scan_video_files(self.input_dir)
            
            if not files:
                self.progress.emit("No video files found")
                self.finished.emit(False)
                return
            
            self.progress.emit(f"Found {len(files)} video files")
            
            # Group files
            self.progress.emit("Grouping files...")
            groups, remainder = group_files(
                files,
                self.group_size,
                self.sort_mode,
                self.remainder_behavior
            )
            
            if not groups:
                self.progress.emit("No groups to process")
                self.finished.emit(False)
                return
            
            self.progress.emit(f"Created {len(groups)} groups")
            
            # Handle remainder
            if remainder:
                if self.remainder_behavior == RemainderBehavior.WARN:
                    self.progress.emit(f"Warning: {len(remainder)} files remain ungrouped")
                elif self.remainder_behavior == RemainderBehavior.EXPORT_SINGLE:
                    groups.append(remainder)
            
            # Process groups
            ffmpeg = FFmpegConcat(self.ffmpeg_path)
            total_groups = len(groups)
            success_count = 0
            
            for i, group in enumerate(groups):
                if self._cancelled:
                    self.progress.emit("Processing cancelled")
                    self.finished.emit(False)
                    return
                
                # Generate output filename
                output_filename = self._generate_output_filename(i, len(group))
                output_file = self.output_dir / output_filename
                
                self.progress.emit(f"Processing group {i + 1}/{total_groups}: {output_filename}")
                
                def progress_callback(msg: str):
                    self.progress.emit(msg)
                
                success = ffmpeg.concat_videos(group, output_file, use_copy=True, progress_callback=progress_callback)
                
                if success:
                    success_count += 1
                    self.progress.emit(f"✓ Group {i + 1} completed")
                else:
                    self.progress.emit(f"✗ Group {i + 1} failed")
                
                self.group_complete.emit(i + 1, total_groups, success)
            
            # Final status
            if success_count == total_groups:
                self.progress.emit(f"All {total_groups} groups processed successfully")
                self.finished.emit(True)
            else:
                self.progress.emit(f"Completed {success_count}/{total_groups} groups")
                self.finished.emit(False)
        
        except Exception as e:
            logger.error(f"Processing error: {e}")
            self.progress.emit(f"Error: {str(e)}")
            self.finished.emit(False)
    
    def _generate_output_filename(self, group_index: int, file_count: int) -> str:
        """Generate output filename based on pattern."""
        pattern = self.output_naming_pattern
        
        # Replace placeholders
        filename = pattern.replace("{group}", f"{group_index + 1:03d}")
        filename = filename.replace("{count}", str(file_count))
        
        # Ensure .mp4 extension
        if not filename.endswith('.mp4'):
            filename += '.mp4'
        
        return filename
