## 2023-10-27 - [Pre-scale Images in Render Loops]
**Learning:** PyQt game loops suffer massive performance degradation if QPixmap.scaled() is called dynamically on every frame inside a draw() or paintEvent() method.
**Action:** Always pre-scale QPixmaps and cache them (e.g., as `self.scaled_image` or `self.scaled_frames`) in the `__init__` or `resizeEvent` phase before rendering to avoid runtime bottlenecks.
## 2024-04-19 - Pre-scale dynamic block images
**Learning:** Downscaling high-res images directly within the `paintEvent` or `draw` loop to process transformations causes massive CPU rendering bottlenecks, even when aspect-ratio constraints are used. This logic applied to the `barrel` item in `module/block.py` was being parsed on each frame instead of caching the scaled state.
**Action:** Always pre-scale assets when initializing object pools. Avoid putting base scaling routines into rendering functions. Pre-scaled base components still scale up gracefully via PyQt Transform attributes, enabling more effective use of computational resources.
## 2024-05-29 - [Pre-scale Images in Render Loops for PauseScreen]
**Learning:** PyQt game loops and UI overlays suffer massive performance degradation if QPixmap.scaled() is called dynamically on every paintEvent() method. For `PauseScreen`, this was reducing paintEvent performance from ~0.008s down to ~0.265s for 100 loops.
**Action:** Always pre-scale QPixmaps and cache them (e.g., as `self._scaled_background`) in the `__init__` or `resizeEvent` phase before rendering to avoid runtime bottlenecks.
