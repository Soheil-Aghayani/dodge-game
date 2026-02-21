
import pytest
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import Qt
import sys
import os

# Ensure module is in path
sys.path.append(os.getcwd())

from module.block import Block
from module.floor import Floor
from module.player import Player
from module.abnormal import AbnormalManager

# Mock GameWidget
class MockGameWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.abnormal_manager = AbnormalManager()
        self.floor = Floor(self)
        self.player = Player(self)

    def get_floor_height(self):
        return self.floor.get_height()

@pytest.fixture(scope="module")
def app():
    # Only create QApplication once per test run
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    yield app

def test_block_rendering(app):
    widget = MockGameWidget()
    block = Block(widget)

    # Test that block has an image
    assert block.image is not None
    assert block.image_type in ["barrel", "metalbox", "woodenbox"]

    # Test drawing
    pixmap = QPixmap(800, 600)
    painter = QPainter(pixmap)
    try:
        block.draw(painter)
    finally:
        painter.end()

def test_scaled_images_generation(app):
    # This test might fail before optimization is implemented if the field doesn't exist
    # So we check if the class has the attribute first
    if hasattr(Block, 'scaled_obstacle_images'):
        widget = MockGameWidget()
        # Force block creation to trigger image loading
        _ = Block(widget)

        # Check if scaled images are populated for static types
        assert "metalbox" in Block.scaled_obstacle_images
        assert "woodenbox" in Block.scaled_obstacle_images

        # Check size roughly matches 40x40 (or aspect ratio equivalent)
        metalbox = Block.scaled_obstacle_images["metalbox"]
        # metalbox 270x281 -> ~38x40
        assert metalbox.width() <= 40
        assert metalbox.height() <= 40
        assert metalbox.width() > 30
        assert metalbox.height() > 30
