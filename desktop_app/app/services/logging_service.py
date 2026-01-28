"""Logging service for file-based logging."""
import logging
from datetime import datetime
from pathlib import Path
from app.utils.paths import get_logs_dir, ensure_directories


def setup_logging():
    """Setup file-based logging."""
    ensure_directories()
    logs_dir = get_logs_dir()
    
    # Create log file with timestamp
    log_file = logs_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()  # Also log to console
        ]
    )
    
    return logging.getLogger("VideoMixer")


logger = setup_logging()
