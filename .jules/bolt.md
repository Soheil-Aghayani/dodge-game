## 2025-02-28 - Pre-scale Images in PyQt Render Loops
**Learning:** Calling `.scaled()` on `QPixmap` inside `draw()` or `paintEvent()` is a severe performance bottleneck in PyQt game loops, as it performs expensive image processing on every frame.
**Action:** Always pre-scale images (like shields or explosions) during initialization or when sizes explicitly change, cache the scaled `QPixmap` in an instance variable, and draw the cached image directly.
