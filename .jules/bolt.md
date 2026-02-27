## 2024-05-18 - Caching PyQt Scaled Images
**Learning:** In a PyQt game loop (e.g., in `module/explosion.py` and `module/shield.py`), constantly re-scaling images inside the `paintEvent` or `draw` methods (e.g., using `QPixmap.scaled`) can be a significant performance bottleneck.
**Action:** Always pre-scale and cache images during initialization or when their size changes, instead of inside the `draw` method.
