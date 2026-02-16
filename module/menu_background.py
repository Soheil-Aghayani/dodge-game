from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import Qt
import os

class MenuBackground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.background = None
        self._scaled_background = None
        self.load_background()
        
    def load_background(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        background_path = os.path.join(current_dir, "asset", "background", "menu_background.png")
        self.background = QPixmap(background_path)
        self._update_scaled_background()

    def _update_scaled_background(self):
        """Scale the background image to cover the widget while maintaining aspect ratio."""
        if self.background and not self.background.isNull() and not self.size().isEmpty():
            self._scaled_background = self.background.scaled(
                self.size(),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )
        else:
            self._scaled_background = None

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_scaled_background()

    def paintEvent(self, event):
        if self._scaled_background:
            painter = QPainter(self)
            
            # Calculate the position to center the scaled pixmap
            x = (self._scaled_background.width() - self.width()) // 2
            y = (self._scaled_background.height() - self.height()) // 2
            
            # Draw the background
            painter.drawPixmap(-x, -y, self._scaled_background)
