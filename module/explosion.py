from module.animation import Animation
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt

class ExplosionAnimation(Animation):
    def __init__(self, x, y, size):
        super().__init__("explosion", 8, 100)  # Changed from 50ms to 100ms delay
        self.x = x
        self.y = y
        self.size = size
        self.is_finished = False
        self.current_frame = 0
        
        # Optimization: Pre-scale animation frames during initialization
        # instead of scaling them every frame in draw()
        self.scaled_frames = []
        scaled_size = int(self.size * 2.5)
        for frame in self.frames:
            if frame and not frame.isNull():
                scaled_frame = frame.scaled(scaled_size, scaled_size, Qt.KeepAspectRatio, Qt.FastTransformation)
                self.scaled_frames.append(scaled_frame)
            else:
                self.scaled_frames.append(frame)

    def update(self, delta_time):
        if self.is_finished:
            return
            
        self.time_accumulated += delta_time
        if self.time_accumulated >= self.frame_delay:
            self.time_accumulated = 0
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                self.is_finished = True
                return
                
    def draw(self, painter):
        if self.is_finished or not self.scaled_frames:
            return
            
        current_frame = self.scaled_frames[self.current_frame]
        if current_frame:
            # Center the explosion on the block's position
            x = self.x + (self.size - current_frame.width()) // 2
            y = self.y + (self.size - current_frame.height()) // 2
            
            painter.drawPixmap(int(x), int(y), current_frame)