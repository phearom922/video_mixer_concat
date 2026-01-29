"""Update notification dialog."""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit
)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices, QIcon
from pathlib import Path
from app.services.update_service import update_service
from app.services.config_service import config_service


class UpdateDialog(QDialog):
    """Dialog for showing update notifications."""
    
    def __init__(self, update_info: dict, parent=None):
        super().__init__(parent)
        self.update_info = update_info
        self.setWindowTitle("Update Available")
        self.setMinimumWidth(500)
        self.setMinimumHeight(350)
        self.setModal(True)
        
        # Set window icon
        assets_path = Path(__file__).parent / "assets"
        icon_path = assets_path / "logo128x128.png"
        if icon_path.exists():
            icon = QIcon(str(icon_path))
            self.setWindowIcon(icon)
        else:
            fallback_icon_path = assets_path / "logo96x96.png"
            if fallback_icon_path.exists():
                icon = QIcon(str(fallback_icon_path))
                self.setWindowIcon(icon)
        
        # Apply Dark Mode styling
        self.setStyleSheet("""
            QDialog {
                background-color: #0d1117;
                color: #e6edf3;
            }
            QLabel {
                color: #e6edf3;
            }
            QTextEdit {
                background-color: #161b22;
                border: 1px solid #30363d;
                border-radius: 8px;
                color: #c9d1d9;
                padding: 12px;
                font-size: 13px;
                selection-background-color: #388bfd;
            }
            QPushButton {
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 13px;
                border: none;
                min-width: 120px;
            }
            QPushButton#downloadButton {
                background-color: #238636;
                color: white;
            }
            QPushButton#downloadButton:hover {
                background-color: #2ea043;
            }
            QPushButton#downloadButton:pressed {
                background-color: #1f7a2e;
            }
            QPushButton#laterButton {
                background-color: #4b5563;
                color: #e0e0e0;
            }
            QPushButton#laterButton:hover {
                background-color: #374151;
            }
            QPushButton#laterButton:pressed {
                background-color: #1f2937;
            }
            QPushButton#skipButton {
                background-color: #6b7280;
                color: #e0e0e0;
            }
            QPushButton#skipButton:hover {
                background-color: #4b5563;
            }
            QPushButton#skipButton:pressed {
                background-color: #374151;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Title
        title = QLabel(f"Version {update_info.get('latest_version')} Available")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #e6edf3;")
        layout.addWidget(title)
        
        layout.addSpacing(8)
        
        # Release notes
        notes_label = QLabel("Release Notes:")
        notes_label.setStyleSheet("font-size: 14px; font-weight: 600; color: #8b949e;")
        layout.addWidget(notes_label)
        
        notes_text = QTextEdit()
        notes_text.setReadOnly(True)
        notes_text.setMaximumHeight(200)
        notes_text.setText(update_info.get("release_notes", "No release notes available."))
        layout.addWidget(notes_text)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        self.download_button = QPushButton("Download")
        self.download_button.setObjectName("downloadButton")
        self.download_button.clicked.connect(self.download)
        button_layout.addWidget(self.download_button)
        
        self.later_button = QPushButton("Later")
        self.later_button.setObjectName("laterButton")
        self.later_button.clicked.connect(self.accept)
        button_layout.addWidget(self.later_button)
        
        self.skip_button = QPushButton("Skip This Version")
        self.skip_button.setObjectName("skipButton")
        self.skip_button.clicked.connect(self.skip_version)
        button_layout.addWidget(self.skip_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def download(self):
        """Open download URL in browser."""
        download_url = self.update_info.get("download_url")
        if download_url:
            QDesktopServices.openUrl(download_url)
        self.accept()
    
    def skip_version(self):
        """Skip this version."""
        version = self.update_info.get("latest_version")
        if version:
            update_service.skip_version(version)
        self.accept()
