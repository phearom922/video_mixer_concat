"""Update notification dialog."""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QDesktopServices
from app.services.update_service import update_service
from app.services.config_service import config_service


class UpdateDialog(QDialog):
    """Dialog for showing update notifications."""
    
    def __init__(self, update_info: dict, parent=None):
        super().__init__(parent)
        self.update_info = update_info
        self.setWindowTitle("Update Available")
        self.setMinimumWidth(500)
        self.setModal(True)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel(f"Version {update_info.get('latest_version')} Available")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)
        
        # Release notes
        notes_label = QLabel("Release Notes:")
        layout.addWidget(notes_label)
        
        notes_text = QTextEdit()
        notes_text.setReadOnly(True)
        notes_text.setMaximumHeight(200)
        notes_text.setText(update_info.get("release_notes", "No release notes available."))
        layout.addWidget(notes_text)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.download)
        button_layout.addWidget(self.download_button)
        
        self.later_button = QPushButton("Later")
        self.later_button.clicked.connect(self.accept)
        button_layout.addWidget(self.later_button)
        
        self.skip_button = QPushButton("Skip This Version")
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
