## 2024-11-20 - [Pre-scale Shield Image and Block Images]
**Learning:** Calling `QPixmap.scaled` inside `draw()` every frame creates a massive performance bottleneck. The same issue exists when calling `QPixmap.width()` and `QPixmap.height()` directly from Python to C++ repeatedly.
**Action:** When working with rendering objects in PyQt, pre-scale images inside the `__init__` constructor and cache their size as instance attributes like `self.img_w` or `self.scaled_image` so it bypasses expensive re-calculations on every frame.
