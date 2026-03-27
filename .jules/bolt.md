## 2024-03-27 - [Pre-scale and cache dynamic images]
**Learning:** In PyQt game loops, constantly re-scaling images (e.g., `QPixmap.scaled`) inside `draw()` or `paintEvent()` is a severe bottleneck. Images for entities like explosions or shields must be pre-scaled and cached during initialization or when their size explicitly changes.
**Action:** Always pre-scale and cache QPixmaps in `__init__` rather than recalculating them in the render loop.
