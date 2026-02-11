from module.animation import Animation

class MovingPlayer(Animation):
    def __init__(self):
        super().__init__("moving", 4, 100)  # 4 frames, 100ms delay for faster animation 