from PyQt5.QtGui import QPainter, QPixmap
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
        
    def draw(self, painter):
        if self.background_image.isNull():
            return
            
        # Calculate scaling factors
        window_width = self.game_widget.width()
        window_height = self.game_widget.height()
        
        # Calculate scale to fit while maintaining aspect ratio
        scale_width = window_width / self.original_width
        scale_height = window_height / self.original_height
        scale = max(scale_width, scale_height)  # Use the larger scale to ensure full coverage
        
        # Calculate new dimensions
        new_width = int(self.original_width * scale)
        new_height = int(self.original_height * scale)
        
        # Calculate position to center the image
        x = (window_width - new_width) // 2
        y = (window_height - new_height) // 2
        
        # Draw the scaled background image
        painter.drawPixmap(x, y, new_width, new_height, self.background_image) 