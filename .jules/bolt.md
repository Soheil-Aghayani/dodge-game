## 2023-10-27 - [Pre-scale Images in Render Loops]
**Learning:** PyQt game loops suffer massive performance degradation if QPixmap.scaled() is called dynamically on every frame inside a draw() or paintEvent() method.
**Action:** Always pre-scale QPixmaps and cache them (e.g., as `self.scaled_image` or `self.scaled_frames`) in the `__init__` or `resizeEvent` phase before rendering to avoid runtime bottlenecks.
## 2024-04-19 - Pre-scale dynamic block images
**Learning:** Downscaling high-res images directly within the `paintEvent` or `draw` loop to process transformations causes massive CPU rendering bottlenecks, even when aspect-ratio constraints are used. This logic applied to the `barrel` item in `module/block.py` was being parsed on each frame instead of caching the scaled state.
**Action:** Always pre-scale assets when initializing object pools. Avoid putting base scaling routines into rendering functions. Pre-scaled base components still scale up gracefully via PyQt Transform attributes, enabling more effective use of computational resources.
## 2024-05-29 - [Pre-scale Images in Render Loops for PauseScreen]
**Learning:** PyQt game loops and UI overlays suffer massive performance degradation if QPixmap.scaled() is called dynamically on every paintEvent() method. For `PauseScreen`, this was reducing paintEvent performance from ~0.008s down to ~0.265s for 100 loops.
**Action:** Always pre-scale QPixmaps and cache them (e.g., as `self._scaled_background`) in the `__init__` or `resizeEvent` phase before rendering to avoid runtime bottlenecks.
## 2024-06-25 - [Pre-scale Sprite Flips in Render Loops]
**Learning:** In PyQt game loops, dynamically flipping sprites using `painter.scale(-1, 1)` and `painter.translate` during `paintEvent` or `draw` methods is significantly slower (~6.8x slower in benchmarks) than drawing pre-cached transformed pixmaps.
**Action:** When initializing animation frames, use `QPixmap.transformed(QTransform().scale(-1, 1))` to pre-cache horizontally flipped versions of the frames alongside the normal ones. Then, select the correct pre-cached frame based on the facing direction to avoid expensive transform state changes in the render loop.
## 2024-08-01 - [Pre-cache Fonts, Colors, and Static Metrics in Render Loops]
**Learning:** In PyQt game loops, repeatedly instantiating `QFont` and `QColor` objects, or dynamically calculating static text boundaries using `QFontMetrics.boundingRect()` inside `paintEvent()`, creates significant performance overhead (hundreds of milliseconds over 10k loops).
**Action:** Always pre-cache these objects and metrics during widget initialization (e.g., in `__init__`) as instance variables and reuse them in the render loop.

