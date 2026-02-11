from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QApplication
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

class DeathScreen(QWidget):
    restart_signal = pyqtSignal()  # Signal to restart the game
    
    def __init__(self, score):
        super().__init__()
        self.setWindowTitle("Game Over")
        self.setFixedSize(300, 200)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 200);
                color: white;
            }
            QPushButton {
                background-color: #444444;
                border: none;
                padding: 10px;
                min-width: 100px;
                color: white;
            }
            QPushButton:hover {
                background-color: #666666;
            }
        """)
        
        # Create layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        # Game Over text
        game_over_label = QLabel("Game Over!")
        game_over_label.setFont(QFont('Arial', 24, QFont.Bold))
        game_over_label.setAlignment(Qt.AlignCenter)
        
        # Score text
        score_label = QLabel(f"Score: {score}")
        score_label.setFont(QFont('Arial', 18))
        score_label.setAlignment(Qt.AlignCenter)
        
        # Restart button
        restart_button = QPushButton("Restart")
        restart_button.setFont(QFont('Arial', 12))
        restart_button.clicked.connect(self._on_restart)
        
        # Add widgets to layout
        layout.addWidget(game_over_label)
        layout.addWidget(score_label)
        layout.addWidget(restart_button)
        
        self.setLayout(layout)
        
    def _on_restart(self):
        self.restart_signal.emit()
        self.close()
        
    def showEvent(self, event):
        # Center the widget on the screen
        screen = QApplication.primaryScreen().geometry()
        self.move(
            screen.center().x() - self.width() // 2,
            screen.center().y() - self.height() // 2
        ) 