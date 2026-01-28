"""Reusable UI widgets."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt


class ProgressWidget(QWidget):
    """Widget for displaying progress."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.setSpacing(8)
        
        self.label = QLabel("Ready")
        self.label.setStyleSheet("color: #d0d0d0; font-size: 13px; font-weight: 500;")
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #404040;
                border-radius: 8px;
                background-color: #1a1a1a;
                text-align: center;
                color: #e0e0e0;
                font-weight: 600;
                height: 28px;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6366f1, stop:1 #8b5cf6);
                border-radius: 6px;
            }
        """)
        
        layout.addWidget(self.label)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)
    
    def set_progress(self, value: int, text: str = ""):
        """Set progress value and optional text."""
        self.progress_bar.setValue(value)
        if text:
            self.label.setText(text)
    
    def reset(self):
        """Reset progress."""
        self.progress_bar.setValue(0)
        self.label.setText("Ready")
