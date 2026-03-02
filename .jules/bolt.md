## 2024-03-02 - Cache QPixmap.scaled() Results

**Learning:** Calling `QPixmap.scaled()` directly inside `paintEvent` or `draw` methods creates massive overhead during the render loop in PyQt5, significantly decreasing frame rates, especially for frequently drawn components like shields and explosion animations.
**Action:** Always pre-scale and cache `QPixmap` assets in `__init__` (or lazily upon the first call) instead of performing the transformation every single frame. When the target bounds are flexible, implement a `resizeEvent` handler to compute and store the `_scaled_background` once.