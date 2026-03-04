
## 2024-03-04 - [Optimize Shield and Explosion Renderings]
**Learning:** In PyQt, calling `.scaled()` on `QPixmap` or image frames every frame inside `paintEvent` or `draw` methods significantly impacts performance. Pre-scaling dynamic entities like the `Shield` image and `Explosion` frames in their constructors avoids this expensive per-frame calculation, substantially improving rendering efficiency.
**Action:** When working with dynamic graphical elements in PyQt loops, pre-scale images and frames during object initialization or only when their specific size needs to change, instead of dynamically scaling them on every draw call.
