from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPixmap, QPainter
import os

class Floor:
    def __init__(self, game_widget):
        self.game_widget = game_widget
        # Get the absolute path to the floor image
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "asset", "block", "floor.png")
        
        self.image = QPixmap(image_path)
        if self.image.isNull():
            print("Error: Could not load floor.png")
        else:
            self.image = self.image.scaled(50, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
    def get_height(self):
        height = self.image.height() if not self.image.isNull() else 0
        return height
        
    def get_y_position(self):
        y_pos = self.game_widget.height() - self.get_height()
        return y_pos
        
    def draw(self, painter):
        if not self.image.isNull():
            for x in range(0, self.game_widget.width(), self.image.width()):
                painter.drawPixmap(x, self.get_y_position(), self.image)
        else:
            print("Cannot draw floor: Image is null")
                
    def get_rect(self):
        return QRect(0, self.get_y_position(), self.game_widget.width(), self.get_height()) 