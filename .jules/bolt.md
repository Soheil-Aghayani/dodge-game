## 2024-05-24 - Pre-scaling Shield and Explosion Images
**Learning:** In PyQt game loops, constantly re-scaling images (e.g., `QPixmap.scaled`) inside `draw()` or `paintEvent()` is a severe bottleneck. Images for entities like explosions or shields must be pre-scaled and cached during initialization or when their size explicitly changes.
**Action:** When working on PyQt components, pre-calculate dimensions during `__init__` and store the `QPixmap.scaled` images in properties such as `self.scaled_image` or `self.scaled_frames` instead of calling `QPixmap.scaled` in `draw()` methods.
