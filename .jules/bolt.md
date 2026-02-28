## 2025-02-21 - Image Scaling Overhead in PyQt Render Loop
**Learning:** In PyQt (and similar frameworks), constantly calling `QPixmap.scaled` inside high-frequency functions like `draw()` or `paintEvent()` is a severe performance bottleneck. It creates a new pixmap and performs the scaling math every frame. In this codebase, the benchmark showed an almost ~480x speedup when moving scaling out of the render loop.
**Action:** Always pre-scale and cache images during initialization (`__init__`) or when their size explicitly changes. Use the cached images in the render loop.
