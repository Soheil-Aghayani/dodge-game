from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap
import os

class HealthSystem:
    def __init__(self, game_widget):
        self.game_widget = game_widget
        self.max_health = 3
        self.current_health = self.max_health
        self.is_invincible = False
        self.invincibility_timer = QTimer()
        self.invincibility_timer.timeout.connect(self._end_invincibility)
        self.invincibility_duration = 3000  # 3 seconds in milliseconds
        self.blink_interval = 200  # Blink every 200ms
        self.is_visible = True  # For blinking effect
        
        # Load heart images
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "asset", "ui")
        self.heart_images = {
            0: QPixmap(os.path.join(ui_path, "0.png")),
            1: QPixmap(os.path.join(ui_path, "1.png")),
            2: QPixmap(os.path.join(ui_path, "2.png")),
            3: QPixmap(os.path.join(ui_path, "3.png"))
        }
        
        # Scale images if needed
        for health, pixmap in self.heart_images.items():
            if not pixmap.isNull():
                self.heart_images[health] = pixmap.scaled(100, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        # Blink timer for invincibility visual feedback
        self.blink_timer = QTimer()
        self.blink_timer.timeout.connect(self._toggle_visibility)
        
    def take_damage(self):
        """Try to deal damage to the player. Returns True if damage was dealt."""
        if self.is_invincible:
            return False
            
        self.current_health -= 1
        if self.current_health <= 0:
            self.current_health = 0
            return True
            
        # Start invincibility period
        self.start_invincibility()
        return True
        
    def start_invincibility(self):
        """Start the invincibility period with blinking effect."""
        self.is_invincible = True
        self.invincibility_timer.start(self.invincibility_duration)
        self.blink_timer.start(self.blink_interval)
        
    def _end_invincibility(self):
        """End the invincibility period."""
        self.is_invincible = False
        self.invincibility_timer.stop()
        self.blink_timer.stop()
        self.is_visible = True
        
    def _toggle_visibility(self):
        """Toggle visibility for blinking effect."""
        self.is_visible = not self.is_visible
        
    def reset(self):
        """Reset health to maximum."""
        self.current_health = self.max_health
        self.is_invincible = False
        self.invincibility_timer.stop()
        self.blink_timer.stop()
        self.is_visible = True
        
    def draw(self, painter):
        """Draw the health indicator."""
        if not self.is_visible:
            return
            
        # Draw the appropriate heart image based on current health
        heart_image = self.heart_images.get(self.current_health)
        if heart_image and not heart_image.isNull():
            painter.drawPixmap(10, 50, heart_image)
            
    def is_game_over(self):
        """Check if player has run out of health."""
        return self.current_health <= 0 