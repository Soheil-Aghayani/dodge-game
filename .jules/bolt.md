## 2023-10-27 - [Pre-scale Images in Render Loops]
**Learning:** PyQt game loops suffer massive performance degradation if QPixmap.scaled() is called dynamically on every frame inside a draw() or paintEvent() method.
**Action:** Always pre-scale QPixmaps and cache them (e.g., as `self.scaled_image` or `self.scaled_frames`) in the `__init__` or `resizeEvent` phase before rendering to avoid runtime bottlenecks.
## 2024-04-19 - Pre-scale dynamic block images
**Learning:** Downscaling high-res images directly within the `paintEvent` or `draw` loop to process transformations causes massive CPU rendering bottlenecks, even when aspect-ratio constraints are used. This logic applied to the `barrel` item in `module/block.py` was being parsed on each frame instead of caching the scaled state.
**Action:** Always pre-scale assets when initializing object pools. Avoid putting base scaling routines into rendering functions. Pre-scaled base components still scale up gracefully via PyQt Transform attributes, enabling more effective use of computational resources.
## 2024-05-29 - [Pre-scale Images in Render Loops for PauseScreen]
**Learning:** PyQt game loops and UI overlays suffer massive performance degradation if QPixmap.scaled() is called dynamically on every paintEvent() method. For `PauseScreen`, this was reducing paintEvent performance from ~0.008s down to ~0.265s for 100 loops.
**Action:** Always pre-scale QPixmaps and cache them (e.g., as `self._scaled_background`) in the `__init__` or `resizeEvent` phase before rendering to avoid runtime bottlenecks.
## 2024-06-25 - [Pre-scale Sprite Flips in Render Loops]
**Learning:** In PyQt game loops, dynamically flipping sprites using `painter.scale(-1, 1)` and `painter.translate` during `paintEvent` or `draw` methods is significantly slower (~6.8x slower in benchmarks) than drawing pre-cached transformed pixmaps.
**Action:** When initializing animation frames, use `QPixmap.transformed(QTransform().scale(-1, 1))` to pre-cache horizontally flipped versions of the frames alongside the normal ones. Then, select the correct pre-cached frame based on the facing direction to avoid expensive transform state changes in the render loop.
