"""License activation window."""
from pathlib import Path
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QTextEdit, QFrame, QProgressBar
)
from PySide6.QtCore import Qt, QUrl, QTimer, QSize
from PySide6.QtGui import QDesktopServices, QFont, QPixmap, QIcon
from pathlib import Path
from app.ui.icon_helper import set_icon_to_label, create_icon_label
from datetime import datetime
from app.services.device_fingerprint import get_device_fingerprint
from app.services.api_client import api_client
from app.services.config_service import config_service
from app.services.logging_service import logger
from app import APP_VERSION

TELEGRAM_URL = "https://t.me/ronphearom"


class ActivationWindow(QDialog):
    """Window for license activation."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Activate License - Video Mixer Concat")
        self.setMinimumWidth(500)
        self.setMinimumHeight(450)
        self.setModal(True)
        
        # Set window icon
        assets_path = Path(__file__).parent / "assets"
        icon_path = assets_path / "logo128x128.png"
        if icon_path.exists():
            icon = QIcon(str(icon_path))
            self.setWindowIcon(icon)
        else:
            # Fallback: try logo96x96.png
            fallback_icon_path = assets_path / "logo96x96.png"
            if fallback_icon_path.exists():
                icon = QIcon(str(fallback_icon_path))
                self.setWindowIcon(icon)
        
        # Apply Dark Mode styling
        self.setStyleSheet("""
            QDialog {
                background-color: #2a2a2a;
                color: #e0e0e0;
            }
            QLabel {
                color: #d0d0d0;
            }
            QLineEdit {
                padding: 10px 12px;
                border: 1px solid #404040;
                border-radius: 8px;
                background-color: #252525;
                color: #e0e0e0;
                font-size: 13px;
                selection-background-color: #4a5568;
            }
            QLineEdit:focus {
                border-color: #6366f1;
                background-color: #2d2d2d;
                outline: none;
            }
            QPushButton {
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 14px;
                border: none;
                min-width: 140px;
            }
            QPushButton#activateButton {
                background-color: #6366f1;
                color: white;
            }
            QPushButton#activateButton:hover {
                background-color: #4f46e5;
            }
            QPushButton#activateButton:pressed {
                background-color: #4338ca;
            }
            QPushButton#activateButton:disabled {
                background-color: #374151;
                color: #6b7280;
            }
            QPushButton#cancelButton {
                background-color: #4b5563;
                color: #e0e0e0;
            }
            QPushButton#cancelButton:hover {
                background-color: #374151;
            }
            QPushButton#cancelButton:pressed {
                background-color: #1f2937;
            }
            QPushButton#telegramButton {
                background-color: #0088cc;
                color: white;
                padding: 10px 18px;
                min-width: 140px;
                border-radius: 8px;
            }
            QPushButton#telegramButton:hover {
                background-color: #006ba3;
            }
            QPushButton#telegramButton:pressed {
                background-color: #005a8a;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(32, 32, 32, 32)
        
        # Logo section (centered)
        logo_layout = QVBoxLayout()
        logo_layout.setAlignment(Qt.AlignCenter)
        
        # Load logo (96x96 pixels)
        assets_path = Path(__file__).parent / "assets"
        logo_path = assets_path / "logo128x128.png"
        
        if logo_path.exists():
            logo_label = QLabel()
            pixmap = QPixmap(str(logo_path))
            # Scale to 96x96 if needed
            if pixmap.width() != 96 or pixmap.height() != 96:
                pixmap = pixmap.scaled(96, 96, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            logo_layout.addWidget(logo_label)
        else:
            # Fallback if logo not found
            logger.warning(f"Logo not found at {logo_path}")
        
        # App name "VIDMIX CONCAT"
        app_name = QLabel("VIDMIX CONCAT")
        app_name_font = QFont()
        app_name_font.setPointSize(18)
        app_name_font.setBold(True)
        app_name.setFont(app_name_font)
        app_name.setStyleSheet("color: #ffffff; margin-top: 8px;")
        app_name.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(app_name)
        
        layout.addLayout(logo_layout)
        layout.addSpacing(8)
        
        # Title "Activate Your License" with key icon
        title_layout = QHBoxLayout()
        title_layout.setAlignment(Qt.AlignCenter)
        title_layout.setSpacing(8)
        
        title_icon = create_icon_label("key", 20)
        title = QLabel("Activate Your License")
        title_font = QFont()
        title_font.setPointSize(22)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #e0e0e0;")
        title.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title_icon)
        title_layout.addWidget(title)
        
        layout.addLayout(title_layout)
        layout.addSpacing(4)
        
        # Instructions
        instructions = QLabel(
            "Enter your license key to unlock features. Activation requires internet."
        )
        instructions.setWordWrap(True)
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("color: #9ca3af; font-size: 13px;")
        layout.addWidget(instructions)
        
        layout.addSpacing(12)
        
        # Telegram Contact Section
        telegram_frame = QFrame()
        telegram_frame_layout = QVBoxLayout()
        telegram_frame_layout.setSpacing(8)
        telegram_frame_layout.setContentsMargins(0, 0, 0, 0)
        
        telegram_label = QLabel("Need a license key? Contact us.")
        telegram_label.setStyleSheet("color: #9ca3af; font-size: 12px;")
        telegram_label.setAlignment(Qt.AlignCenter)
        telegram_frame_layout.addWidget(telegram_label)
        
        telegram_button_layout = QHBoxLayout()
        telegram_button_layout.setAlignment(Qt.AlignCenter)
        
        # Create button with icon using QIcon
        telegram_icon_path = Path(__file__).parent / "assets" / "icon_airplane.svg"
        telegram_button = QPushButton("Open Telegram")
        telegram_button.setObjectName("telegramButton")
        if telegram_icon_path.exists():
            telegram_icon = QIcon(str(telegram_icon_path))
            telegram_button.setIcon(telegram_icon)
            telegram_button.setIconSize(QSize(16, 16))
        telegram_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(TELEGRAM_URL)))
        telegram_button_layout.addWidget(telegram_button)
        
        telegram_frame_layout.addLayout(telegram_button_layout)
        telegram_frame.setLayout(telegram_frame_layout)
        layout.addWidget(telegram_frame)
        
        layout.addSpacing(16)
        
        # License key input
        license_label = QLabel("License Key:")
        license_label.setStyleSheet("font-weight: 600; color: #d0d0d0; font-size: 13px;")
        layout.addWidget(license_label)
        self.license_input = QLineEdit()
        self.license_input.setPlaceholderText("Paste key here...")
        layout.addWidget(self.license_input)
        
        # Device label (optional)
        device_label = QLabel("Device Label (Optional):")
        device_label.setStyleSheet("font-weight: 600; color: #d0d0d0; font-size: 13px;")
        layout.addWidget(device_label)
        self.device_label_input = QLineEdit()
        self.device_label_input.setPlaceholderText("e.g., Work-PC")
        layout.addWidget(self.device_label_input)
        
        layout.addStretch()
        
        # Loading progress bar (hidden initially)
        self.loading_progress = QProgressBar()
        self.loading_progress.setMinimum(0)
        self.loading_progress.setMaximum(0)  # Indeterminate
        self.loading_progress.setVisible(False)
        self.loading_progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #404040;
                border-radius: 8px;
                background-color: #1a1a1a;
                height: 6px;
            }
            QProgressBar::chunk {
                background-color: #6366f1;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.loading_progress)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setObjectName("cancelButton")
        self.cancel_button.clicked.connect(self.reject)
        self.activate_button = QPushButton("Activate License")
        self.activate_button.setObjectName("activateButton")
        self.activate_button.clicked.connect(self.activate)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.activate_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def activate(self):
        """Activate license."""
        license_key = self.license_input.text().strip()
        if not license_key:
            QMessageBox.warning(self, "Error", "Please enter a license key")
            return
        
        device_label = self.device_label_input.text().strip() or None
        device_fingerprint = get_device_fingerprint()
        
        # Show loading state
        self.activate_button.setEnabled(False)
        self.activate_button.setText("Activating...")
        self.loading_progress.setVisible(True)
        self.cancel_button.setEnabled(False)
        self.license_input.setEnabled(False)
        self.device_label_input.setEnabled(False)
        
        # Force UI update
        QTimer.singleShot(100, self._perform_activation)
    
    def _perform_activation(self):
        """Perform the actual activation (called after UI update)."""
        license_key = self.license_input.text().strip()
        device_label = self.device_label_input.text().strip() or None
        device_fingerprint = get_device_fingerprint()
        
        try:
            result = api_client.activate(
                license_key,
                device_fingerprint,
                APP_VERSION,
                device_label
            )
            
            # Store activation token
            config_service.set_activation_token(result["activation_token"])
            
            # Store license expiration date if available
            license_info = result.get("license", {})
            expires_at = license_info.get("expires_at")
            if expires_at:
                config_service.set_license_expires_at(expires_at)
            
            # Hide loading
            self.loading_progress.setVisible(False)
            self.activate_button.setEnabled(True)
            self.activate_button.setText("Activate License")
            self.cancel_button.setEnabled(True)
            self.license_input.setEnabled(True)
            self.device_label_input.setEnabled(True)
            
            # Prepare success message
            message = "Your license has been activated successfully!\n\n"
            
            if expires_at:
                try:
                    exp_date = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
                    message += f"License expires: {exp_date.strftime('%B %d, %Y')}\n"
                except:
                    pass
            
            customer_name = license_info.get("customer_name")
            if customer_name:
                message += f"Customer: {customer_name}\n"
            
            # Create custom message box with centered OK button
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle("Activation Successful")
            msg_box.setText(message)
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #1e1e1e;
                    color: #e0e0e0;
                }
                QMessageBox QLabel {
                    color: #e0e0e0;
                }
                QMessageBox QPushButton {
                    min-width: 100px;
                    padding: 10px 20px;
                    background-color: #6366f1;
                    color: white;
                    border-radius: 6px;
                    font-weight: 600;
                }
                QMessageBox QPushButton:hover {
                    background-color: #4f46e5;
                }
            """)
            msg_box.exec()
            
            self.accept()
        
        except Exception as e:
            logger.error(f"Activation error: {e}")
            
            # Hide loading
            self.loading_progress.setVisible(False)
            self.activate_button.setEnabled(True)
            self.activate_button.setText("Activate License")
            self.cancel_button.setEnabled(True)
            self.license_input.setEnabled(True)
            self.device_label_input.setEnabled(True)
            
            error_msg = str(e)
            if "not found" in error_msg.lower():
                error_msg += f"\n\nNeed a license? Contact us on Telegram:\n{TELEGRAM_URL}"
            
            # Create custom message box with centered OK button
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowTitle("Activation Failed")
            msg_box.setText(f"Failed to activate license:\n\n{error_msg}")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #1e1e1e;
                    color: #e0e0e0;
                }
                QMessageBox QLabel {
                    color: #e0e0e0;
                }
                QMessageBox QPushButton {
                    min-width: 100px;
                    padding: 10px 20px;
                    background-color: #ef4444;
                    color: white;
                    border-radius: 6px;
                    font-weight: 600;
                }
                QMessageBox QPushButton:hover {
                    background-color: #dc2626;
                }
            """)
            msg_box.exec()
