from module.animation import Animation
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt

class ExplosionAnimation(Animation):
    # Cache pre-scaled frames based on size to avoid expensive scaling every frame
    _scaled_frames_cache = {}

    def __init__(self, x, y, size):
        super().__init__("explosion", 8, 100)  # Changed from 50ms to 100ms delay
        self.x = x
        self.y = y
        self.size = size
        self.is_finished = False
        self.current_frame = 0
        
        # Pre-scale frames to 2.5x larger than the block and cache them
        self.scaled_size = int(self.size * 2.5)
        cache_key = self.scaled_size

        if cache_key not in ExplosionAnimation._scaled_frames_cache:
            scaled_frames = []
            for frame in self.frames:
                scaled_frame = frame.scaled(
                    self.scaled_size,
                    self.scaled_size,
                    Qt.KeepAspectRatio,
                    Qt.FastTransformation
                )
                scaled_frames.append(scaled_frame)
            ExplosionAnimation._scaled_frames_cache[cache_key] = scaled_frames

        self.scaled_frames = ExplosionAnimation._scaled_frames_cache[cache_key]

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
            
        scaled_frame = self.scaled_frames[self.current_frame]
        if scaled_frame:
            # Center the explosion on the block's position
            x = self.x + (self.size - scaled_frame.width()) // 2
            y = self.y + (self.size - scaled_frame.height()) // 2
            
            painter.drawPixmap(int(x), int(y), scaled_frame) 