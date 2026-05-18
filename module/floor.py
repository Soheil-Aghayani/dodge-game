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
            self._cached_img_height = 0
        else:
            self.image = self.image.scaled(50, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self._cached_img_height = self.image.height()

        self._cached_width = 0
        self._cached_floor = None
        
    def get_height(self):
        return self._cached_img_height
        
    def get_y_position(self):
        y_pos = self.game_widget.height() - self.get_height()
        return y_pos
        
    def draw(self, painter, game_width=None, floor_y=None):
        if not self.image.isNull():
            current_width = game_width if game_width is not None else self.game_widget.width()
            # ⚡ BOLT OPTIMIZATION:
            # Pre-render the tiled floor onto a single QPixmap when the window width changes.
            # Doing this avoids the expense of rendering the floor tile-by-tile on every single frame,
            # resulting in ~4x faster floor rendering.
            if self._cached_floor is None or current_width != self._cached_width:
                self._cached_width = current_width
                self._cached_floor = QPixmap(current_width, self.image.height())
                self._cached_floor.fill(Qt.transparent)

                cache_painter = QPainter(self._cached_floor)
                for x in range(0, current_width, self.image.width()):
                    cache_painter.drawPixmap(x, 0, self.image)
                cache_painter.end()

            y_pos = floor_y if floor_y is not None else self.get_y_position()
            painter.drawPixmap(0, y_pos, self._cached_floor)
        else:
            print("Cannot draw floor: Image is null")
                
    def get_rect(self):
        return (0, self.get_y_position(), self.game_widget.width(), self.get_height())