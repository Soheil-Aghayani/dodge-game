## 2023-10-27 - [Pre-scale Images in Render Loops]
**Learning:** PyQt game loops suffer massive performance degradation if QPixmap.scaled() is called dynamically on every frame inside a draw() or paintEvent() method.
**Action:** Always pre-scale QPixmaps and cache them (e.g., as `self.scaled_image` or `self.scaled_frames`) in the `__init__` or `resizeEvent` phase before rendering to avoid runtime bottlenecks.

## 2023-10-27 - [Pre-flip Sprite Frames]
**Learning:** In PyQt game loops, dynamically flipping sprites using `painter.scale(-1, 1)` and `painter.translate` during every `paintEvent` is surprisingly slow compared to drawing pre-cached transformed pixmaps (~6.8x slower in microbenchmarks).
**Action:** When working with sprites that face multiple directions, always pre-cache flipped versions of the frames (using `QPixmap.transformed`) during initialization rather than applying painter transformations dynamically during rendering.
