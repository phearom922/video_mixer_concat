"""Helper functions for loading and displaying SVG icons."""
from pathlib import Path
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import Qt


def get_icon_path(icon_name: str) -> Path:
    """Get the path to an icon file."""
    assets_path = Path(__file__).parent / "assets"
    return assets_path / f"icon_{icon_name}.svg"


def create_icon_label(icon_name: str, size: int = 16) -> QLabel:
    """
    Create a QLabel with an SVG icon.
    
    Args:
        icon_name: Name of the icon (without 'icon_' prefix and '.svg' extension)
        size: Size of the icon in pixels (default: 16)
    
    Returns:
        QLabel with the icon displayed
    """
    label = QLabel()
    set_icon_to_label(label, icon_name, size)
    return label


def set_icon_to_label(label: QLabel, icon_name: str, size: int = 16):
    """
    Set an SVG icon to an existing QLabel.
    
    Args:
        label: The QLabel to set the icon to
        icon_name: Name of the icon (without 'icon_' prefix and '.svg' extension)
        size: Size of the icon in pixels (default: 16)
    """
    icon_path = get_icon_path(icon_name)
    
    if icon_path.exists():
        # Load SVG and render to pixmap
        renderer = QSvgRenderer(str(icon_path))
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        
        label.setPixmap(pixmap)
        label.setFixedSize(size, size)
    else:
        # Fallback: clear label if icon not found
        label.setText("")
        label.setFixedSize(size, size)
