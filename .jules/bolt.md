## 2024-05-18 - Pre-scale Shield Animations for PyQt
**Learning:** PyQt `QPixmap.scaled` is an expensive operation and severely impacts frame rates when called continuously inside a `draw()` or `paintEvent()` render loop (like what was happening with `Shield`).
**Action:** When a static image or animation is resized for display (like making a shield larger than a player), always pre-scale and cache the `QPixmap` during `__init__` rather than recalculating it dynamically in `draw()`.
