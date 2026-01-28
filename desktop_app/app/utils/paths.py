"""Path utilities for app data directories."""
import os
from pathlib import Path


def get_app_data_dir() -> Path:
    """Get application data directory."""
    app_name = "VideoMixerConcat"
    app_data = Path(os.getenv("APPDATA", Path.home() / "AppData" / "Roaming"))
    return app_data / app_name


def get_config_file() -> Path:
    """Get config file path."""
    return get_app_data_dir() / "config.json"


def get_logs_dir() -> Path:
    """Get logs directory."""
    return get_app_data_dir() / "logs"


def ensure_directories():
    """Ensure all required directories exist."""
    get_app_data_dir().mkdir(parents=True, exist_ok=True)
    get_logs_dir().mkdir(parents=True, exist_ok=True)
