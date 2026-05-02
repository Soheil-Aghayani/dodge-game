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
