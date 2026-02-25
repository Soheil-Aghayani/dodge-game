
import pytest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap
import sys
import os
from module.block import Block

# Need a QApplication for QPixmap to work
@pytest.fixture(scope="session")
def qapp():
    if not QApplication.instance():
        app = QApplication(sys.argv)
        yield app
    else:
        yield QApplication.instance()

class MockGameWidget:
    def __init__(self):
        self.width = lambda: 800
        self.height = lambda: 600
        self.abnormal_manager = MockAbnormalManager()
        self.floor = MockFloor()

class MockAbnormalManager:
    def is_active(self): return False
    def get_type(self): return None

class MockFloor:
    def get_y_position(self): return 500

def test_barrel_image_optimization(qapp):
    # Ensure Block class is reset or initialized
    # Since Block.obstacle_images is a class variable, we need to be careful.
    # If other tests ran before, it might already be initialized.
    # But since we are in a separate process or fresh run, it should be fine.

    # We can force re-initialization by clearing it if needed, but let's assume standard flow.
    Block.obstacle_images = {} # clear just in case

    game_widget = MockGameWidget()
    _ = Block(game_widget)

    # Check barrel image size
    barrel_img = Block.obstacle_images.get("barrel")
    assert barrel_img is not None
    assert barrel_img.width() == 100
    # Height should be scaled proportionally.
    # Original: 350x336. Aspect ratio ~1.04
    # New height should be roughly 100 * (336/350) = 96
    assert 90 <= barrel_img.height() <= 100

    # Check metalbox image size (should be original)
    metalbox_img = Block.obstacle_images.get("metalbox")
    assert metalbox_img is not None
    assert metalbox_img.width() > 200 # Original is 270

    # Check woodenbox image size (should be original)
    woodenbox_img = Block.obstacle_images.get("woodenbox")
    assert woodenbox_img is not None
    assert woodenbox_img.width() > 200 # Original is 292
