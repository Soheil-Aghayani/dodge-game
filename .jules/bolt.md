## 2024-05-24 - PyQt paintEvent Optimization
**Learning:** Calling `QPixmap.scaled` with `Qt.SmoothTransformation` inside `paintEvent` is a severe performance bottleneck because `paintEvent` can be triggered frequently (animations, UI updates).
**Action:** Always pre-scale and cache background images. Introduce a `_scaled_background` property and update it inside `resizeEvent`, then simply draw the cached image in `paintEvent`.
