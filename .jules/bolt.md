## 2024-03-18 - [Optimize Dynamic Rendered Objects]
**Learning:** In PyQt game loops, constantly re-scaling images (e.g., `QPixmap.scaled`) inside `draw()` or `paintEvent()` is a severe bottleneck.
**Action:** Images for entities like explosions or shields must be pre-scaled and cached during initialization (`__init__`) or when their size explicitly changes.
