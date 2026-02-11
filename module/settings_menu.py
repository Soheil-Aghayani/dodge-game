from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QFontDatabase
from module.menu_background import MenuBackground
import os

class SettingsMenu(QWidget):
    def __init__(self, parent, sound_manager):
        super().__init__()
        self.parent = parent
        self.sound_manager = sound_manager
        
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
            
        self.setup_ui()

    def setup_ui(self):
        # Setup background
        self.background = MenuBackground(self)
        self.background.setGeometry(0, 0, self.width(), self.height())
        
        # Create main layout
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(50, 100, 50, 100)
        
        # Title
        title = QLabel("Settings")
        title.setFont(QFont(self.font_family, 48))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white;")
        main_layout.addWidget(title)
        
        # Add some spacing
        main_layout.addSpacing(40)
        
        # Settings Container
        settings_container = QWidget()
        settings_container.setFixedWidth(600)
        settings_layout = QVBoxLayout(settings_container)
        settings_layout.setSpacing(30)
        settings_layout.setContentsMargins(20, 20, 20, 20)

        # Sound Toggle Container
        sound_container = QWidget()
        sound_container.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 0.3);
                border-radius: 15px;
                padding: 20px;
            }
        """)
        sound_layout = QVBoxLayout(sound_container)
        sound_layout.setSpacing(20)

        # Sound Toggle
        sound_toggle_layout = QHBoxLayout()
        sound_toggle_layout.setAlignment(Qt.AlignLeft)
        sound_toggle_label = QLabel("Sound Effects")
        sound_toggle_label.setFont(QFont(self.font_family, 24))
        sound_toggle_label.setStyleSheet("color: white;")
        self.sound_toggle = QCheckBox()
        self.sound_toggle.setChecked(self.sound_manager.sound_enabled)
        self.sound_toggle.stateChanged.connect(self.toggle_sound)
        self.sound_toggle.setStyleSheet("""
            QCheckBox {
                width: 40px;
                height: 40px;
            }
            QCheckBox::indicator {
                width: 40px;
                height: 40px;
            }
            QCheckBox::indicator:unchecked {
                background-color: rgba(0, 0, 0, 0.5);
                border: 2px solid #999;
                border-radius: 20px;
            }
            QCheckBox::indicator:checked {
                background-color: #F44336;
                border: 2px solid #EF5350;
                border-radius: 20px;
            }
            QCheckBox::indicator:hover {
                border-color: #fff;
            }
        """)
        sound_toggle_layout.addWidget(sound_toggle_label)
        sound_toggle_layout.addWidget(self.sound_toggle)
        sound_toggle_layout.addStretch()
        sound_layout.addLayout(sound_toggle_layout)

        settings_layout.addWidget(sound_container)

        # Back Button
        self.back_button = QPushButton("Back")
        self.back_button.setFont(QFont(self.font_family, 24))
        self.back_button.setFixedSize(200, 50)
        self.back_button.setCursor(Qt.PointingHandCursor)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                border: none;
                border-radius: 25px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #EF5350;
            }
            QPushButton:pressed {
                background-color: #E53935;
            }
        """)
        self.back_button.clicked.connect(self.go_back)
        settings_layout.addWidget(self.back_button, alignment=Qt.AlignCenter)

        main_layout.addWidget(settings_container, alignment=Qt.AlignCenter)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Update background size when window is resized
        self.background.setGeometry(0, 0, self.width(), self.height())

    def toggle_sound(self, state):
        self.sound_manager.toggle_sound(state == Qt.Checked)
        self.sound_manager.play_cursor()

    def go_back(self):
        self.sound_manager.play_cursor()
        self.parent.show_main_menu() 