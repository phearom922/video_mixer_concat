"""Main application window."""
from pathlib import Path
from datetime import datetime, timezone
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QComboBox, QSpinBox, QTextEdit,
    QFileDialog, QMessageBox, QGroupBox, QFormLayout, QFrame, QDialog
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from app.ui.activation_window import ActivationWindow
from app.ui.update_dialog import UpdateDialog
from app.ui.widgets import ProgressWidget
from app.core.worker import VideoProcessingWorker
from app.core.grouper import SortMode, RemainderBehavior
from app.services.config_service import config_service
from app.services.license_guard import license_guard
from app.services.update_service import update_service
from app.services.logging_service import logger
from app import APP_VERSION


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.worker: VideoProcessingWorker = None
        self.setWindowTitle(f"Video Mixer Concat v{APP_VERSION}")
        self.setMinimumSize(900, 700)
        
        # Apply Dark Mode styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #e0e0e0;
            }
            QGroupBox {
                font-weight: 600;
                font-size: 14px;
                color: #e0e0e0;
                border: 2px solid #3a3a3a;
                border-radius: 10px;
                margin-top: 12px;
                padding-top: 16px;
                background-color: #2a2a2a;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px;
                background-color: #2a2a2a;
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
            }
            QLineEdit:disabled {
                background-color: #1a1a1a;
                color: #666666;
                border-color: #2a2a2a;
            }
            QPushButton {
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 14px;
                border: none;
                min-width: 120px;
            }
            QPushButton#startButton {
                background-color: #10b981;
                color: white;
            }
            QPushButton#startButton:hover {
                background-color: #059669;
            }
            QPushButton#startButton:pressed {
                background-color: #047857;
            }
            QPushButton#startButton:disabled {
                background-color: #374151;
                color: #6b7280;
            }
            QPushButton#cancelButton {
                background-color: #ef4444;
                color: white;
            }
            QPushButton#cancelButton:hover {
                background-color: #dc2626;
            }
            QPushButton#cancelButton:pressed {
                background-color: #b91c1c;
            }
            QPushButton#cancelButton:disabled {
                background-color: #374151;
                color: #6b7280;
            }
            QPushButton#browseButton {
                background-color: #6366f1;
                color: white;
                padding: 10px 20px;
                min-width: 100px;
            }
            QPushButton#browseButton:hover {
                background-color: #4f46e5;
            }
            QPushButton#browseButton:pressed {
                background-color: #4338ca;
            }
            QTextEdit {
                border: 2px solid #404040;
                border-radius: 8px;
                background-color: #1a1a1a;
                color: #d0d0d0;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
                padding: 8px;
            }
            QSpinBox, QComboBox {
                padding: 10px 14px;
                border: 2px solid #404040;
                border-radius: 8px;
                background-color: #252525;
                color: #e0e0e0;
                min-width: 150px;
                font-size: 13px;
                font-weight: 500;
            }
            QSpinBox:focus, QComboBox:focus {
                border-color: #6366f1;
                background-color: #2d2d2d;
            }
            QSpinBox:hover, QComboBox:hover {
                border-color: #525252;
                background-color: #2a2a2a;
            }
            QComboBox::drop-down {
                border: none;
                width: 35px;
                background-color: #3a3a3a;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
            }
            QComboBox::drop-down:hover {
                background-color: #4a4a4a;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #e0e0e0;
                width: 0;
                height: 0;
                margin-right: 8px;
            }
            QComboBox QAbstractItemView {
                background-color: #2a2a2a;
                border: 2px solid #404040;
                border-radius: 8px;
                color: #e0e0e0;
                selection-background-color: #6366f1;
                selection-color: white;
                padding: 4px;
                min-width: 150px;
            }
            QComboBox QAbstractItemView::item {
                padding: 8px 12px;
                border-radius: 4px;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #3a3a3a;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: #3a3a3a;
                border: none;
                border-radius: 6px;
                width: 25px;
                margin: 2px;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #4a4a4a;
            }
            QSpinBox::up-button:pressed, QSpinBox::down-button:pressed {
                background-color: #525252;
            }
            QSpinBox::up-arrow, QSpinBox::down-arrow {
                width: 0;
                height: 0;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
            }
            QSpinBox::up-arrow {
                border-bottom: 6px solid #e0e0e0;
                margin-bottom: 2px;
            }
            QSpinBox::down-arrow {
                border-top: 6px solid #e0e0e0;
                margin-top: 2px;
            }
            QFrame#licenseInfoFrame {
                background-color: #1e3a5f;
                border: 2px solid #3b82f6;
                border-radius: 10px;
                padding: 12px;
            }
        """)
        
        # Setup UI
        self._setup_ui()
        
        # Setup license validation timer (every 24 hours)
        self.validation_timer = QTimer()
        self.validation_timer.timeout.connect(self._check_license)
        self.validation_timer.start(24 * 60 * 60 * 1000)  # 24 hours
        
        # Check license on startup
        self._check_license()
        
        # Check for updates
        self._check_updates()
        
        # Update license info display
        self._update_license_info()
    
    def _setup_ui(self):
        """Setup the user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header with app title and license info
        header_layout = QHBoxLayout()
        title_label = QLabel(f"🎬 Video Mixer Concat v{APP_VERSION}")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #e0e0e0;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # License info frame
        self.license_info_frame = QFrame()
        self.license_info_frame.setObjectName("licenseInfoFrame")
        license_info_layout = QVBoxLayout()
        license_info_layout.setSpacing(6)
        license_info_layout.setContentsMargins(12, 12, 12, 12)
        
        # Status row
        status_layout = QHBoxLayout()
        status_layout.setSpacing(8)
        self.license_status_label = QLabel("🔒 License: Not Activated")
        self.license_status_label.setStyleSheet("font-weight: 600; color: #60a5fa; font-size: 12px;")
        status_layout.addWidget(self.license_status_label)
        status_layout.addStretch()
        license_info_layout.addLayout(status_layout)
        
        # Expiration row
        expires_layout = QHBoxLayout()
        expires_layout.setSpacing(8)
        self.license_expires_label = QLabel("📅 No expiration date")
        self.license_expires_label.setStyleSheet("color: #93c5fd; font-size: 11px;")
        expires_layout.addWidget(self.license_expires_label)
        expires_layout.addStretch()
        license_info_layout.addLayout(expires_layout)
        
        self.license_info_frame.setLayout(license_info_layout)
        header_layout.addWidget(self.license_info_frame)
        
        layout.addLayout(header_layout)
        
        # Input/Output folders
        folder_group = QGroupBox("📁 Folders")
        folder_layout = QFormLayout()
        folder_layout.setSpacing(12)
        
        self.input_folder_edit = QLineEdit()
        self.input_folder_edit.setReadOnly(True)
        self.input_folder_edit.textChanged.connect(self._on_input_folder_changed)
        input_browse = QPushButton("Browse...")
        input_browse.setObjectName("browseButton")
        input_browse.clicked.connect(self._browse_input_folder)
        input_layout = QHBoxLayout()
        input_layout.setSpacing(8)
        input_layout.addWidget(self.input_folder_edit)
        input_layout.addWidget(input_browse)
        
        # Label to show video count
        self.input_video_count_label = QLabel("(0 videos)")
        self.input_video_count_label.setStyleSheet("color: #9ca3af; font-style: italic; font-size: 11px;")
        folder_layout.addRow("Input Folder:", input_layout)
        folder_layout.addRow("", self.input_video_count_label)  # Empty label for spacing
        
        self.output_folder_edit = QLineEdit()
        self.output_folder_edit.setReadOnly(True)
        output_browse = QPushButton("Browse...")
        output_browse.setObjectName("browseButton")
        output_browse.clicked.connect(self._browse_output_folder)
        output_layout = QHBoxLayout()
        output_layout.setSpacing(8)
        output_layout.addWidget(self.output_folder_edit)
        output_layout.addWidget(output_browse)
        folder_layout.addRow("Output Folder:", output_layout)
        
        folder_group.setLayout(folder_layout)
        layout.addWidget(folder_group)
        
        # Settings
        settings_group = QGroupBox("⚙️ Settings")
        settings_layout = QFormLayout()
        settings_layout.setSpacing(12)
        
        self.group_size_spin = QSpinBox()
        self.group_size_spin.setMinimum(2)
        self.group_size_spin.setMaximum(100)
        self.group_size_spin.setValue(2)
        settings_layout.addRow("Group Size:", self.group_size_spin)
        
        self.sort_mode_combo = QComboBox()
        self.sort_mode_combo.addItems(["Filename", "Time", "Random"])
        settings_layout.addRow("Sort Mode:", self.sort_mode_combo)
        
        self.remainder_combo = QComboBox()
        self.remainder_combo.addItems(["Ignore", "Export Single", "Warn"])
        settings_layout.addRow("Remainder Behavior:", self.remainder_combo)
        
        self.naming_pattern_edit = QLineEdit()
        self.naming_pattern_edit.setText("group_{group}.mp4")
        self.naming_pattern_edit.setPlaceholderText("group_{group}.mp4 (use {group} and {count})")
        settings_layout.addRow("Output Naming:", self.naming_pattern_edit)
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
        
        # Progress
        self.progress_widget = ProgressWidget()
        layout.addWidget(self.progress_widget)
        
        # Log
        log_label = QLabel("📋 Processing Log:")
        log_label.setStyleSheet("font-weight: 600; color: #e0e0e0; font-size: 13px;")
        layout.addWidget(log_label)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        layout.addWidget(self.log_text)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        self.start_button = QPushButton("▶ Start Processing")
        self.start_button.setObjectName("startButton")
        self.start_button.clicked.connect(self._start_processing)
        self.cancel_button = QPushButton("⏹ Cancel")
        self.cancel_button.setObjectName("cancelButton")
        self.cancel_button.clicked.connect(self._cancel_processing)
        self.cancel_button.setEnabled(False)
        button_layout.addStretch()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        central_widget.setLayout(layout)
    
    def _browse_input_folder(self):
        """Browse for input folder."""
        folder = QFileDialog.getExistingDirectory(self, "Select Input Folder")
        if folder:
            self.input_folder_edit.setText(folder)
            self._update_video_count()
    
    def _on_input_folder_changed(self):
        """Handle input folder text change."""
        self._update_video_count()
    
    def _update_video_count(self):
        """Update the video count label."""
        folder_path = self.input_folder_edit.text()
        if not folder_path:
            self.input_video_count_label.setText("(0 videos)")
            return
        
        try:
            from app.core.grouper import scan_video_files
            folder = Path(folder_path)
            if folder.exists() and folder.is_dir():
                files = scan_video_files(folder)
                count = len(files)
                if count == 0:
                    self.input_video_count_label.setText("(0 videos)")
                elif count == 1:
                    self.input_video_count_label.setText("(1 video)")
                else:
                    self.input_video_count_label.setText(f"({count} videos)")
            else:
                self.input_video_count_label.setText("(Invalid folder)")
        except Exception as e:
            logger.error(f"Error scanning video files: {e}")
            self.input_video_count_label.setText("(Error scanning)")
    
    def _browse_output_folder(self):
        """Browse for output folder."""
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_folder_edit.setText(folder)
    
    def _start_processing(self):
        """Start video processing."""
        input_folder = self.input_folder_edit.text()
        output_folder = self.output_folder_edit.text()
        
        if not input_folder or not Path(input_folder).exists():
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Error")
            msg_box.setText("Please select a valid input folder")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #1e1e1e;
                    color: #e0e0e0;
                }
                QMessageBox QLabel {
                    color: #e0e0e0;
                    font-size: 14px;
                }
                QMessageBox QPushButton {
                    min-width: 120px;
                    padding: 12px 24px;
                    background-color: #6366f1;
                    color: white;
                    border-radius: 8px;
                    font-weight: 600;
                    font-size: 14px;
                }
                QMessageBox QPushButton:hover {
                    background-color: #4f46e5;
                }
            """)
            msg_box.exec()
            return
        
        if not output_folder or not Path(output_folder).exists():
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Error")
            msg_box.setText("Please select a valid output folder")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #1e1e1e;
                    color: #e0e0e0;
                }
                QMessageBox QLabel {
                    color: #e0e0e0;
                    font-size: 14px;
                }
                QMessageBox QPushButton {
                    min-width: 120px;
                    padding: 12px 24px;
                    background-color: #6366f1;
                    color: white;
                    border-radius: 8px;
                    font-weight: 600;
                    font-size: 14px;
                }
                QMessageBox QPushButton:hover {
                    background-color: #4f46e5;
                }
            """)
            msg_box.exec()
            return
        
        # Get settings
        group_size = self.group_size_spin.value()
        sort_mode_map = {
            0: SortMode.FILENAME,
            1: SortMode.TIME,
            2: SortMode.RANDOM
        }
        sort_mode = sort_mode_map[self.sort_mode_combo.currentIndex()]
        
        remainder_map = {
            0: RemainderBehavior.IGNORE,
            1: RemainderBehavior.EXPORT_SINGLE,
            2: RemainderBehavior.WARN
        }
        remainder_behavior = remainder_map[self.remainder_combo.currentIndex()]
        
        output_pattern = self.naming_pattern_edit.text() or "group_{group}.mp4"
        ffmpeg_path = config_service.get_ffmpeg_path()
        
        # Create worker
        self.worker = VideoProcessingWorker(
            Path(input_folder),
            Path(output_folder),
            group_size,
            sort_mode,
            remainder_behavior,
            output_pattern,
            ffmpeg_path
        )
        
        # Connect signals
        self.worker.progress.connect(self._on_progress)
        self.worker.group_complete.connect(self._on_group_complete)
        self.worker.finished.connect(self._on_finished)
        
        # Update UI
        self.start_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.log_text.clear()
        self.progress_widget.reset()
        
        # Start worker
        self.worker.start()
    
    def _cancel_processing(self):
        """Cancel video processing."""
        if self.worker and self.worker.isRunning():
            self.worker.cancel()
            self.worker.wait()
            self._log("Processing cancelled")
            self.start_button.setEnabled(True)
            self.cancel_button.setEnabled(False)
    
    def _on_progress(self, message: str):
        """Handle progress message."""
        self._log(message)
    
    def _on_group_complete(self, group_index: int, total: int, success: bool):
        """Handle group completion."""
        progress = int((group_index / total) * 100)
        self.progress_widget.set_progress(progress, f"Group {group_index}/{total}")
    
    def _on_finished(self, success: bool):
        """Handle processing finished."""
        self.start_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        
        if success:
            self.progress_widget.set_progress(100, "Processing complete!")
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle("Success")
            msg_box.setText("Video processing completed successfully!")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #1e1e1e;
                    color: #e0e0e0;
                }
                QMessageBox QLabel {
                    color: #e0e0e0;
                    font-size: 14px;
                }
                QMessageBox QPushButton {
                    min-width: 120px;
                    padding: 12px 24px;
                    background-color: #6366f1;
                    color: white;
                    border-radius: 8px;
                    font-weight: 600;
                    font-size: 14px;
                }
                QMessageBox QPushButton:hover {
                    background-color: #4f46e5;
                }
                QMessageBox QPushButton:pressed {
                    background-color: #4338ca;
                }
            """)
            msg_box.exec()
        else:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Warning")
            msg_box.setText("Processing completed with errors. Check the log for details.")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #1e1e1e;
                    color: #e0e0e0;
                }
                QMessageBox QLabel {
                    color: #e0e0e0;
                    font-size: 14px;
                }
                QMessageBox QPushButton {
                    min-width: 120px;
                    padding: 12px 24px;
                    background-color: #ef4444;
                    color: white;
                    border-radius: 8px;
                    font-weight: 600;
                    font-size: 14px;
                }
                QMessageBox QPushButton:hover {
                    background-color: #dc2626;
                }
                QMessageBox QPushButton:pressed {
                    background-color: #b91c1c;
                }
            """)
            msg_box.exec()
    
    def _log(self, message: str):
        """Add message to log."""
        self.log_text.append(message)
        logger.info(message)
    
    def _check_license(self):
        """Check license validity."""
        is_valid, reason = license_guard.is_license_valid()
        self._update_license_info()
        
        if not is_valid:
            # Show blocking dialog
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("License Validation Failed")
            msg.setText("Your license is not valid.")
            msg.setInformativeText(reason or "Please activate your license.")
            msg.setStandardButtons(QMessageBox.Ok)
            
            # Show activation window
            activation = ActivationWindow(self)
            if activation.exec() == QDialog.Accepted:
                # Retry validation
                self._check_license()
            else:
                # Exit if user cancels
                self.close()
    
    def _update_license_info(self):
        """Update license information display."""
        token = config_service.get_activation_token()
        if token:
            is_valid, reason = license_guard.is_license_valid()
            if is_valid:
                self.license_status_label.setText("✅ License: Active")
                self.license_status_label.setStyleSheet("font-weight: 600; color: #34d399; font-size: 12px;")
            else:
                self.license_status_label.setText("⚠️ License: Invalid")
                self.license_status_label.setStyleSheet("font-weight: 600; color: #f87171; font-size: 12px;")
            
            # Show expiration date
            expires_at = config_service.get_license_expires_at()
            if expires_at:
                try:
                    # Parse expiration date (handle both with and without timezone)
                    exp_str = expires_at.replace("Z", "+00:00")
                    exp_date = datetime.fromisoformat(exp_str)
                    
                    # Ensure both datetimes are timezone-aware
                    if exp_date.tzinfo is None:
                        exp_date = exp_date.replace(tzinfo=timezone.utc)
                    
                    # Use timezone-aware datetime for comparison
                    now = datetime.now(timezone.utc)
                    days_until = (exp_date - now).days
                    
                    if days_until > 0:
                        exp_text = f"📅 Expires: {exp_date.strftime('%B %d, %Y')} ({days_until} days remaining)"
                        self.license_expires_label.setText(exp_text)
                        if days_until <= 30:
                            self.license_expires_label.setStyleSheet("color: #f87171; font-size: 11px; font-weight: 600;")
                        else:
                            self.license_expires_label.setStyleSheet("color: #93c5fd; font-size: 11px;")
                    else:
                        self.license_expires_label.setText("⚠️ License Expired")
                        self.license_expires_label.setStyleSheet("color: #f87171; font-size: 11px; font-weight: 600;")
                except Exception as e:
                    logger.error(f"Error parsing expiration date: {e}")
                    self.license_expires_label.setText("📅 Expiration date unavailable")
                    self.license_expires_label.setStyleSheet("color: #9ca3af; font-size: 11px;")
            else:
                self.license_expires_label.setText("📅 No expiration date")
                self.license_expires_label.setStyleSheet("color: #9ca3af; font-size: 11px;")
        else:
            self.license_status_label.setText("🔒 License: Not Activated")
            self.license_status_label.setStyleSheet("font-weight: 600; color: #f87171; font-size: 12px;")
            self.license_expires_label.setText("📅 Please activate your license")
            self.license_expires_label.setStyleSheet("color: #9ca3af; font-size: 11px;")
    
    def _check_updates(self):
        """Check for app updates."""
        update_info = update_service.check_for_updates()
        if update_info:
            dialog = UpdateDialog(update_info, self)
            dialog.exec()
