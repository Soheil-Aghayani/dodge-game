from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPixmap, QTransform, QPainter
import os
from PyQt5.Qt import Qt

class Shield:
    def __init__(self, player):
        self.player = player
        # Load shield image
        current_dir = os.path.dirname(os.path.abspath(__file__))
        shield_path = os.path.join(current_dir, "asset", "shield", "1.png")
        self.image = QPixmap(shield_path)
        
        # Shield should be 20% larger than player
        self.width = int(player.width * 1.5)
        self.height = int(player.height * 1.5)

        self.hitbox_offset_x = (self.width - self.player.width) // 2
        self.hitbox_offset_y = (self.height - self.player.height) // 2

        # ⚡ Bolt: Pre-scale image and apply opacity to optimize rendering loop
        if not self.image.isNull():
            scaled = self.image.scaled(self.width, self.height,
                Qt.KeepAspectRatio, Qt.FastTransformation)

            # Pre-render the opacity into the image to avoid expensive painter.setOpacity calls in draw loop
            self.scaled_image = QPixmap(scaled.size())
            self.scaled_image.fill(Qt.transparent)
            painter = QPainter(self.scaled_image)
            painter.setOpacity(0.7)
            painter.drawPixmap(0, 0, scaled)
            painter.end()
        else:
            self.scaled_image = QPixmap()
            
    def get_rect(self):
        # Center the shield hitbox around the player
        return (
            int(self.player.x) - self.hitbox_offset_x,
            int(self.player.y) - self.hitbox_offset_y,
            self.width,
            self.height
        )
        
    def draw(self, painter):
        if not self.scaled_image.isNull():
            # Only draw if health system says we're visible (for blinking effect)
            if not hasattr(self.player.game_widget, 'health_system') or \
               self.player.game_widget.health_system.is_visible:
                # Center shield around player
                painter.drawPixmap(
                    int(self.player.x) - self.hitbox_offset_x,
                    int(self.player.y) - self.hitbox_offset_y,
                    self.scaled_image
                )