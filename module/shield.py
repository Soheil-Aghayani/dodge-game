from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPixmap, QTransform
import os
from PyQt5.Qt import Qt

class Shield:
    # Cache pre-scaled shield images based on size to avoid expensive scaling every frame
    _scaled_images_cache = {}

    def __init__(self, player):
        self.player = player
        # Load shield image
        current_dir = os.path.dirname(os.path.abspath(__file__))
        shield_path = os.path.join(current_dir, "asset", "shield", "1.png")
        self.image = QPixmap(shield_path)
        
        # Shield should be 20% larger than player
        self.width = int(player.width * 1.5)
        self.height = int(player.height * 1.5)

        # Pre-scale shield to correct size and cache it
        cache_key = (self.width, self.height)
        if cache_key not in Shield._scaled_images_cache and not self.image.isNull():
            scaled_shield = self.image.scaled(
                self.width, self.height,
                Qt.KeepAspectRatio, Qt.FastTransformation
            )
            Shield._scaled_images_cache[cache_key] = scaled_shield

        self.scaled_shield = Shield._scaled_images_cache.get(cache_key)
            
    def get_rect(self):
        # Center the shield hitbox around the player
        x_offset = (self.width - self.player.width) // 2
        y_offset = (self.height - self.player.height) // 2
        return QRect(
            int(self.player.x - x_offset),
            int(self.player.y - y_offset),
            self.width,
            self.height
        )
        
    def draw(self, painter):
        if self.scaled_shield is not None:
            # Only draw if health system says we're visible (for blinking effect)
            if not hasattr(self.player.game_widget, 'health_system') or \
               self.player.game_widget.health_system.is_visible:
                # Center shield around player
                x_offset = (self.width - self.player.width) // 2
                y_offset = (self.height - self.player.height) // 2
                
                painter.setOpacity(0.7)  # Make shield semi-transparent
                painter.drawPixmap(
                    int(self.player.x - x_offset),
                    int(self.player.y - y_offset),
                    self.scaled_shield
                )
                painter.setOpacity(1.0)  # Reset opacity