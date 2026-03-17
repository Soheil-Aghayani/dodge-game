## 2024-05-15 - [Optimize Shield and Explosion Render Loop by Pre-scaling]
**Learning:** Calling `.scaled()` inside `draw()` on dynamic items (like shields or explosive animations) happens every frame, which drains FPS.
**Action:** When working on rendering in Qt components (e.g. PyQt5 `QPainter`), always pre-scale `QPixmap` instances in `__init__` and store them on `self` for rapid rendering during `paintEvent` or `draw` methods.
