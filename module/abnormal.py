import random

class AbnormalManager:
    ABNORMAL_TYPES = [
        'reverse_floor',    # موانع از پایین به بالا و بازیکن برعکس
        'reverse_control',  # کنترل چپ و راست برعکس
        'random_blocks'     # حرکت رندوم موانع
    ]

    def __init__(self):
        self.current_window = 0
        self.abnormal_trigger_score = None
        self.abnormal_type = None
        self.active = False
        self.manual_mode = False  # For test/manual activation
        self.last_abnormal_type = None  # Track last used abnormal type

    def update(self, score):
        if self.manual_mode:
            return  # Do not auto-update in manual mode
            
        # Calculate current window (every 100 points)
        window = score // 100
        
        # If we've entered a new window, set up the next abnormality
        if window != self.current_window:
            self.current_window = window
            # Deactivate current abnormality
            self.active = False
            # Set trigger score to be between 20-80 points into the new window
            self.abnormal_trigger_score = (window * 100) + random.randint(20, 80)
            # Choose a new abnormal type that's different from the last one
            available_types = [t for t in self.ABNORMAL_TYPES if t != self.last_abnormal_type]
            if available_types:
                self.abnormal_type = random.choice(available_types)
            else:
                self.abnormal_type = random.choice(self.ABNORMAL_TYPES)
            self.last_abnormal_type = self.abnormal_type
            
        # Activate abnormality when score reaches trigger point
        if self.abnormal_trigger_score is not None and score >= self.abnormal_trigger_score:
            self.active = True
        else:
            self.active = False

    def is_active(self):
        return self.active

    def get_type(self):
        return self.abnormal_type if self.active else None

    # --- Manual/test methods ---
    def activate_manual(self, abnormal_type):
        if abnormal_type in self.ABNORMAL_TYPES:
            self.abnormal_type = abnormal_type
            self.active = True
            self.manual_mode = True
            self.last_abnormal_type = abnormal_type

    def deactivate_manual(self):
        self.active = False
        self.manual_mode = False
        self.abnormal_type = None 