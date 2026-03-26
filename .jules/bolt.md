## 2024-05-23 - Prevent image scaling in PyQt5 loops
**Learning:** In PyQt game loops, constantly re-scaling images (e.g., `QPixmap.scaled`) inside `draw()` or `paintEvent()` is a severe bottleneck.
**Action:** Pre-scale and cache images during initialization or when their size explicitly changes.
