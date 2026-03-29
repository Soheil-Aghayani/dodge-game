import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPixmap, QPainter
from module.shield import Shield
from module.player import Player
from module.explosion import ExplosionAnimation
from module.floor import Floor

class DummyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.floor = Floor(self)

app = QApplication(sys.argv)
widget = DummyWidget()
player = Player(widget)

shield = Shield(player)
print("Shield pre-scaled image exists:", hasattr(shield, 'scaled_image'))

explosion = ExplosionAnimation(0, 0, 40)
print("Explosion scaled frames exists:", hasattr(explosion, 'scaled_frames'))
