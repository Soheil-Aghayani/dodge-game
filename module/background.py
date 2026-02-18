from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import Qt
import os

class Background:
    def __init__(self, game_widget):
        self.game_widget = game_widget
        # Get the absolute path to the background image
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "asset", "background", "warehouse.png")
        
        # Load the warehouse background image
        self.background_image = QPixmap(image_path)
        # Debug: Check if image loaded successfully
        if self.background_image.isNull():
            print("Error: Background image failed to load!")
            print(f"Tried to load from path: {image_path}")
            # Try alternative path
            alt_path = os.path.join(os.getcwd(), "Game", "dodge_game", "asset", "background", "warehouse.png")
            print(f"Trying alternative path: {alt_path}")
            self.background_image = QPixmap(alt_path)
            if not self.background_image.isNull():
                print("Successfully loaded from alternative path!")
            
        # Store original dimensions
        self.original_width = self.background_image.width()
        self.original_height = self.background_image.height()
        
        # Cached scaled background
        self.scaled_background = None
        self.scaled_x = 0
        self.scaled_y = 0

    def resize(self, window_width, window_height):
        if self.background_image.isNull():
            return
            
        # Scale the image to cover the window while preserving aspect ratio
        self.scaled_background = self.background_image.scaled(
            window_width, window_height,
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )
        
        # Calculate position to center the image
        self.scaled_x = (window_width - self.scaled_background.width()) // 2
        self.scaled_y = (window_height - self.scaled_background.height()) // 2
        
    def draw(self, painter):
        if self.background_image.isNull():
            return

        # If scaled background hasn't been created yet, create it now
        if self.scaled_background is None:
            self.resize(self.game_widget.width(), self.game_widget.height())

        # Draw the cached scaled background image
        painter.drawPixmap(self.scaled_x, self.scaled_y, self.scaled_background)
