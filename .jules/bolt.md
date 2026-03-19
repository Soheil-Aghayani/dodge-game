## 2024-05-14 - Pre-scaling Images in Initialization
**Learning:** In PyQt game loops, constantly re-scaling images (e.g., `QPixmap.scaled`) inside `draw()` or `paintEvent()` is a severe bottleneck.
**Action:** Images for entities like explosions or shields must be pre-scaled and cached during initialization or when their size explicitly changes. Store the scaled images in a new instance attribute (e.g., `self.scaled_frames`) instead of mutating inherited or shared lists (like `self.frames`) in place to prevent global state corruption across instances.
