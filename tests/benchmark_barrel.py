import sys
import time
import os
import math
import random
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPainter, QPixmap, QColor
from PyQt5.QtCore import Qt

# Add repository root to path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from module.block import Block

class MockGameWidget:
    def __init__(self):
        self.abnormal_manager = MockAbnormalManager()
        self.floor = MockFloor()
    def width(self):
        return 800
    def height(self):
        return 600

class MockAbnormalManager:
    def is_active(self):
        return False
    def get_type(self):
        return None

class MockFloor:
    def get_y_position(self):
        return 550

def run_benchmark():
    app = QApplication(sys.argv)

    # Mock game widget
    game_widget = MockGameWidget()

    # Initialize Block
    # This will trigger the loading of images in Block.obstacle_images
    block = Block(game_widget)

    # Force the block to be a barrel
    block.image_type = "barrel"
    # Ensure it uses the loaded image
    if "barrel" in Block.obstacle_images:
        block.image = Block.obstacle_images["barrel"]
        print(f"Loaded barrel image size: {block.image.width()}x{block.image.height()}")
    else:
        print("Error: Barrel image not loaded!")
        return

    block.should_rotate = True
    block.should_pulse = True
    block.width = 50
    block.height = 50
    block.x = 100
    block.y = 100

    # Canvas to draw on
    pixmap = QPixmap(800, 600)
    pixmap.fill(QColor(0, 0, 0))

    # Warm up
    painter = QPainter(pixmap)
    for _ in range(100):
        block.draw(painter)
        block.angle = (block.angle + 2) % 360
    painter.end()

    # Benchmark
    start_time = time.time()
    iterations = 5000  # Default iterations

    print(f"Benchmarking {iterations} draws of barrel...")

    painter = QPainter(pixmap)
    for i in range(iterations):
        block.draw(painter)
        block.angle = (block.angle + 2) % 360
        # Simulate pulse update slightly
        block.pulse_time += 0.1
    painter.end()

    end_time = time.time()

    duration = end_time - start_time
    print(f"Total time: {duration:.4f} seconds")
    print(f"Average time per draw: {duration/iterations*1000:.4f} ms")
    print(f"FPS equivalent (draw only): {iterations/duration:.2f}")

if __name__ == "__main__":
    run_benchmark()
