## 2025-04-09 - Avoid continuous QPixmap.scaled in paintEvent
**Learning:** Performing `QPixmap.scaled` operations with `Qt.SmoothTransformation` inside a widget's `paintEvent` creates a severe performance bottleneck because `paintEvent` runs frequently (e.g., during animations or updates).
**Action:** Always cache the scaled image in a class attribute (like `_scaled_background`) and update it only when the size changes, typically by overriding `resizeEvent`.
