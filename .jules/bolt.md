## 2023-10-27 - [Pre-scale Images in Render Loops]
**Learning:** PyQt game loops suffer massive performance degradation if QPixmap.scaled() is called dynamically on every frame inside a draw() or paintEvent() method.
**Action:** Always pre-scale QPixmaps and cache them (e.g., as `self.scaled_image` or `self.scaled_frames`) in the `__init__` or `resizeEvent` phase before rendering to avoid runtime bottlenecks.
## 2023-11-20 - [Pre-scale Images in Pause Screen]
**Learning:** PyQt game loops suffer massive performance degradation if QPixmap.scaled() is called dynamically on every frame inside paintEvent(). The PauseScreen widget was recalculating its scaled background image on every paint event.
**Action:** Always pre-scale QPixmaps and cache them (e.g., as `self._scaled_background`) during `resizeEvent` before rendering to avoid runtime bottlenecks.