## 2024-04-24 - [Avoid Instantiating UI Primitives in PyQt Loops]
**Learning:** Instantiating `QFont`, `QColor`, and calculating `QFontMetrics.boundingRect` dynamically inside `paintEvent` creates significant overhead in PyQt since these methods are called every frame.
**Action:** Always instantiate immutable styling objects (`QFont`, `QColor`) and pre-compute static text boundaries using `QFontMetrics` inside `__init__` (or whenever the underlying static data changes) to pass them directly to the `QPainter` within `paintEvent`.
## 2024-08-02 - [Cache static QFontMetrics bounding rects]
**Learning:** Calling `QFontMetrics.boundingRect` dynamically for static texts inside a PyQt `paintEvent` introduces unnecessary layout calculation overhead on every frame, reducing frame rate.
**Action:** Identify static strings (e.g. static UI labels, game over texts, warning instructions) and pre-calculate their bounding rects in the `__init__` function using `QFontMetrics` to avoid repeated computation in `paintEvent`.
## 2024-05-24 - [Tiling Optimization]
**Learning:** Tiling an image across the screen using a loop of `painter.drawPixmap` calls inside a PyQt `paintEvent` or `draw` loop is highly inefficient.
**Action:** Pre-render the tiled pattern onto a single, full-width `QPixmap` (e.g., initialized during `__init__` and updated when the window width changes) and draw the single cached image to achieve a significant performance boost.
## 2024-05-01 - [Avoid eager evaluation in dict.get for costly functions]
**Learning:** In Python, using `dict.get(key, expensive_function())` forces the `expensive_function()` to execute eagerly, even when `key` already exists in the dictionary. When applied to calculating static bounding rects like `painter.fontMetrics().boundingRect` inside a PyQt `paintEvent`, it negates caching entirely.
**Action:** Use an `if key not in dict:` block to compute and cache expensive operations lazily instead of relying on `dict.get()` with default function calls.
## 2024-08-05 - [Avoid Inline Dictionary Instantiation in Render Loops]
**Learning:** Avoid inline dictionary definitions (e.g. `{...}.get(key)`) inside highly-called functions like `paintEvent` or `draw` methods, as recreating the dictionary every frame causes unnecessary garbage collection and memory overhead.
**Action:** Pre-initialize such static mappings as class attributes in `__init__` and reference them dynamically inside the rendering functions.
## 2024-11-20 - [Avoid redundant property lookups and C++ crossings in hot loops]
**Learning:** In PyQt game loops, repeatedly invoking C++ properties or methods (like `.width()`, `.height()`, or `.get_rect()`) and re-calculating identical bounding areas inside high-frequency `paintEvent` or `update_game` loops causes notable performance overhead due to the continuous Python-to-C++ boundary crossings.
**Action:** Always pre-cache structural dimension values (`img.width()`, `img.height()`) in `__init__` when they remain constant. Furthermore, pull loop-invariant calculations (such as evaluating the player's bounding rect before checking collisions against all blocks) completely outside the iteration scope.
## 2026-05-01 - [Pull loop-invariant C++ calls outside render loops]
**Learning:** In PyQt game loops, repeatedly invoking C++ properties or methods (like `.width()`, `.height()`, or `.get_y_position()`) and calculating state inside high-frequency loops (like `update_game` iterating over `blocks` or glitch loops) causes notable performance overhead due to continuous Python-to-C++ boundary crossings.
**Action:** Always pre-calculate loop-invariant values (like `self.width()`, `self.floor.get_y_position()`, and abnormal state queries) *before* entering inner iterative loops and pass them as arguments to update methods (like `Block.update()`) to minimize C++ boundary calls.

## 2026-05-02 - [Pre-cache randomized UI primitives in render loops]
**Learning:** Instantiating random UI primitives (like `QColor`) dynamically inside a high-frequency loop within `paintEvent` (e.g., glitch effects drawing 20 random color rects per frame) causes significant performance overhead due to repeated object creation and garbage collection.
**Action:** Pre-compute a pool of randomized UI primitives (like a list of 50 random `QColor` objects) during initialization (e.g., in `__init__`) and use `random.choice()` from this cached pool during the render loop to achieve the same visual effect without the overhead of instantiation.
## 2024-11-21 - [Avoid redundant QPainter state save/restore]
**Learning:** Calling `painter.save()` and `painter.restore()` in high-frequency PyQt render loops introduces unnecessary overhead by pushing and popping the C++ state matrix. If a draw method only executes non-mutating operations like `painter.drawPixmap()`, these state preservation calls are completely redundant.
**Action:** Remove `painter.save()` and `painter.restore()` around simple draw operations to reduce C++ boundary overhead and improve rendering performance.
## 2024-11-21 - [Pre-cache dynamic properties in paintEvent]
**Learning:** In PyQt5, repeatedly calling instance properties like `self.width()`, `self.height()`, and `self.rect()` inside the rendering function (especially inside loops, such as glitch effects) results in thousands of redundant Python-to-C++ boundary crossings per second.
**Action:** Always fetch loop-invariant structural properties into local Python variables at the very top of `paintEvent()` or `draw()` (e.g., `w = self.width()`) and use those local variables throughout the function to avoid boundary overhead.
## 2024-11-21 - [Avoid redundant object creation and inline imports in render loops]
**Learning:** Instantiating `QColor` (e.g., `QColor(255, 0, 0)`) or dynamically importing modules (`from PyQt5.QtGui import QColor`) inside a `draw()` or `paintEvent()` loop adds unnecessary garbage collection and module-resolution overhead that triggers per-frame for every object drawn.
**Action:** Move all UI object instantiations to `__init__` or as class variables to cache them, and ensure all imports reside at the top of the file.
## 2024-11-21 - [Pre-cache Animation Frames globally]
**Learning:** Loading and pre-scaling identical animation frames from disk for every newly spawned entity (like `ExplosionAnimation` or `Player`) introduces unnecessary I/O blocking and memory overhead.
**Action:** Use a class-level dictionary (`_global_frame_cache` for base animation frames, or `_cached_scaled_frames_by_size` for size-specific derived frames) keyed by logical attributes (like folder name or scaled dimensions) to store processed `QPixmap` arrays so they can be reused instantaneously across multiple instances.
## 2024-11-21 - [Pre-render Opacity in QPixmaps]
**Learning:** In PyQt game loops, modifying `QPainter` opacity dynamically per frame (e.g., `painter.setOpacity(0.7)`) is computationally expensive (~20% slower in benchmarks).
**Action:** When drawing semi-transparent, static images (like a player shield), pre-render the opacity into a cached `QPixmap` during initialization by creating a transparent canvas and drawing the image onto it with the desired opacity, thereby avoiding dynamic opacity changes in the high-frequency `draw` or `paintEvent` loops.
## 2024-11-21 - [Optimize List Iteration and Deletion in Game Loops]
**Learning:** In high-frequency game loops (e.g., `update_game`), iterating over a shallow copy of a list (`for block in self.blocks[:]:`) and using `.remove(block)` introduces significant overhead due to $O(N)$ allocation for the copy and $O(N)$ search time per removal.
**Action:** Iterate backwards using `range(len(self.blocks) - 1, -1, -1)` and safely remove elements using `.pop(i)`. This avoids the shallow copy allocation and avoids the initial search overhead.
## 2024-11-21 - [Replace QTime with time.time() in Game Loops]
**Learning:** In PyQt game loops, repeatedly calling `QTime.currentTime().msecsSinceStartOfDay()` to calculate delta times causes significant performance overhead (~32x slower in benchmarks) due to the constant Python-to-C++ boundary crossings required to instantiate the `QTime` object.
**Action:** Replace `QTime.currentTime().msecsSinceStartOfDay()` with Python's native `int(time.time() * 1000)` or `time.time_ns() // 1_000_000` to calculate timestamps and deltas directly in Python space, avoiding C++ boundary overhead entirely in high-frequency update loops.
## 2026-05-13 - [Pass pre-calculated floor_y to avoid redundant C++ property lookups in Player update]
**Learning:** In PyQt game loops, calling `self.game_widget.floor.get_y_position()` within nested update loops like `Player.update()` causes repeated Python-to-C++ boundary crossings when it could be calculated once at the start of `update_game`.
**Action:** Extract loop-invariant evaluations like `floor_y` to the top of the update loop and pass them down to nested update functions as arguments to avoid C++ overhead.
## 2026-05-14 - [Pre-cache dynamically rotated QPixmaps]
**Learning:** In PyQt render loops, dynamically rotating images using `painter.rotate()` and `painter.translate()` every frame is a significant performance bottleneck (e.g. ~0.26s dynamically vs ~0.08s cached over 10k ops).
**Action:** Pre-cache rotated variants of a `QPixmap` (e.g., all 180 angles for a rotating barrel) using `QTransform().rotate()` during initialization and render the cached image directly using `painter.drawPixmap` to avoid this overhead in hot loops.
## 2026-05-17 - [Use Tuples for Collision Detection Hot Paths]
**Learning:** In PyQt games, repeatedly instantiating `QRect` objects or calling `.intersects()` and dimension-fetching methods inside high-frequency loops (like collision detection) causes severe performance degradation due to Python-C++ boundary crossings. Using plain Python tuples `(x, y, w, h)` and manual AABB math is significantly faster (~15x).
**Action:** When optimizing `QRect` out of hot loops by switching to Python tuples, avoid changing the return signature of widely used getters like `get_rect()`. Changing this signature can cause severe regressions in downstream Qt APIs that expect a `QRect` object (such as `painter.drawRect()`). Implement separate methods (e.g., `get_hitbox_tuple()`) or unpack the rect at the specific bottleneck to perform the tuple-based calculations safely.
## 2026-05-18 - [Cache entity geometries to optimize collision hot-paths]
**Learning:** In PyQt game loops, repeatedly performing arithmetic operations like float multiplication (e.g., `self.width * 0.7`) and integer division (e.g., `self.width // 2`) inside a `get_rect()` method causes noticeable overhead when these calculations happen on thousands of entities per second during collision loops.
**Action:** Identify static entity dimensions and offsets and pre-calculate them during `__init__` (e.g., `self.hitbox_width`, `self.hitbox_offset_x`), allowing `get_rect()` to just return a tuple using simple addition.
## 2026-05-18 - [Cache entity geometries to optimize collision hot-paths]
**Learning:** In PyQt game loops, repeatedly performing arithmetic operations like float multiplication (e.g., `self.width * 0.7`) and integer division (e.g., `self.width // 2`) inside a `get_rect()` method causes noticeable overhead when these calculations happen on thousands of entities per second during collision loops.
**Action:** Identify static entity dimensions and offsets and pre-calculate them during `__init__` (e.g., `self.hitbox_width`, `self.hitbox_offset_x`), allowing `get_rect()` to just return a tuple using simple addition.
## 2026-05-19 - [Cache rendered text as QPixmap to optimize QPainter.drawText]
**Learning:** In PyQt game loops, calling `painter.drawText()` with dynamically changing strings (like scores) or large static blocks of text (like game over screens) is significantly slower (up to 4-6x) than rendering a pre-cached `QPixmap`.
**Action:** When rendering text, evaluate if the text changes every frame. If it updates infrequently (like a score) or is static once triggered (like a death screen), pre-render the text onto a transparent `QPixmap` and use `painter.drawPixmap()` in the render loop. Re-render the cache only when the text content changes.

## 2026-05-20 - [Defer heavy geometry math in render loops]
**Learning:** In PyQt game loops, unconditionally calculating math for geometry (e.g., `scale`, `width`, `height`, `x`, `y`) at the start of a `draw()` method wastes CPU cycles if the subsequent conditional branches do not use them (e.g., when rendering a pre-cached object).
**Action:** Always defer heavy geometry math and variable initializations into the specific conditional blocks where they are actually utilized.

## 2026-05-20 - [Pass loop-invariant current_time to avoid redundant system calls]
**Learning:** In nested update loops (like `Block.update` called from `update_game`), invoking `int(time.time() * 1000)` locally for every entity creates redundant system call overhead when processing many entities.
**Action:** Calculate `current_time` once at the top of the main update loop and pass it as an argument to nested update functions to minimize system calls.
## 2026-05-20 - [Optimize Collision Hot-Paths with Broad-Phase Early Returns]
**Learning:** In PyQt games, collision detection inside high-frequency loops (like checking all blocks against the player every frame) can be a bottleneck. Calling methods to fetch bounding rects and doing complex AABB intersection checks on entities that are nowhere near each other wastes CPU cycles.
**Action:** Implement simple 1D bounding-volume broad-phase checks (e.g., `if self.y + 150 < py: return False`) at the start of collision methods to early-return before executing heavy math or method calls.
## 2026-06-12 - [Pre-cache random choice arguments in frequent instantiation]
**Learning:** In high-frequency object instantiation (e.g., spawning `Block`s every few frames), defining inline dictionaries (e.g., `weights = {'barrel': 0.5, ...}`) and calling `list(weights.keys())` to pass to `random.choices` causes redundant memory allocations and garbage collection overhead on every spawn.
**Action:** Define the keys and values as static, class-level lists (e.g., `_image_keys`, `_image_values`) and use those directly in `random.choices()` to optimize initialization speed.
## 2024-11-21 - [Optimize Collision Hot-Paths with 2D Broad-Phase Early Returns]
**Learning:** In PyQt games, 1D broad-phase checks (e.g. vertical boundaries only) on bounding volumes help filter out distant entities. However, extending these into 2D broad-phase checks by also verifying horizontal boundaries skips significantly more unneeded complex AABB generation (e.g., getting the explosion box sizes) and intersection calculation loops during collision.
**Action:** Implement 2D bounding-volume broad-phase checks (`if self.y + 150 < py or self.x + 150 < px: ...`) instead of 1D prior to complex arithmetic or generating full bounding boxes in collision detection loops.
## 2026-06-15 - [Use tuples for key event membership checks]
**Learning:** In PyQt5 key event handlers (e.g., `keyPressEvent`, `keyReleaseEvent`), using inline lists for membership checks (`in` / `not in`) causes unnecessary memory allocations and garbage collection overhead on every keyboard input.
**Action:** Use tuples (like `(Qt.Key_Left, Qt.Key_Right)`) rather than inline lists to avoid this overhead, as tuples are immutable and optimized by Python.
## 2026-06-30 - [Replace random.randint with random.random in high-frequency loops]
**Learning:** In high-frequency game logic (like spawning particles or drawing glitch effects with dozens of iterations per frame), calling `random.randint(a, b)` is noticeably slower than using `random.random()` with simple integer arithmetic (`int(random.random() * (b - a + 1)) + a`). Benchmarks show ~3x performance improvement.
**Action:** Replace `random.randint()` with optimized `random.random()` math in high-frequency render or update loops (like glitch drawing).
