## 2026-05-18 - [Cache entity geometries to optimize collision hot-paths]
**Learning:** In PyQt game loops, repeatedly performing arithmetic operations like float multiplication (e.g., `self.width * 0.7`) and integer division (e.g., `self.width // 2`) inside a `get_rect()` method causes noticeable overhead when these calculations happen on thousands of entities per second during collision loops.
**Action:** Identify static entity dimensions and offsets and pre-calculate them during `__init__` (e.g., `self.hitbox_width`, `self.hitbox_offset_x`), allowing `get_rect()` to just return a tuple using simple addition.

## 2026-05-19 - [Cache static bounding box offsets and multipliers]
**Learning:** In highly-executed methods such as `draw()` or `get_rect()`, simple integer division like `self.width // 2` or constant bounding calculations can accumulate to create overhead over many iterations in python. Additionally, relying on dimensions passed from external sources when internal state should be definitive can lead to regressions if variables are misused.
**Action:** Always pre-calculate and store static multiplier results like `self.half_width` or static scales during `__init__`. Also, ensure these variables are unconditionally initialized so that they are guaranteed to exist when the instance methods invoke them.
