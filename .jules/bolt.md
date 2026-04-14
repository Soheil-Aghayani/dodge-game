## 2023-10-27 - [Pre-scale Images in Render Loops]
**Learning:** PyQt game loops suffer massive performance degradation if QPixmap.scaled() is called dynamically on every frame inside a draw() or paintEvent() method.
**Action:** Always pre-scale QPixmaps and cache them (e.g., as `self.scaled_image` or `self.scaled_frames`) in the `__init__` or `resizeEvent` phase before rendering to avoid runtime bottlenecks.
## 2023-10-27 - [Dynamic Image Scaling Optmization]
**Learning:** In PyQt game loops, large dynamic images that undergo continuous transformations (e.g., pulsating and rotating barrels in `Block`) should be pre-scaled once to their base render size during initialization. Attempting to scale a very large original image on every frame down to a smaller size is highly inefficient and creates significant performance bottlenecks.
**Action:** Overwrite the original large image in memory with its pre-scaled base version, ensuring that any subsequent frame transformations (like sine-wave based scaling for pulsing) operate on a much smaller and more efficient base image size.
