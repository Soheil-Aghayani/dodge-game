import time
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from main import GameWindow
from module.block import Block

app = QApplication(sys.argv)
window = GameWindow()
window.start_game()
game = window.game_widget

# spawn 1000 blocks
for _ in range(1000):
    game.spawn_block()

start = time.time()
for _ in range(1000):
    game.update_game()
end = time.time()
print(f"update_game 1000x: {end - start:.4f}s")
