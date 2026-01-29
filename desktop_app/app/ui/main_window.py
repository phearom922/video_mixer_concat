"""Main application window."""
from pathlib import Path
from datetime import datetime, timezone
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QComboBox, QSpinBox, QTextEdit,
    QFileDialog, QMessageBox, QGroupBox, QFormLayout, QFrame, QDialog
)
from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtGui import QFont, QIcon
from PySide6.QtGui import QDesktopServices
from app.ui.icon_helper import set_icon_to_label, create_icon_label
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
        self.setMinimumSize(1000, 930)
        self.resize(1000, 930)  # Set initial size
        
        # Assets Path
        assets_path = Path(__file__).parent / "assets"
        arrow_up = (assets_path / "arrow_up.svg").as_posix()
        arrow_down = (assets_path / "arrow_down.svg").as_posix()
        
        # Set window icon
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
        
        # Apply Premium Dark Mode styling
        self.setStyleSheet(f"""
            /* Main Window */
            QMainWindow {{
                background-color: #0d1117;
            }}
            QWidget {{
                background-color: transparent;
                color: #e6edf3;
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            
            /* Modern Card-Style GroupBox with Pill-shaped Title */
            QGroupBox {{
                font-weight: bold;
                font-size: 13px;
                color: #ffffff;
                border: 1px solid #30363d;
                border-radius: 12px;
                margin-top: 24px;
                padding: 24px 16px 16px 16px;
                background-color: #161b22;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 12px;
                top: 10px;
                padding: 6px 16px;
                background-color: #238636;
                border-radius: 14px;
                color: #ffffff;
                font-size: 12px;
                min-height: 20px;
            }}
            
            /* Labels */
            QLabel {{
                color: #8b949e;
                font-size: 13px;
                background-color: transparent;
            }}
            
            /* Input Fields - Transparent Background */
            QLineEdit {{
                padding: 10px 14px;
                border: 1px solid #30363d;
                border-radius: 8px;
                background-color: transparent;
                color: #e6edf3;
                font-size: 13px;
                selection-background-color: #388bfd;
            }}
            QLineEdit:focus {{
                border: 1px solid #58a6ff;
            }}
            QLineEdit:hover {{
                border: 1px solid #484f58;
            }}
            QLineEdit:disabled {{
                color: #484f58;
                border: 1px solid #21262d;
            }}
            QLineEdit::placeholder {{
                color: #6e7681;
            }}
            
            /* Buttons Base */
            QPushButton {{
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
                border: none;
                min-width: 100px;
            }}
            
            /* Start Button - Green */
            QPushButton#startButton {{
                background-color: #238636;
                color: #ffffff;
            }}
            QPushButton#startButton:hover {{
                background-color: #2ea043;
            }}
            QPushButton#startButton:pressed {{
                background-color: #196c2e;
            }}
            QPushButton#startButton:disabled {{
                background-color: #1c3d2a;
                color: #4d8f5f;
            }}
            
            /* Cancel Button - Pink/Magenta */
            QPushButton#cancelButton {{
                background-color: #6e40c9;
                color: #ffffff;
                border: none;
            }}
            QPushButton#cancelButton:hover {{
                background-color: #8957e5;
            }}
            QPushButton#cancelButton:pressed {{
                background-color: #553098;
            }}
            QPushButton#cancelButton:disabled {{
                background-color: #2d2a4a;
                color: #6e6a99;
            }}
            
            /* Browse Button - Purple */
            QPushButton#browseButton {{
                background-color: #6e40c9;
                color: #ffffff;
                padding: 10px 16px;
                min-width: 90px;
            }}
            QPushButton#browseButton:hover {{
                background-color: #8957e5;
            }}
            QPushButton#browseButton:pressed {{
                background-color: #553098;
            }}
            
            /* Log TextEdit */
            QTextEdit {{
                border: 1px solid #30363d;
                border-radius: 8px;
                background-color: #0d1117;
                color: #7ee787;
                font-family: 'Cascadia Code', 'Consolas', monospace;
                font-size: 12px;
                padding: 10px;
                selection-background-color: #388bfd;
            }}
            
            /* Spinbox - Transparent Background */
            QSpinBox {{
                padding: 8px 12px;
                border: 1px solid #30363d;
                border-radius: 8px;
                background-color: transparent;
                color: #e6edf3;
                min-width: 120px;
                font-size: 13px;
            }}
            QSpinBox:focus {{
                border: 1px solid #58a6ff;
            }}
            QSpinBox:hover {{
                border: 1px solid #484f58;
            }}
            QSpinBox::up-button, QSpinBox::down-button {{
                background-color: transparent;
                border: none;
                width: 20px;
                border-radius: 4px;
                margin: 2px;
            }}
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
                background-color: #21262d;
            }}
            QSpinBox::up-arrow {{
                image: url({arrow_up});
                width: 12px;
                height: 12px;
            }}
            QSpinBox::down-arrow {{
                image: url({arrow_down});
                width: 12px;
                height: 12px;
            }}
            
            /* Combobox - Transparent Background */
            QComboBox {{
                padding: 8px 12px;
                border: 1px solid #30363d;
                border-radius: 8px;
                background-color: transparent;
                color: #e6edf3;
                min-width: 140px;
                font-size: 13px;
            }}
            QComboBox:focus {{
                border: 1px solid #58a6ff;
            }}
            QComboBox:hover {{
                border: 1px solid #484f58;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
                background-color: transparent;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
            }}
            QComboBox::down-arrow {{
                image: url({arrow_down});
                width: 14px;
                height: 14px;
                padding-right: 10px;
            }}
            QComboBox QAbstractItemView {{
                background-color: #161b22;
                border: 1px solid #30363d;
                border-radius: 8px;
                color: #e6edf3;
                selection-background-color: #388bfd;
                selection-color: #ffffff;
                padding: 4px;
                outline: none;
            }}
            QComboBox QAbstractItemView::item {{
                padding: 8px 12px;
                border-radius: 4px;
                min-height: 24px;
            }}
            QComboBox QAbstractItemView::item:hover {{
                background-color: #21262d;
            }}
            
            /* Settings GroupBox - Purple Badge */
            QGroupBox#settingsGroup::title {{
                background-color: #6e40c9;
            }}
            
            /* License Info Frame */
            QFrame#licenseInfoFrame {{
                background-color: #0d1117;
                border: 1px solid #238636;
                border-radius: 10px;
                padding: 8px;
            }}
            
            /* Scrollbar */
            QScrollBar:vertical {{
                background-color: #0d1117;
                width: 10px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background-color: #30363d;
                border-radius: 5px;
                min-height: 30px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: #484f58;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0;
            }}
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
        central_widget.setStyleSheet("background-color: #0d1117;")
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Header with app title and license info
        header_layout = QHBoxLayout()
        header_layout.setSpacing(16)
        
        # App icon and title container
        title_container = QHBoxLayout()
        title_container.setSpacing(14)
        
        # Icon label
        icon_label = QLabel("🎬")
        icon_label.setStyleSheet("font-size: 36px;")
        title_container.addWidget(icon_label)
        
        # Title and subtitle
        title_text = QVBoxLayout()
        title_text.setSpacing(4)
        
        title_label = QLabel("Video Mixer Concat")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #ffffff;
        """)
        
        version_label = QLabel(f"v{APP_VERSION}")
        version_label.setStyleSheet("""
            font-size: 12px;
            font-weight: bold;
            color: #8957e5;
        """)
        
        title_text.addWidget(title_label)
        title_text.addWidget(version_label)
        title_container.addLayout(title_text)
        
        header_layout.addLayout(title_container)
        header_layout.addStretch()
        
        # License info frame
        self.license_info_frame = QFrame()
        self.license_info_frame.setObjectName("licenseInfoFrame")
        self.license_info_frame.setMinimumWidth(300)
        license_info_layout = QVBoxLayout()
        license_info_layout.setSpacing(6)
        license_info_layout.setContentsMargins(16, 12, 16, 12)
        
        # Status row with icon
        status_row = QHBoxLayout()
        status_row.setSpacing(6)
        status_row.setContentsMargins(0, 0, 0, 0)
        self.license_status_icon = create_icon_label("key", 16)
        self.license_status_label = QLabel("License: Not Activated")
        self.license_status_label.setStyleSheet("""
            font-weight: bold;
            color: #3fb950;
            font-size: 13px;
        """)
        status_row.addWidget(self.license_status_icon)
        status_row.addWidget(self.license_status_label)
        status_row.addStretch()
        license_info_layout.addLayout(status_row)
        
        # Expiration row with icon
        expires_row = QHBoxLayout()
        expires_row.setSpacing(6)
        expires_row.setContentsMargins(0, 0, 0, 0)
        self.license_expires_icon = create_icon_label("calendar", 14)
        self.license_expires_label = QLabel("No expiration date")
        self.license_expires_label.setStyleSheet("""
            color: #8b949e;
            font-size: 12px;
        """)
        expires_row.addWidget(self.license_expires_icon)
        expires_row.addWidget(self.license_expires_label)
        expires_row.addStretch()
        license_info_layout.addLayout(expires_row)
        
        self.license_info_frame.setLayout(license_info_layout)
        header_layout.addWidget(self.license_info_frame)
        
        layout.addLayout(header_layout)
        
        # Input/Output folders
        folder_group = QGroupBox("Folders")
        folder_layout = QFormLayout()
        folder_layout.setSpacing(12)
        folder_layout.setContentsMargins(16, 20, 16, 16)
        folder_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        # Input folder
        input_label = QLabel("Input Folder:")
        input_label.setStyleSheet("color: #c9d1d9; font-weight: bold;")
        
        self.input_folder_edit = QLineEdit()
        self.input_folder_edit.setReadOnly(True)
        self.input_folder_edit.setPlaceholderText("Select folder containing video files...")
        self.input_folder_edit.textChanged.connect(self._on_input_folder_changed)
        
        input_browse = QPushButton("Browse...")
        input_browse.setObjectName("browseButton")
        input_browse.setStyleSheet("""
            QPushButton {
                background-color: #6e40c9;
                color: #ffffff;
                padding: 10px 16px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
                border: none;
                min-width: 90px;
            }
            QPushButton:hover {
                background-color: #8957e5;
            }
            QPushButton:pressed {
                background-color: #553098;
            }
        """)
        input_browse.clicked.connect(self._browse_input_folder)
        
        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)
        input_layout.addWidget(self.input_folder_edit, 1)
        input_layout.addWidget(input_browse)
        
        # Video count label with icon
        video_count_row = QHBoxLayout()
        video_count_row.setSpacing(6)
        video_count_row.setContentsMargins(0, 0, 0, 0)
        self.input_video_count_icon = create_icon_label("video", 12)
        self.input_video_count_label = QLabel("0 videos found")
        self.input_video_count_label.setStyleSheet("color: #6e7681; font-size: 11px; font-style: italic;")
        video_count_row.addWidget(self.input_video_count_icon)
        video_count_row.addWidget(self.input_video_count_label)
        video_count_row.addStretch()
        video_count_widget = QWidget()
        video_count_widget.setLayout(video_count_row)
        
        folder_layout.addRow(input_label, input_layout)
        folder_layout.addRow("", video_count_widget)
        
        # Output folder
        output_label = QLabel("Output Folder:")
        output_label.setStyleSheet("color: #c9d1d9; font-weight: bold;")
        
        self.output_folder_edit = QLineEdit()
        self.output_folder_edit.setReadOnly(True)
        self.output_folder_edit.setPlaceholderText("Select folder for output files...")
        
        output_browse = QPushButton("Browse...")
        output_browse.setObjectName("browseButton")
        output_browse.setStyleSheet("""
            QPushButton {
                background-color: #6e40c9;
                color: #ffffff;
                padding: 10px 16px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
                border: none;
                min-width: 90px;
            }
            QPushButton:hover {
                background-color: #8957e5;
            }
            QPushButton:pressed {
                background-color: #553098;
            }
        """)
        output_browse.clicked.connect(self._browse_output_folder)
        
        output_open_folder = QPushButton("Open Folder")
        output_open_folder.setObjectName("browseButton")
        output_open_folder.setStyleSheet("""
            QPushButton {
                background-color: #6e40c9;
                color: #ffffff;
                padding: 10px 16px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
                border: none;
                min-width: 90px;
            }
            QPushButton:hover {
                background-color: #8957e5;
            }
            QPushButton:pressed {
                background-color: #553098;
            }
            QPushButton:disabled {
                background-color: #2d2a4a;
                color: #6e6a99;
            }
        """)
        output_open_folder.clicked.connect(self._open_output_folder)
        output_open_folder.setEnabled(False)  # Disabled until folder is selected
        self.output_open_folder_button = output_open_folder  # Store reference
        
        # Enable/disable Open Folder button when output folder changes
        self.output_folder_edit.textChanged.connect(self._on_output_folder_changed)
        
        output_layout = QHBoxLayout()
        output_layout.setSpacing(10)
        output_layout.addWidget(self.output_folder_edit, 1)
        output_layout.addWidget(output_browse)
        output_layout.addWidget(output_open_folder)
        
        folder_layout.addRow(output_label, output_layout)
        folder_group.setLayout(folder_layout)
        layout.addWidget(folder_group)
        
        # Settings - Use object name for styling
        settings_group = QGroupBox("Settings")
        settings_group.setObjectName("settingsGroup")
        settings_layout = QFormLayout()
        settings_layout.setSpacing(12)  # Match Folders section
        settings_layout.setContentsMargins(16, 20, 16, 16)  # Match Folders section
        settings_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        # Group Size
        group_size_label = QLabel("Group Size:")
        group_size_label.setStyleSheet("color: #c9d1d9; font-weight: bold;")
        self.group_size_spin = QSpinBox()
        self.group_size_spin.setMinimum(2)
        self.group_size_spin.setMaximum(100)
        self.group_size_spin.setValue(2)
        settings_layout.addRow(group_size_label, self.group_size_spin)
        
        # Sort Mode
        sort_mode_label = QLabel("Sort Mode:")
        sort_mode_label.setStyleSheet("color: #c9d1d9; font-weight: bold;")
        self.sort_mode_combo = QComboBox()
        self.sort_mode_combo.addItems(["Filename", "Time", "Random"])
        settings_layout.addRow(sort_mode_label, self.sort_mode_combo)
        
        # Remainder
        remainder_label = QLabel("Remainder:")
        remainder_label.setStyleSheet("color: #c9d1d9; font-weight: bold;")
        self.remainder_combo = QComboBox()
        self.remainder_combo.addItems(["Ignore", "Export Single", "Warn"])
        settings_layout.addRow(remainder_label, self.remainder_combo)
        
        # Output Naming
        naming_label = QLabel("Output Naming:")
        naming_label.setStyleSheet("color: #c9d1d9; font-weight: bold;")
        self.naming_pattern_edit = QLineEdit()
        self.naming_pattern_edit.setText("group_{group}.mp4")
        self.naming_pattern_edit.setPlaceholderText("group_{group}.mp4")
        settings_layout.addRow(naming_label, self.naming_pattern_edit)
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
        
        # Progress
        self.progress_widget = ProgressWidget()
        layout.addWidget(self.progress_widget)
        
        # Log section
        log_header = QHBoxLayout()
        log_label = QLabel("📋 Processing Log")
        log_label.setStyleSheet("color: #ffffff; font-weight: bold; font-size: 13px;")
        log_header.addWidget(log_label)
        log_header.addStretch()
        layout.addLayout(log_header)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(120)
        self.log_text.setPlaceholderText("Processing output will appear here...")
        layout.addWidget(self.log_text)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        self.start_button = QPushButton("▶  Start Processing")
        self.start_button.setObjectName("startButton")
        self.start_button.setMinimumHeight(44)
        self.start_button.setMinimumWidth(160)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #238636;
                color: #ffffff;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2ea043;
            }
            QPushButton:pressed {
                background-color: #196c2e;
            }
            QPushButton:disabled {
                background-color: #1c3d2a;
                color: #4d8f5f;
            }
        """)
        self.start_button.clicked.connect(self._start_processing)
        
        self.cancel_button = QPushButton("⏹  Cancel")
        self.cancel_button.setObjectName("cancelButton")
        self.cancel_button.setMinimumHeight(44)
        self.cancel_button.setMinimumWidth(120)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #da3633;
                color: #ffffff;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
                border: none;
            }
            QPushButton:hover {
                background-color: #f85149;
            }
            QPushButton:pressed {
                background-color: #b62324;
            }
            QPushButton:disabled {
                background-color: #3d1a1a;
                color: #8b5454;
            }
        """)
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
            set_icon_to_label(self.input_video_count_icon, "video", 12)
            self.input_video_count_label.setText("0 videos found")
            self.input_video_count_label.setStyleSheet("color: #6e7681; font-size: 11px; font-style: italic;")
            return
        
        try:
            from app.core.grouper import scan_video_files
            folder = Path(folder_path)
            if folder.exists() and folder.is_dir():
                files = scan_video_files(folder)
                count = len(files)
                if count == 0:
                    set_icon_to_label(self.input_video_count_icon, "video", 12)
                    self.input_video_count_label.setText("No videos found")
                    self.input_video_count_label.setStyleSheet("color: #f85149; font-size: 11px;")
                elif count == 1:
                    set_icon_to_label(self.input_video_count_icon, "video", 12)
                    self.input_video_count_label.setText("1 video found")
                    self.input_video_count_label.setStyleSheet("color: #3fb950; font-size: 11px; font-weight: bold;")
                else:
                    set_icon_to_label(self.input_video_count_icon, "video", 12)
                    self.input_video_count_label.setText(f"{count} videos found")
                    self.input_video_count_label.setStyleSheet("color: #3fb950; font-size: 11px; font-weight: bold;")
            else:
                set_icon_to_label(self.input_video_count_icon, "warning", 12)
                self.input_video_count_label.setText("Invalid folder")
                self.input_video_count_label.setStyleSheet("color: #f85149; font-size: 11px;")
        except Exception as e:
            logger.error(f"Error scanning video files: {e}")
            set_icon_to_label(self.input_video_count_icon, "warning", 12)
            self.input_video_count_label.setText("Error scanning")
            self.input_video_count_label.setStyleSheet("color: #f85149; font-size: 11px;")
    
    def _browse_output_folder(self):
        """Browse for output folder."""
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_folder_edit.setText(folder)
    
    def _open_output_folder(self):
        """Open output folder in file explorer."""
        output_folder = self.output_folder_edit.text()
        if output_folder and Path(output_folder).exists():
            # Open folder in file explorer
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(Path(output_folder).absolute())))
        else:
            self._show_message("Error", "Output folder does not exist", QMessageBox.Warning)
    
    def _on_output_folder_changed(self):
        """Enable/disable Open Folder button based on folder path."""
        output_folder = self.output_folder_edit.text()
        if hasattr(self, 'output_open_folder_button'):
            self.output_open_folder_button.setEnabled(
                bool(output_folder) and Path(output_folder).exists()
            )
    
    def _start_processing(self):
        """Start video processing."""
        input_folder = self.input_folder_edit.text()
        output_folder = self.output_folder_edit.text()
        
        if not input_folder or not Path(input_folder).exists():
            self._show_message("Error", "Please select a valid input folder", QMessageBox.Warning)
            return
        
        if not output_folder or not Path(output_folder).exists():
            self._show_message("Error", "Please select a valid output folder", QMessageBox.Warning)
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
    
    def _show_message(self, title: str, text: str, icon=QMessageBox.Information):
        """Show a styled message box."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #161b22;
            }
            QMessageBox QLabel {
                color: #e6edf3;
                font-size: 13px;
            }
            QMessageBox QPushButton {
                min-width: 100px;
                padding: 8px 20px;
                background-color: #238636;
                color: #ffffff;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
                border: none;
            }
            QMessageBox QPushButton:hover {
                background-color: #2ea043;
            }
        """)
        msg_box.exec()
    
    def _cancel_processing(self):
        """Cancel video processing."""
        if self.worker and self.worker.isRunning():
            self.worker.cancel()
            self.worker.wait()
            self._log("⏹ Processing cancelled")
            self.start_button.setEnabled(True)
            self.cancel_button.setEnabled(False)
    
    def _on_progress(self, message: str):
        """Handle progress message."""
        self._log(message)
    
    def _on_group_complete(self, group_index: int, total: int, success: bool):
        """Handle group completion."""
        progress = int((group_index / total) * 100)
        self.progress_widget.set_progress(progress, f"Processing group {group_index} of {total}")
    
    def _on_finished(self, success: bool):
        """Handle processing finished."""
        self.start_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        
        if success:
            self.progress_widget.set_progress(100, "Processing complete!")
            self._show_message("Success", "Video processing completed successfully!")
        else:
            self._show_message("Warning", "Processing completed with errors. Check the log.", QMessageBox.Warning)
    
    def _log(self, message: str):
        """Add message to log."""
        self.log_text.append(message)
        logger.info(message)
    
    def _check_license(self):
        """Check license validity."""
        is_valid, reason = license_guard.is_license_valid()
        self._update_license_info()
        
        if not is_valid:
            activation = ActivationWindow(self)
            if activation.exec() == QDialog.Accepted:
                self._check_license()
            else:
                self.close()
    
    def _update_license_info(self):
        """Update license information display."""
        token = config_service.get_activation_token()
        if token:
            is_valid, reason = license_guard.is_license_valid()
            if is_valid:
                set_icon_to_label(self.license_status_icon, "check", 16)
                self.license_status_label.setText("License: Active")
                self.license_status_label.setStyleSheet("font-weight: bold; color: #3fb950; font-size: 13px;")
                self.license_info_frame.setStyleSheet("""
                    QFrame#licenseInfoFrame {
                        background-color: #0d1117;
                        border: 1px solid #238636;
                        border-radius: 10px;
                        padding: 8px;
                    }
                """)
            else:
                set_icon_to_label(self.license_status_icon, "warning", 16)
                self.license_status_label.setText("License: Invalid")
                self.license_status_label.setStyleSheet("font-weight: bold; color: #f85149; font-size: 13px;")
                self.license_info_frame.setStyleSheet("""
                    QFrame#licenseInfoFrame {
                        background-color: #0d1117;
                        border: 1px solid #f85149;
                        border-radius: 10px;
                        padding: 8px;
                    }
                """)
            
            expires_at = config_service.get_license_expires_at()
            if expires_at:
                try:
                    exp_str = expires_at.replace("Z", "+00:00")
                    exp_date = datetime.fromisoformat(exp_str)
                    if exp_date.tzinfo is None:
                        exp_date = exp_date.replace(tzinfo=timezone.utc)
                    now = datetime.now(timezone.utc)
                    days_until = (exp_date - now).days
                    
                    if days_until > 0:
                        set_icon_to_label(self.license_expires_icon, "calendar", 14)
                        self.license_expires_label.setText(
                            f"Expires: {exp_date.strftime('%B %d, %Y')} ({days_until} days remaining)"
                        )
                        if days_until <= 30:
                            self.license_expires_label.setStyleSheet("color: #d29922; font-size: 12px; font-weight: bold;")
                        else:
                            self.license_expires_label.setStyleSheet("color: #8b949e; font-size: 12px;")
                    else:
                        set_icon_to_label(self.license_expires_icon, "warning", 14)
                        self.license_expires_label.setText("License Expired")
                        self.license_expires_label.setStyleSheet("color: #f85149; font-size: 12px; font-weight: bold;")
                except Exception as e:
                    logger.error(f"Error parsing expiration date: {e}")
                    set_icon_to_label(self.license_expires_icon, "calendar", 14)
                    self.license_expires_label.setText("Expiration unavailable")
                    self.license_expires_label.setStyleSheet("color: #6e7681; font-size: 12px;")
            else:
                set_icon_to_label(self.license_expires_icon, "calendar", 14)
                self.license_expires_label.setText("No expiration date")
                self.license_expires_label.setStyleSheet("color: #6e7681; font-size: 12px;")
        else:
            set_icon_to_label(self.license_status_icon, "key", 16)
            self.license_status_label.setText("License: Not Activated")
            self.license_status_label.setStyleSheet("font-weight: bold; color: #f85149; font-size: 13px;")
            set_icon_to_label(self.license_expires_icon, "calendar", 14)
            self.license_expires_label.setText("Please activate your license")
            self.license_expires_label.setStyleSheet("color: #6e7681; font-size: 12px;")
            self.license_info_frame.setStyleSheet("""
                QFrame#licenseInfoFrame {
                    background-color: #0d1117;
                    border: 1px solid #f85149;
                    border-radius: 10px;
                    padding: 8px;
                }
            """)
    
    def _check_updates(self, force: bool = True):
        """Check for app updates."""
        try:
            update_info = update_service.check_for_updates(force=force)
            if update_info:
                logger.info(f"Update available: {update_info.get('latest_version')}")
                dialog = UpdateDialog(update_info, self)
                dialog.exec()
            else:
                logger.info("No update available or update check returned None")
        except Exception as e:
            logger.error(f"Error checking for updates: {e}")
