"""Main application entry point."""
import sys
import shutil
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt
from app.ui.main_window import MainWindow
from app.ui.activation_window import ActivationWindow
from app.services.config_service import config_service
from app.services.license_guard import license_guard
from app.services.logging_service import logger
from app.utils.paths import ensure_directories


def find_ffmpeg() -> str:
    """Try to find FFmpeg in PATH."""
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        return ffmpeg
    return None


def check_ffmpeg():
    """Check if FFmpeg is available."""
    ffmpeg_path = config_service.get_ffmpeg_path()
    if not ffmpeg_path:
        # Try to find in PATH
        ffmpeg_path = find_ffmpeg()
        if ffmpeg_path:
            config_service.set_ffmpeg_path(ffmpeg_path)
            return True
        return False
    return Path(ffmpeg_path).exists()


def main():
    """Main application function."""
    # Ensure directories exist
    ensure_directories()
    
    # Setup logging
    logger.info("Starting Video Mixer Concat")
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Video Mixer Concat")
    
    # Check FFmpeg
    if not check_ffmpeg():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("FFmpeg Not Found")
        msg.setText("FFmpeg is not installed or not found in PATH.")
        msg.setInformativeText(
            "Please install FFmpeg or configure the path in settings.\n"
            "You can download FFmpeg from https://ffmpeg.org/download.html"
        )
        msg.exec()
    
    # Check license activation
    token = config_service.get_activation_token()
    if not token:
        # Show activation window
        activation = ActivationWindow()
        if activation.exec() != ActivationWindow.Accepted:
            sys.exit(0)
    
    # Validate license
    is_valid, reason = license_guard.is_license_valid()
    if not is_valid:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("License Validation Failed")
        msg.setText("Your license is not valid.")
        msg.setInformativeText(reason or "Please activate your license.")
        msg.setStandardButtons(QMessageBox.Ok)
        
        activation = ActivationWindow()
        if activation.exec() != ActivationWindow.Accepted:
            sys.exit(0)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
