## 2023-10-27 - [Pre-scale Images in Render Loops]
**Learning:** PyQt game loops suffer massive performance degradation if QPixmap.scaled() is called dynamically on every frame inside a draw() or paintEvent() method.
**Action:** Always pre-scale QPixmaps and cache them (e.g., as `self.scaled_image` or `self.scaled_frames`) in the `__init__` or `resizeEvent` phase before rendering to avoid runtime bottlenecks.

## 2024-05-18 - [Pre-scale Large Rotating Entities at Initialization]
**Learning:** Calling QPixmap.scaled() along with QPainter coordinate transformations (rotate/translate) on a huge raw image (e.g. 350x336 barrel) every single frame inside `draw()`/`paintEvent()` creates severe render loop bottleneck (takes ~3.5x longer).
**Action:** When working with dynamic elements that rotate or pulse, pre-scale the underlying image to its max expected target size directly in `__init__` before storing it. Then, `draw()` can apply transformations onto the already small pre-scaled image, saving considerable CPU time per frame.
