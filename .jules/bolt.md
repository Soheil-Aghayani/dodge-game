## 2026-03-10 - Pre-scaling Explosion Animation Frames
**Learning:** In PyQt render loops, calling QPixmap.scaled on animation frames during the paintEvent/draw method creates a severe bottleneck. Frames for rapidly spawning entities like explosions must be pre-scaled once during initialization.
**Action:** When working with QPixmap animations in PyQt that don't change size dynamically, scale all frames in __init__ and store them in a self.scaled_frames list.
