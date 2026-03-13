## 2025-02-23 - QPixmap.scaled() bottleneck in PyQt render loops
**Learning:** Calling `QPixmap.scaled()` or scaling large images dynamically per frame inside a `paintEvent` or `draw` method is a severe performance bottleneck in PyQt rendering loops.
**Action:** Always pre-scale static images and base assets for dynamic entities in their `__init__` methods and store the pre-scaled versions (`self.scaled_frames`, `self.scaled_image`, etc.). This dramatically reduces the cost of rendering animated or dynamically resizing elements.
