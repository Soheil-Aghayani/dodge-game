from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint
from PyQt5.QtGui import QFont, QPainter, QColor, QLinearGradient, QPen, QFontDatabase
from module.sound_manager import SoundManager
from module.menu_background import MenuBackground
import math
import time
import os

class StyledButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(250, 60)
        
        # Load custom font
        current_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(current_dir, "asset", "font", "KarenFat.ttf")
        try:
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id != -1:
                font_families = QFontDatabase.applicationFontFamilies(font_id)
                if font_families:
                    font_family = font_families[0]
                else:
                    print(f"Warning: No font families found for {font_path}")
                    font_family = 'Arial'
            else:
                print(f"Warning: Failed to load font from {font_path}")
                font_family = 'Arial'
        except Exception as e:
            print(f"Error loading font: {e}")
            font_family = 'Arial'
            
        self.setFont(QFont(font_family, 20))
        self.setCursor(Qt.PointingHandCursor)
        
        # Custom styling with semi-transparent background
        self.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 76, 76, 180);
                color: white;
                border: none;
                border-radius: 30px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: rgba(255, 107, 107, 200);
            }
            QPushButton:pressed {
                background-color: rgba(255, 51, 51, 220);
            }
        """)
        
    def enterEvent(self, event):
        super().enterEvent(event)
        # Get the MainMenu instance and play cursor sound
        main_menu = self.parent()
        if hasattr(main_menu, 'sound_manager'):
            main_menu.sound_manager.play_cursor()

class MainMenu(QWidget):
    def __init__(self, parent, sound_manager):
        super().__init__()
        self.parent = parent
        self.sound_manager = sound_manager
        self.title_y_offset = 0
        
        # Load custom font
        current_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(current_dir, "asset", "font", "KarenFat.ttf")
        try:
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id != -1:
                font_families = QFontDatabase.applicationFontFamilies(font_id)
                if font_families:
                    self.font_family = font_families[0]
                else:
                    print(f"Warning: No font families found for {font_path}")
                    self.font_family = 'Arial'
            else:
                print(f"Warning: Failed to load font from {font_path}")
                self.font_family = 'Arial'
        except Exception as e:
            print(f"Error loading font: {e}")
            self.font_family = 'Arial'
            
        # Setup background
        self.background = MenuBackground(self)
        self.background.setGeometry(0, 0, self.width(), self.height())
        
        self.setup_ui()
        self.setup_animation()
        
    def setup_ui(self):
        # Create layout with more spacing
        layout = QVBoxLayout()
        layout.setSpacing(30)
        layout.setContentsMargins(50, 100, 50, 100)
        
        # Game title
        self.title = QLabel("Dodge the Blocks")
        self.title.setFont(QFont(self.font_family, 48))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: white;")
        layout.addWidget(self.title)
        
        # Add some spacing
        layout.addSpacing(40)
        
        # Start button with custom styling
        self.start_button = StyledButton("Start Game")
        self.start_button.clicked.connect(self.start_game)
        layout.addWidget(self.start_button, alignment=Qt.AlignCenter)
        
        # Settings button
        self.settings_button = StyledButton("Settings")
        self.settings_button.clicked.connect(self.show_settings)
        layout.addWidget(self.settings_button, alignment=Qt.AlignCenter)
        
        # Exit button
        self.exit_button = StyledButton("Exit")
        self.exit_button.clicked.connect(self.exit_game)
        layout.addWidget(self.exit_button, alignment=Qt.AlignCenter)
        
        # Game over label (initially hidden)
        self.game_over_label = QLabel()
        self.game_over_label.setFont(QFont(self.font_family, 24))
        self.game_over_label.setAlignment(Qt.AlignCenter)
        self.game_over_label.setStyleSheet("color: white;")
        self.game_over_label.hide()
        layout.addWidget(self.game_over_label)
        
        self.setLayout(layout)
        
    def setup_animation(self):
        # Title bounce animation with reduced movement
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_title_animation)
        self.animation_timer.start(50)  # 20 FPS for smooth animation
        
    def update_title_animation(self):
        # Update title position with reduced sine wave movement
        self.title_y_offset = math.sin(int(time.time() * 1000) / 300) * 5
        self.title.move(self.title.x(), self.title.y() + int(self.title_y_offset))
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Update background size when window is resized
        self.background.setGeometry(0, 0, self.width(), self.height())
        
    def start_game(self):
        self.sound_manager.play_cursor()
        self.parent.start_game()
        
    def show_settings(self):
        self.sound_manager.play_cursor()
        self.parent.show_settings()
        
    def exit_game(self):
        self.sound_manager.play_cursor()
        self.parent.close()

    def show_game_over(self, score):
        self.game_over_label.setText(f"Game Over!\nScore: {score}")
        self.game_over_label.show() 