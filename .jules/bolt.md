## 2024-05-24 - [Avoid `QPixmap.scaled` in `draw` or `paintEvent`]
**Learning:** In PyQt5 rendering loops, repeatedly calling `QPixmap.scaled()` on images (like explosions and shields) inside the `draw` or `paintEvent` method is a severe performance bottleneck. It causes significant lag as it continuously calculates the new dimensions on every frame.
**Action:** Always pre-scale images to their required sizes during initialization (`__init__`) and store them in instance attributes. Then, simply draw the pre-scaled attributes inside the main rendering loop.
