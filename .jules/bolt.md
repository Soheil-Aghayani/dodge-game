## 2024-05-24 - Pre-scaling images in PyQt
**Learning:** Constantly re-scaling images using `QPixmap.scaled` inside `draw()` or `paintEvent()` is a severe performance bottleneck in PyQt rendering loops.
**Action:** Always pre-scale and cache images during initialization or when their size explicitly changes. For animated frames, store the scaled images in a separate instance attribute (e.g., `self.scaled_frames`) to avoid mutating shared state.
