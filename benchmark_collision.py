import time
import random

def run_benchmark():
    # Setup
    num_blocks = 1000
    iterations = 10000

    blocks = []
    for _ in range(num_blocks):
        bx = random.randint(0, 800)
        by = random.randint(0, 600)
        bw = 50
        bh = 50
        blocks.append((bx, by, bw, bh))

    px, py, pw, ph = 400, 300, 48, 81

    # Old method
    start = time.time()
    for _ in range(iterations):
        for bx, by, bw, bh in blocks:
            if by + 150 < py or by - 150 > py + ph or bx + 150 < px or bx - 150 > px + pw:
                continue
            if not (px >= bx + bw or px + pw <= bx or py >= by + bh or py + ph <= by):
                pass
    old_time = time.time() - start

    # New method
    start = time.time()
    for _ in range(iterations):
        player_right = px + pw
        player_bottom = py + ph
        for bx, by, bw, bh in blocks:
            if by + 150 < py or by - 150 > player_bottom or bx + 150 < px or bx - 150 > player_right:
                continue
            if not (px >= bx + bw or player_right <= bx or py >= by + bh or player_bottom <= by):
                pass
    new_time = time.time() - start

    print(f"Old time: {old_time:.4f}s")
    print(f"New time: {new_time:.4f}s")
    print(f"Speedup: {old_time / new_time:.2f}x")

run_benchmark()
