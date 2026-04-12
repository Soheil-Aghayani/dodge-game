## 2023-10-27 - [Pre-scale Images in Render Loops]
**Learning:** PyQt game loops suffer massive performance degradation if QPixmap.scaled() is called dynamically on every frame inside a draw() or paintEvent() method.
**Action:** Always pre-scale QPixmaps and cache them (e.g., as `self.scaled_image` or `self.scaled_frames`) in the `__init__` or `resizeEvent` phase before rendering to avoid runtime bottlenecks.

## 2026-04-12 - [Pre-scale Large Dynamic Assets to Base Size]
**Learning:** Large source assets for dynamically scaled and rotated entities (like 'barrel') cause significant CPU overhead if scaled from their original high resolution on every frame inside `draw`.
**Action:** Pre-scale the source `QPixmap` to its base logical size (e.g., 50x50) during initialization, even if it will undergo further dynamic scaling/rotation later. This drastically reduces the pixel processing overhead for `QPainter`.
