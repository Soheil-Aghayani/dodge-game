from module.animation import Animation
from PyQt5.QtGui import QPixmap, QPainter, QColor

class JumpPlayer(Animation):
    def __init__(self):
        super().__init__("jump", 9, 50)  # 9 frames, 50ms delay for smooth jump animation
        self.jump_height = 150  # Maximum jump height
        self.jump_speed = 0
        self.gravity = 0.5
        self.is_jumping = False
        self.initial_y = 0
        self.current_y_offset = 0
        
    def start_jump(self, initial_y):
        if not self.is_jumping:
            self.is_jumping = True
            self.initial_y = initial_y
            self.jump_speed = -12  # Initial upward velocity
            self.current_y_offset = 0
            self.current_frame = 0  # Reset animation
            
    def update(self, delta_time):
        if self.is_jumping:
            # Update jump physics
            self.jump_speed += self.gravity
            self.current_y_offset += self.jump_speed
            
            # Check if jump is complete (back to ground)
            if self.current_y_offset >= 0:
                self.current_y_offset = 0
                self.is_jumping = False
                self.jump_speed = 0
                return True  # Jump complete
                
            # Update animation frame
            self.time_accumulated += delta_time
            if self.time_accumulated >= self.frame_delay:
                self.time_accumulated = 0
                if self.current_frame < len(self.frames) - 1:  # Don't loop jump animation
                    self.current_frame += 1
                    
        return False  # Jump not complete
        
    def get_y_offset(self):
        return self.current_y_offset 