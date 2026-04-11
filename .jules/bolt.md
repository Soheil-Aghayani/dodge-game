## 2023-10-27 - [Pre-scale Images in Render Loops]
**Learning:** PyQt game loops suffer massive performance degradation if QPixmap.scaled() is called dynamically on every frame inside a draw() or paintEvent() method.
**Action:** Always pre-scale QPixmaps and cache them (e.g., as `self.scaled_image` or `self.scaled_frames`) in the `__init__` or `resizeEvent` phase before rendering to avoid runtime bottlenecks.
## 2024-05-18 - [Dynamic Image Scaling]
**Learning:** In `module/block.py`, dynamic images that pulse or rotate (like 'barrel') should be pre-scaled directly within `Block.obstacle_images` during initialization rather than `Block.scaled_obstacle_images`, as the latter is used strictly as a fast-path that skips transformation logic for static blocks.
**Action:** When pre-scaling dynamic images that undergo further transformation, overwrite the original high-resolution image in the main cache dictionary with the scaled version to ensure downstream transformation logic operates on a smaller base image.
