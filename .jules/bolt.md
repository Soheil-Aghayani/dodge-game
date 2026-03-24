## 2024-03-24 - [Avoid dynamic scaling inside PyQt paintEvent]
**Learning:** In PyQt game loops, constantly re-scaling images (e.g., `QPixmap.scaled`) inside `draw()` or `paintEvent()` is a severe CPU bottleneck.
**Action:** Always pre-scale and cache images during initialization or when their size explicitly changes. For animated elements, create a separate array for `self.scaled_frames` rather than resizing inside the render loop.
