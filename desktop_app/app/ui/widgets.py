"""Reusable UI widgets."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt
from app.ui.icon_helper import set_icon_to_label, create_icon_label


class ProgressWidget(QWidget):
    """Widget for displaying progress with modern styling."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(0, 8, 0, 8)
        
        # Status header
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)
        
        self.status_icon = create_icon_label("hourglass", 14)
        header_layout.addWidget(self.status_icon)
        
        self.label = QLabel("Ready to process")
        self.label.setStyleSheet("""
            color: #e6edf3;
            font-size: 13px;
            font-weight: bold;
            background: transparent;
        """)
        header_layout.addWidget(self.label)
        header_layout.addStretch()
        
        # Percentage label
        self.percent_label = QLabel("0%")
        self.percent_label.setStyleSheet("""
            color: #8957e5;
            font-size: 13px;
            font-weight: bold;
            background: transparent;
        """)
        header_layout.addWidget(self.percent_label)
        
        layout.addLayout(header_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(12)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 6px;
                background-color: #21262d;
            }
            QProgressBar::chunk {
                background-color: #8957e5;
                border-radius: 6px;
            }
        """)
        
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)
    
    def set_progress(self, value: int, text: str = ""):
        """Set progress value and optional text."""
        self.progress_bar.setValue(value)
        self.percent_label.setText(f"{value}%")
        
        if text:
            self.label.setText(text)
        
        # Update styling based on progress
        if value == 0:
            set_icon_to_label(self.status_icon, "hourglass", 14)
            self.percent_label.setStyleSheet("color: #8957e5; font-size: 13px; font-weight: bold; background: transparent;")
            self.progress_bar.setStyleSheet("""
                QProgressBar {
                    border: none;
                    border-radius: 6px;
                    background-color: #21262d;
                }
                QProgressBar::chunk {
                    background-color: #8957e5;
                    border-radius: 6px;
                }
            """)
        elif value < 100:
            set_icon_to_label(self.status_icon, "lightning", 14)
            self.percent_label.setStyleSheet("color: #58a6ff; font-size: 13px; font-weight: bold; background: transparent;")
            self.progress_bar.setStyleSheet("""
                QProgressBar {
                    border: none;
                    border-radius: 6px;
                    background-color: #21262d;
                }
                QProgressBar::chunk {
                    background-color: #58a6ff;
                    border-radius: 6px;
                }
            """)
        else:
            set_icon_to_label(self.status_icon, "check", 14)
            self.percent_label.setStyleSheet("color: #3fb950; font-size: 13px; font-weight: bold; background: transparent;")
            self.progress_bar.setStyleSheet("""
                QProgressBar {
                    border: none;
                    border-radius: 6px;
                    background-color: #21262d;
                }
                QProgressBar::chunk {
                    background-color: #3fb950;
                    border-radius: 6px;
                }
            """)
    
    def reset(self):
        """Reset progress."""
        self.progress_bar.setValue(0)
        self.percent_label.setText("0%")
        self.label.setText("Ready to process")
        set_icon_to_label(self.status_icon, "hourglass", 14)
        self.percent_label.setStyleSheet("color: #8957e5; font-size: 13px; font-weight: bold; background: transparent;")
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 6px;
                background-color: #21262d;
            }
            QProgressBar::chunk {
                background-color: #8957e5;
                border-radius: 6px;
            }
        """)
