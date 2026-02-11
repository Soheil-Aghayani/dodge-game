from module.animation import Animation

class IdlePlayer(Animation):
    def __init__(self):
        super().__init__("idle", 2, 500)  # 2 frames, 500ms delay 