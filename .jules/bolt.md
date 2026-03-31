## 2024-05-20 - PyQt Image Scaling Bottleneck
**Learning:** Constantly re-scaling images (e.g., `QPixmap.scaled`) inside `draw()` or `paintEvent()` in PyQt game loops is a severe bottleneck. This pattern is prevalent in this codebase's rendering architecture.
**Action:** When working with dynamic objects like `ExplosionAnimation` or `Shield`, always pre-scale and cache their images during `__init__` or whenever their size explicitly changes, rather than calculating it on every frame in the render loop.
