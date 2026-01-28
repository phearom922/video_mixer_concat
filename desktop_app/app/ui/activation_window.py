"""License activation window."""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QTextEdit, QFrame, QProgressBar
)
from PySide6.QtCore import Qt, QUrl, QTimer
from PySide6.QtGui import QDesktopServices, QFont
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
        
        # Apply Dark Mode styling
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
                color: #e0e0e0;
            }
            QLabel {
                color: #d0d0d0;
            }
            QLineEdit {
                padding: 10px 12px;
                border: 2px solid #404040;
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
                min-width: 120px;
            }
            QPushButton#telegramButton:hover {
                background-color: #006ba3;
            }
            QPushButton#telegramButton:pressed {
                background-color: #005a8a;
            }
            QFrame#infoFrame {
                background-color: #1e3a5f;
                border: 2px solid #3b82f6;
                border-radius: 10px;
                padding: 12px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Title
        title = QLabel("🔑 License Activation")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #e0e0e0; margin-bottom: 8px;")
        layout.addWidget(title)
        
        # Instructions
        instructions = QLabel(
            "Enter your license key to activate the application.\n"
            "An internet connection is required for activation."
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet("color: #9ca3af; font-size: 13px; margin-bottom: 4px;")
        layout.addWidget(instructions)
        
        # Info frame with Telegram link
        info_frame = QFrame()
        info_frame.setObjectName("infoFrame")
        info_layout = QVBoxLayout()
        info_layout.setSpacing(8)
        
        info_label = QLabel("💬 Need a license key?")
        info_label.setStyleSheet("font-weight: 600; color: #60a5fa; font-size: 13px;")
        info_layout.addWidget(info_label)
        
        telegram_layout = QHBoxLayout()
        telegram_text = QLabel("Contact us on Telegram:")
        telegram_text.setStyleSheet("color: #93c5fd; font-size: 12px;")
        telegram_layout.addWidget(telegram_text)
        
        telegram_button = QPushButton("📱 Open Telegram")
        telegram_button.setObjectName("telegramButton")
        telegram_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(TELEGRAM_URL)))
        telegram_layout.addWidget(telegram_button)
        telegram_layout.addStretch()
        
        info_layout.addLayout(telegram_layout)
        info_frame.setLayout(info_layout)
        layout.addWidget(info_frame)
        
        layout.addSpacing(8)
        
        # License key input
        license_label = QLabel("License Key:")
        license_label.setStyleSheet("font-weight: 600; color: #d0d0d0; font-size: 13px;")
        layout.addWidget(license_label)
        self.license_input = QLineEdit()
        self.license_input.setPlaceholderText("Enter your license key here...")
        layout.addWidget(self.license_input)
        
        # Device label (optional)
        device_label = QLabel("Device Label (optional):")
        device_label.setStyleSheet("font-weight: 600; color: #d0d0d0; font-size: 13px;")
        layout.addWidget(device_label)
        self.device_label_input = QLineEdit()
        self.device_label_input.setPlaceholderText("e.g., Office-PC-1, Home-Laptop")
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
            message = "✅ Your license has been activated successfully!\n\n"
            
            if expires_at:
                try:
                    exp_date = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
                    message += f"📅 License expires: {exp_date.strftime('%B %d, %Y')}\n"
                except:
                    pass
            
            customer_name = license_info.get("customer_name")
            if customer_name:
                message += f"👤 Customer: {customer_name}\n"
            
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
                error_msg += f"\n\n💡 Need a license? Contact us on Telegram:\n{TELEGRAM_URL}"
            
            # Create custom message box with centered OK button
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowTitle("Activation Failed")
            msg_box.setText(f"❌ Failed to activate license:\n\n{error_msg}")
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
