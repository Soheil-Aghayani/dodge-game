from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os
import math

class Animation:
    def __init__(self, folder_name, frame_count, frame_delay=100):
        self.frames = []
        self.current_frame = 0
        self.frame_count = frame_count
        self.frame_delay = frame_delay
        self.time_accumulated = 0
        self.idle_offset = 0  # For idle animation vertical movement
        
        # Load frames
        current_dir = os.path.dirname(os.path.abspath(__file__))
        for i in range(1, frame_count + 1):
            path = os.path.join(current_dir, "asset", folder_name, f"{i}.png")
            frame = QPixmap(path)
            if frame.isNull():
                print(f"Error loading frame {i} from {path}")
            else:
                # Scale frame to exact dimensions (48x81) using nearest neighbor for pixel art
                frame = frame.scaled(48, 81, Qt.IgnoreAspectRatio, Qt.FastTransformation)
                self.frames.append(frame)
                
    def update(self, delta_time):
        self.time_accumulated += delta_time
        if self.time_accumulated >= self.frame_delay:
            self.time_accumulated = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            
    def get_current_frame(self):
        if self.frames:
            return self.frames[self.current_frame]
        return None
        
    def get_idle_offset(self):
        # Return a small vertical offset for idle animation (1-2 pixels up/down)
        return math.sin(self.time_accumulated / 200) * 1.5 