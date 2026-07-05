import random
import os
import math
import time
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPixmap, QPainter, QColor, QTransform
from module.explosion import ExplosionAnimation

class Block:
    _cached_rotated_barrels = {}
    obstacle_images = {}
    scaled_obstacle_images = {}
    fallback_color = None
    
    # Pre-cached random choice allocations
    _image_weights = {
        "barrel": 0.5,
        "metalbox": 0.3,
        "woodenbox": 0.2
    }
    _image_keys = list(_image_weights.keys())
    _image_values = list(_image_weights.values())

    # ⚡ Bolt Optimization: Pre-cache random speeds to avoid allocating a new list per choice
    _random_speeds = [-3, -2, 2, 3]

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
        self.horizontal_speed = random.choice(Block._random_speeds)  # Random initial direction and speed
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

            # Pre-cache all 180 rotated states of the barrel to avoid expensive
            # dynamic rotation during the render loop (Block.draw)
            barrel_scaled = Block.obstacle_images["barrel"]
            Block._cached_rotated_barrels = {}
            for angle in range(0, 360, 2):
                transform = QTransform().rotate(angle)
                transformed_img = barrel_scaled.transformed(transform, Qt.SmoothTransformation)
                Block._cached_rotated_barrels[angle] = (transformed_img, transformed_img.width(), transformed_img.height())

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
        # ⚡ Bolt Optimization: Use pre-cached keys and values to avoid redundant allocations on every spawn
        self.image_type = random.choices(Block._image_keys, Block._image_values)[0]
        self.image = Block.obstacle_images.get(self.image_type)
        self.img_w = self.image.width() if self.image else 0
        self.img_h = self.image.height() if self.image else 0
        
        # Pre-calculate common properties to avoid float math/division in hot paths
        self.explosion_offset_x = 0
        self.explosion_offset_y = 0
        self.static_offset_x = 0
        self.static_offset_y = 0

        # Set animation properties based on image type
        if self.image_type == "barrel":
            self.should_rotate = True
            self.should_pulse = True
            self.width = 50  # Barrels are slightly bigger
            self.height = 50
            self.explosion_size = int(self.width * 2.5)

            # ⚡ Bolt Optimization: Pre-calculate explosion hitbox offsets
            self.explosion_offset_x = (self.width // 2) - (self.explosion_size // 2)
            self.explosion_offset_y = (self.height // 2) - (self.explosion_size // 2)

            self.explosion_extra = int(self.width * 0.75) # Not directly used for offset if using center_x but kept
            self.hitbox_reduction = int(self.width * 0.2)
            self.reduced_width = self.width - (self.hitbox_reduction * 2)
            self.reduced_height = self.height - (self.hitbox_reduction * 2)
        elif self.image_type in Block.scaled_obstacle_images:
            # ⚡ Bolt Optimization: Pre-calculate static image rendering offsets
            _, scaled_w, scaled_h = Block.scaled_obstacle_images[self.image_type]
            self.static_offset_x = (self.width - scaled_w) // 2
            self.static_offset_y = (self.height - scaled_h) // 2

        # ⚡ Bolt Optimization: Pre-calculate center offset for dynamic barrel rotation
        self.center_offset_x = self.width / 2
        self.center_offset_y = self.height / 2
            
    def update(self, is_random_blocks=None, game_width=None, floor_y=None, current_time=None):
        if self.explosion and not self.explosion.is_finished:
            if current_time is None:
                current_time = int(time.time() * 1000)
            self.explosion.update(current_time)
            return False
            
        if self.explosion and self.explosion.is_finished:
            self.explosion = None
            self.is_exploding = False
            return True
            
        if self.is_exploding:
            return False
            
        self.y += self.fall_speed
        
        # Determine fallback values if None are provided
        if is_random_blocks is None:
            is_random_blocks = self.game_widget.abnormal_manager.is_active() and self.game_widget.abnormal_manager.get_type() == 'random_blocks'
        if game_width is None:
            game_width = self.game_widget.width()
        if floor_y is None:
            floor_y = self.game_widget.floor.get_y_position()

        # Handle random movement if random_blocks is active
        if is_random_blocks:
            # Update horizontal position
            self.x += self.horizontal_speed
            
            # Bounce off walls
            if self.x <= 0:
                self.x = 0
                self.horizontal_speed = abs(self.horizontal_speed)  # Move right
            elif self.x >= game_width - self.width:
                self.x = game_width - self.width
                self.horizontal_speed = -abs(self.horizontal_speed)  # Move left
            
            # Randomly change direction
            self.direction_change_timer -= 1
            if self.direction_change_timer <= 0:
                self.horizontal_speed = random.choice(Block._random_speeds)
                self.direction_change_timer = random.randint(20, 60)
        
        if self.should_rotate:
            self.angle = (self.angle + 2) % 360
            
        if self.should_pulse:
            self.pulse_time += 0.1
            
        # Check if block has hit the floor
        if self.y + self.height >= floor_y:
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
                # ⚡ Bolt Optimization: Use pre-calculated offset for explosion hitbox to avoid float math
                return (
                    int(self.x) + self.explosion_offset_x,
                    int(self.y) + self.explosion_offset_y,
                    self.explosion_size,
                    self.explosion_size
                )
            else:
                # Smaller hitbox for normal barrel (80% of size)
                return (
                    int(self.x) + self.hitbox_reduction,
                    int(self.y) + self.hitbox_reduction,
                    self.reduced_width,
                    self.reduced_height
                )
        else:
            # Normal hitbox for other blocks
            return (
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
            # ⚡ Bolt Optimization: Use pre-calculated offset for static blocks to avoid float math/division
            scaled_img, _, _ = Block.scaled_obstacle_images[self.image_type]
            painter.drawPixmap(int(self.x + self.static_offset_x), int(self.y + self.static_offset_y), scaled_img)
            return

        if self.image:
            img_w = self.img_w
            img_h = self.img_h
            block_w = self.width
            block_h = self.height
            scale_pulse = 1.0
            if self.should_pulse:
                scale_pulse = 0.85 + 0.15 * (1 + math.sin(self.pulse_time + self.pulse_phase))
            if self.should_rotate and self.angle in Block._cached_rotated_barrels:
                # ⚡ Bolt: Use pre-cached rotated image to bypass expensive C++ boundary calls
                # (painter.save/restore, translate, rotate) in the hot render loop.
                cached_img, cached_w, cached_h = Block._cached_rotated_barrels[self.angle]
                # Scale the already-rotated cached image based on the pulse scale
                rot_w = int(cached_w * scale_pulse)
                rot_h = int(cached_h * scale_pulse)

                # Center point of the block
                # ⚡ Bolt Optimization: Use pre-calculated center offset to avoid float math
                center_x = self.x + self.center_offset_x
                center_y = self.y + self.center_offset_y

                # Draw from top-left offset to center
                draw_x = int(center_x - rot_w / 2)
                draw_y = int(center_y - rot_h / 2)

                painter.drawPixmap(draw_x, draw_y, rot_w, rot_h, cached_img)
            else:
                scale = min(block_w / img_w, block_h / img_h) * scale_pulse
                new_w = int(img_w * scale)
                new_h = int(img_h * scale)
                x = self.x + (block_w - new_w) // 2
                y = self.y + (block_h - new_h) // 2
                painter.drawPixmap(int(x), int(y), int(new_w), int(new_h), self.image)
        else:
            if Block.fallback_color is None:
                Block.fallback_color = QColor(255, 0, 0)
            painter.setBrush(Block.fallback_color)
            painter.drawRect(QRect(*self.get_rect()))
            
    def check_collision(self, player_bounds):
        # player_bounds is a tuple (px, py, pw, ph, pr, pb)
        # where pr is player right (px + pw) and pb is player bottom (py + ph)
        px, py, pw, ph, pr, pb = player_bounds

        # ⚡ Bolt Optimization: Fast 2D broad-phase check.
        # If the block (even accounting for max explosion size ~150px) is completely
        # above, below, to the left, or to the right of the player, return early
        # without computing the exact rect or doing the more complex intersection math.
        if self.y + 150 < py or self.y - 150 > pb or self.x + 150 < px or self.x - 150 > pr:
            return False

        rect = self.get_rect()
        if not rect:
            return False

        bx, by, bw, bh = rect
        # Check normal collision if not exploding, or if explosion animation is playing
        if (self.explosion and not self.explosion.is_finished) or not self.is_exploding:
            return not (px >= bx + bw or pr <= bx or py >= by + bh or pb <= by)
        return False