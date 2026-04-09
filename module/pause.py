from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QFont, QFontDatabase, QPixmap
import os

class PauseScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(800, 600)
        self.setFocusPolicy(Qt.StrongFocus)
        
        # Load background image
        current_dir = os.path.dirname(os.path.abspath(__file__))
        background_path = os.path.join(current_dir, "asset", "background", "pause_background.png")
        self.background = QPixmap(background_path)
        self._scaled_background = None
        
        # Load custom font
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
            
        # Create buttons
        self.setup_buttons()
            
    def setup_buttons(self):
        # Create main vertical layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        
        # Create horizontal layout for centering buttons
        h_layout = QHBoxLayout()
        
        # Create vertical layout for buttons
        button_layout = QVBoxLayout()
        button_layout.setSpacing(20)
        
        # Create buttons with custom styling
        self.resume_button = self.create_button("Resume")
        self.restart_button = self.create_button("Restart")
        self.menu_button = self.create_button("Return to Menu")
        
        # Connect buttons to actions
        self.resume_button.clicked.connect(self.resume_action)
        self.restart_button.clicked.connect(self.restart_action)
        self.menu_button.clicked.connect(self.menu_action)
        
        # Add buttons to button layout
        button_layout.addWidget(self.resume_button, 0, Qt.AlignCenter)
        button_layout.addWidget(self.restart_button, 0, Qt.AlignCenter)
        button_layout.addWidget(self.menu_button, 0, Qt.AlignCenter)
        
        # Add button layout to horizontal layout for centering
        h_layout.addStretch()
        h_layout.addLayout(button_layout)
        h_layout.addStretch()
        
        # Add everything to main layout
        main_layout.addStretch()
        main_layout.addLayout(h_layout)
        main_layout.addStretch()
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self.background.isNull() and not self.size().isEmpty():
            self._scaled_background = self.background.scaled(
                self.size(),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )
        else:
            self._scaled_background = None

    def create_button(self, text):
        button = QPushButton(text)
        button.setFont(QFont(self.font_family, 22))
        button.setFixedSize(320, 60)
        button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0.5);
                color: white;
                border: 2px solid #ff6b6b;
                border-radius: 30px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 107, 107, 0.3);
                border: 2px solid #ff6b6b;
                color: #ff6b6b;
            }
            QPushButton:pressed {
                background-color: rgba(255, 107, 107, 0.5);
                border: 2px solid #ff6b6b;
                color: white;
            }
        """)
        return button
            
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw background image in cover mode
        if self._scaled_background is not None:
            # Center the scaled pixmap
            x = (self._scaled_background.width() - self.width()) // 2
            y = (self._scaled_background.height() - self.height()) // 2
            painter.drawPixmap(0, 0, self._scaled_background, x, y, self.width(), self.height())
        else:
            print("Warning: Background image is null")
        
        # Draw semi-transparent overlay
        overlay = QColor(0, 0, 0, 180)
        painter.fillRect(self.rect(), overlay)
        
        # Draw "PAUSED" text with custom font
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont(self.font_family, 72, QFont.Bold))
        text_rect = painter.fontMetrics().boundingRect("PAUSED")
        x = (self.width() - text_rect.width()) // 2
        y = 150
        painter.drawText(x, y, "PAUSED")
            
    def resume_action(self):
        if isinstance(self.parent(), QWidget):
            self.parent().resume_game()
            
    def restart_action(self):
        if isinstance(self.parent(), QWidget):
            self.parent().restart_game()
            
    def menu_action(self):
        game_widget = self.parent()
        if isinstance(game_widget, QWidget):
            # Reset game state
            game_widget.is_paused = False
            game_widget.stop_game()
            game_widget.score = 0
            game_widget.blocks.clear()
            game_widget.player.reset()
            self.hide()
            
            # Switch to main menu
            main_window = game_widget.window()
            if hasattr(main_window, 'stacked_widget') and hasattr(main_window, 'main_menu'):
                main_window.stacked_widget.setCurrentWidget(main_window.main_menu) 