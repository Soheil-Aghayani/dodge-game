from module.animation import Animation
from PyQt5.QtGui import QPixmap, QPainter, QColor

class DiePlayer(Animation):
    def __init__(self):
        super().__init__("die", 8, 200)  # 8 frames, 100ms delay
        self.is_finished = False
        self.played_once = False
        self.current_frame = 0
        self.opacity = 1.0  # Start fully opaque
        self.fall_speed = 0  # Initial fall speed
        self.fall_acceleration = 0.5  # Gravity effect
        self.y_offset = 0  # Track vertical position during fall
        
    def update(self, delta_time):
        if self.is_finished:
            return
            
        self.time_accumulated += delta_time
        if self.time_accumulated >= self.frame_delay:
            self.time_accumulated = 0
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                if not self.played_once:
                    self.played_once = True
                    self.current_frame = len(self.frames) - 1  # Stay on last frame
                    self.is_finished = True
                    
    def get_current_frame(self, flipped=False):
        frames_list = self.flipped_frames if flipped and self.flipped_frames else self.frames
        frame = frames_list[min(len(frames_list) - 1, self.current_frame)]
        if frame and self.opacity < 1.0:
            # Create a copy of the frame for opacity modification
            temp = QPixmap(frame.size())
            temp.fill(QColor(0, 0, 0, 0))  # Transparent background
            painter = QPainter(temp)
            painter.setOpacity(self.opacity)
            painter.drawPixmap(0, 0, frame)
            painter.end()
            return temp
        return frame
        
    def get_fall_offset(self):
        return self.y_offset