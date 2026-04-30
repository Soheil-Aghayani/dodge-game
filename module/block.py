import random
import os
import math
from PyQt5.QtCore import QRect, QTime, Qt
from PyQt5.QtGui import QPixmap, QPainter
from module.explosion import ExplosionAnimation

class Block:
    obstacle_images = {}
    scaled_obstacle_images = {}
    
    def __init__(self, game_widget):
        self.game_widget = game_widget
        self.width = 40
        self.height = 40
        self.x = random.randint(0, game_widget.width() - self.width)
        self.y = -self.height
        self.fall_speed = 5
        self.angle = 0
        self.should_rotate = False
        self.should_pulse = False
        self.pulse_time = 0
        self.pulse_phase = random.uniform(0, 2 * math.pi)
        self.explosion = None
        self.is_exploding = False
        self.image_type = None
        
        # Random movement properties
        self.horizontal_speed = random.choice([-3, -2, 2, 3])  # Random initial direction and speed
        self.direction_change_timer = random.randint(20, 60)  # Random timer for direction changes
        
        # Load images if not already loaded
        if not Block.obstacle_images:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, "asset", "obstacle")
            Block.obstacle_images = {
                "barrel": QPixmap(os.path.join(image_path, "barrel.png")),
                "metalbox": QPixmap(os.path.join(image_path, "metalbox.png")),
                "woodenbox": QPixmap(os.path.join(image_path, "woodenbox.png"))
            }

            # Pre-scale barrel directly within obstacle_images to its base dimensions (50x50)
            # to avoid severe performance bottlenecks during the render loop when it pulses and rotates
            barrel_img = Block.obstacle_images["barrel"]
            scale = min(50 / barrel_img.width(), 50 / barrel_img.height())
            Block.obstacle_images["barrel"] = barrel_img.scaled(
                int(barrel_img.width() * scale), int(barrel_img.height() * scale), Qt.IgnoreAspectRatio, Qt.SmoothTransformation
            )

            # Pre-scale static images for performance optimization
            # This avoids resizing the image every frame in draw()
            Block.scaled_obstacle_images = {}
            for type_name in ["metalbox", "woodenbox"]:
                if type_name in Block.obstacle_images:
                    img = Block.obstacle_images[type_name]
                    # Use current block dimensions for scaling
                    target_w, target_h = self.width, self.height
                    scale = min(target_w / img.width(), target_h / img.height())
                    new_w = int(img.width() * scale)
                    new_h = int(img.height() * scale)
                    scaled_img = img.scaled(
                        new_w, new_h, Qt.IgnoreAspectRatio, Qt.SmoothTransformation
                    )
                    Block.scaled_obstacle_images[type_name] = (scaled_img, new_w, new_h)
        
        # Randomly select an image with weights
        weights = {
            "barrel": 0.5,
            "metalbox": 0.3,
            "woodenbox": 0.2
        }
        self.image_type = random.choices(list(weights.keys()), list(weights.values()))[0]
        self.image = Block.obstacle_images.get(self.image_type)
        self.img_w = self.image.width() if self.image else 0
        self.img_h = self.image.height() if self.image else 0
        
        # Set animation properties based on image type
        if self.image_type == "barrel":
            self.should_rotate = True
            self.should_pulse = True
            self.width = 50  # Barrels are slightly bigger
            self.height = 50
            
    def update(self):
        if self.explosion and not self.explosion.is_finished:
            current_time = QTime.currentTime().msecsSinceStartOfDay()
            self.explosion.update(current_time)
            return False
            
        if self.explosion and self.explosion.is_finished:
            self.explosion = None
            self.is_exploding = False
            return True
            
        if self.is_exploding:
            return False
            
        self.y += self.fall_speed
        
        # Handle random movement if random_blocks is active
        if self.game_widget.abnormal_manager.is_active() and self.game_widget.abnormal_manager.get_type() == 'random_blocks':
            # Update horizontal position
            self.x += self.horizontal_speed
            
            # Bounce off walls
            if self.x <= 0:
                self.x = 0
                self.horizontal_speed = abs(self.horizontal_speed)  # Move right
            elif self.x >= self.game_widget.width() - self.width:
                self.x = self.game_widget.width() - self.width
                self.horizontal_speed = -abs(self.horizontal_speed)  # Move left
            
            # Randomly change direction
            self.direction_change_timer -= 1
            if self.direction_change_timer <= 0:
                self.horizontal_speed = random.choice([-3, -2, 2, 3])
                self.direction_change_timer = random.randint(20, 60)
        
        if self.should_rotate:
            self.angle = (self.angle + 2) % 360
            
        if self.should_pulse:
            self.pulse_time += 0.1
            
        # Check if block has hit the floor
        if self.y + self.height >= self.game_widget.floor.get_y_position():
            if self.should_pulse:  # If it's a barrel, explode
                self.start_explosion()
                return False
            return True  # Other blocks just disappear
            
        return False
        
    def start_explosion(self):
        self.is_exploding = True
        self.explosion = ExplosionAnimation(self.x, self.y, self.width)
        
    def get_rect(self):
        if self.image_type == "barrel":
            if self.is_exploding or (self.explosion and not self.explosion.is_finished):
                # Make hitbox match the explosion animation size (2.5x)
                extra = int(self.width * 0.75)  # This makes total size 2.5x original size
                center_x = self.x + (self.width // 2)
                center_y = self.y + (self.height // 2)
                explosion_size = int(self.width * 2.5)
                return QRect(
                    int(center_x - explosion_size // 2),
                    int(center_y - explosion_size // 2),
                    explosion_size,
                    explosion_size
                )
            else:
                # Smaller hitbox for normal barrel (80% of size)
                reduction = int(self.width * 0.2)
                return QRect(
                    int(self.x + reduction),
                    int(self.y + reduction),
                    self.width - (reduction * 2),
                    self.height - (reduction * 2)
                )
        else:
            # Normal hitbox for other blocks
            return QRect(
                int(self.x),
                int(self.y),
                self.width,
                self.height
            )
            
    def draw(self, painter):
        if self.explosion and not self.explosion.is_finished:
            self.explosion.draw(painter)
            return
            
        if self.is_exploding:
            return
            
        # Optimization: Use pre-scaled image for static blocks to avoid expensive resizing every frame
        if self.image_type in Block.scaled_obstacle_images:
            scaled_img, scaled_w, scaled_h = Block.scaled_obstacle_images[self.image_type]
            x = self.x + (self.width - scaled_w) // 2
            y = self.y + (self.height - scaled_h) // 2
            painter.drawPixmap(int(x), int(y), scaled_img)
            return

        if self.image:
            img_w = self.img_w
            img_h = self.img_h
            block_w = self.width
            block_h = self.height
            scale_pulse = 1.0
            if self.should_pulse:
                scale_pulse = 0.85 + 0.15 * (1 + math.sin(self.pulse_time + self.pulse_phase))
            scale = min(block_w / img_w, block_h / img_h) * scale_pulse
            new_w = int(img_w * scale)
            new_h = int(img_h * scale)
            x = self.x + (block_w - new_w) // 2
            y = self.y + (block_h - new_h) // 2
            if self.should_rotate:
                painter.save()
                # Use SmoothPixmapTransform for better quality rotation
                painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

                # Move coordinate system to center of the block
                center_x = x + new_w / 2
                center_y = y + new_h / 2
                painter.translate(center_x, center_y)

                # Rotate
                painter.rotate(self.angle)

                # Move back to top-left relative to center
                painter.translate(-new_w / 2, -new_h / 2)

                # Draw the image
                painter.drawPixmap(0, 0, int(new_w), int(new_h), self.image)
                painter.restore()
            else:
                painter.drawPixmap(int(x), int(y), int(new_w), int(new_h), self.image)
        else:
            from PyQt5.QtGui import QColor
            painter.setBrush(QColor(255, 0, 0))
            painter.drawRect(self.get_rect())
            
    def check_collision(self, player_rect):
        # Only check collision if explosion animation is playing
        if self.explosion and not self.explosion.is_finished:
            return self.get_rect().intersects(player_rect)
        # Check normal collision if not exploding
        if not self.is_exploding:
            return self.get_rect().intersects(player_rect)
        return False 