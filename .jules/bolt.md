## 2024-05-24 - Pre-scale QPixmap in Initialization

**Learning:** Constantly resizing `QPixmap` objects inside a PyQT game loop `draw()` or `paintEvent()` method is a severe performance bottleneck. Images for entities like explosions or shields must be pre-scaled and cached during initialization.
**Action:** Always pre-scale images or animation frames in `__init__()` and cache them in instance attributes (e.g., `self.scaled_frames`) instead of resizing on the fly in `draw()`.
