from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import Qt
import os

class MenuBackground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.background = None
        self.load_background()
        
    def load_background(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        background_path = os.path.join(current_dir, "asset", "background", "menu_background.png")
        self.background = QPixmap(background_path)
        
    def paintEvent(self, event):
        if self.background and not self.background.isNull():
            painter = QPainter(self)
            # Calculate the scaled size to cover the widget while maintaining aspect ratio
            scaled_pixmap = self.background.scaled(
                self.size(),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )
            
            # Calculate the position to center the scaled pixmap
            x = (scaled_pixmap.width() - self.width()) // 2
            y = (scaled_pixmap.height() - self.height()) // 2
            
            # Draw the background
            painter.drawPixmap(-x, -y, scaled_pixmap) 