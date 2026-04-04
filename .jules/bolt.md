## 2024-05-24 - [Avoid Per-Frame Image Scaling]
**Learning:** In PyQt game loops, calling `QPixmap.scaled` inside `draw()` or `paintEvent()` for active entities (like `Shield` or `ExplosionAnimation`) is extremely expensive and tanks framerate.
**Action:** Always pre-scale images during object initialization (`__init__`) and store them in attributes (e.g., `self.scaled_frames`, `self.scaled_image`) to be directly drawn each frame without re-computing the scaling.
