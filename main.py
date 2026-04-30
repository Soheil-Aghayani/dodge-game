import sys
import os
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget, QMessageBox
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap, QFontDatabase
from module.player import Player
from module.block import Block
from module.floor import Floor
from module.death_screen import DeathScreen
from module.background import Background
from module.sound_manager import SoundManager
from module.main_menu import MainMenu
from module.abnormal import AbnormalManager
from module.pause import PauseScreen
from module.health_system import HealthSystem
from module.settings_menu import SettingsMenu

class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dodge the Falling Blocks")
        self.setFixedSize(800, 600)
        
        # Create stacked widget to manage screens
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Create game widget and menu
        self.game_widget = GameWidget(self)
        self.sound_manager = SoundManager()
        self.main_menu = MainMenu(self, self.sound_manager)
        self.settings_menu = SettingsMenu(self, self.sound_manager)
        
        # Add widgets to stack
        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.game_widget)
        self.stacked_widget.addWidget(self.settings_menu)
        
        # Show main menu initially
        self.stacked_widget.setCurrentWidget(self.main_menu)
        
    def start_game(self):
        self.stacked_widget.setCurrentWidget(self.game_widget)
        self.game_widget.start_game()
        
    def show_main_menu(self):
        self.stacked_widget.setCurrentWidget(self.main_menu)
        self.game_widget.stop_game()

    def show_settings(self):
        self.stacked_widget.setCurrentWidget(self.settings_menu)

class GameWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setFocusPolicy(Qt.StrongFocus)
        
        # Game state
        self.game_active = False
        self.score = 0
        self.last_update = QTime.currentTime().msecsSinceStartOfDay()
        self.waiting_for_restart = False
        self.death_animation_timer = None
        self.show_death_screen = False
        self.high_score = self.load_high_score()
        self.shake_timer = 0
        self.shake_offset = (0, 0)
        self.is_paused = False
        
        # Initialize sound manager
        self.sound_manager = SoundManager()
        
        # Initialize background
        self.background = Background(self)
        
        # Initialize floor
        self.floor = Floor(self)
        
        # Initialize player
        self.player = Player(self)
        
        # Initialize blocks
        self.blocks = []
        self.block_spawn_timer = QTimer(self)
        self.block_spawn_timer.timeout.connect(self.spawn_block)
        
        # Setup game timer
        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.update_game)
        
        # Track pressed keys
        self.pressed_keys = set()
        self.last_footstep_time = 0
        self.last_movement_time = QTime.currentTime().msecsSinceStartOfDay()
        self.movement_delay = 8  # Reduced delay for more responsive movement (~125 FPS)
        
        # Load custom font for Game Over
        current_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(current_dir, "module", "asset", "font", "KarenFat.ttf")
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

        # Cache QFonts to avoid expensive instantiations in paintEvent
        self.cached_font_20 = QFont(self.font_family, 20)
        self.cached_font_48 = QFont(self.font_family, 48)
        self.cached_font_32 = QFont(self.font_family, 32)
        self.cached_font_22 = QFont(self.font_family, 22)
        self.cached_font_28_bold = QFont(self.font_family, 28, QFont.Bold)

        # Cache QColors
        self.cached_color_white = QColor(255, 255, 255)
        self.cached_color_overlay = QColor(0, 0, 0, 180)
        self.cached_color_warning = QColor(255, 200, 0)

        # Pre-calculate static text bounding rects using temporary QFontMetrics
        from PyQt5.QtGui import QFontMetrics
        metrics_48 = QFontMetrics(self.cached_font_48)
        self.cached_rect_game_over = metrics_48.boundingRect("Game Over!")
        
        metrics_22 = QFontMetrics(self.cached_font_22)
        self.cached_rect_restart = metrics_22.boundingRect("Press R to restart")

        metrics_28_bold = QFontMetrics(self.cached_font_28_bold)
        self.cached_warning_rects = {
            'reverse floor': metrics_28_bold.boundingRect('reverse floor'),
            'reverse control': metrics_28_bold.boundingRect('reverse control'),
            'random blocks': metrics_28_bold.boundingRect('random blocks')
        }

        # ⚡ BOLT OPTIMIZATION: Cache dynamically calculated text bounding rects
        # and warning map to prevent recreating them on every render frame
        self.cached_dynamic_text_rects = {}
        self.warning_texts = {
            'reverse_floor': 'reverse floor',
            'reverse_control': 'reverse control',
            'random_blocks': 'random blocks'
        }

        self.abnormal_manager = AbnormalManager()
        self.glitch_timer = 0
        self.pending_abnormal_type = None
        
        # Initialize pause screen
        self.pause_screen = PauseScreen(self)
        self.pause_screen.hide()
        
        # Initialize health system
        self.health_system = HealthSystem(self)
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.background.resize(self.width(), self.height())
        self.player.reset_position()
        
    def stop_game(self):
        self.game_active = False
        self.block_spawn_timer.stop()
        self.game_timer.stop()
        
    def start_game(self):
        self.game_active = True
        self.waiting_for_restart = False
        self.show_death_screen = False
        self.score = 0
        self.player.reset()
        self.blocks.clear()
        self.health_system.reset()  # Reset health when starting new game
        self.game_timer.start(16)  # ~60 FPS
        self.block_spawn_timer.start(1000)  # Spawn a block every second
        self.is_paused = False
        self.setFocus()
        
    def spawn_block(self):
        if self.game_active:
            self.blocks.append(Block(self))
            
    def update_game(self):
        current_time = QTime.currentTime().msecsSinceStartOfDay()
        
        # Always update player animation, even when game is not active
        self.player.update(current_time)
        
        # Update abnormal state
        prev_active = self.abnormal_manager.is_active()
        prev_type = self.abnormal_manager.get_type()
        self.abnormal_manager.update(self.score)
        now_active = self.abnormal_manager.is_active()
        now_type = self.abnormal_manager.get_type()
        # If about to activate abnormal, start glitch
        if not prev_active and now_active and self.glitch_timer == 0:
            self.glitch_timer = 10  # ~0.5s at 50ms per frame
            self.pending_abnormal_type = now_type
            self.abnormal_manager.deactivate_manual()  # Temporarily deactivate
        # If glitch just finished, activate abnormal
        if self.glitch_timer == 1 and self.pending_abnormal_type:
            self.abnormal_manager.activate_manual(self.pending_abnormal_type)
            self.pending_abnormal_type = None
        if self.glitch_timer > 0:
            self.glitch_timer -= 1
        
        if not self.game_active:
            self.update()  # Keep updating display for death animation
            return
            
        # Update player position based on pressed keys with consistent timing
        if current_time - self.last_movement_time >= self.movement_delay:
            if Qt.Key_Left in self.pressed_keys:
                self.player.move_left()
                # Play footstep sound with more natural delay
                if current_time - self.last_footstep_time > 120:
                    self.sound_manager.play_footstep()
                    self.last_footstep_time = current_time
                    
            if Qt.Key_Right in self.pressed_keys:
                self.player.move_right()
                # Play footstep sound with more natural delay
                if current_time - self.last_footstep_time > 120:
                    self.sound_manager.play_footstep()
                    self.last_footstep_time = current_time
            self.last_movement_time = current_time
            
        # Update blocks
        for block in self.blocks[:]:
            if block.update():  # Block reached bottom
                self.blocks.remove(block)
                self.score += 1
            elif block.check_collision(self.player.get_rect()):
                if self.health_system.take_damage():  # Only process collision if damage was dealt
                    self.sound_manager.play_collision()
                    if self.health_system.is_game_over():
                        self.player.die()
                        self.game_over()
                        return
                
        self.update()  # Trigger paintEvent
            
    def game_over(self):
        if self.waiting_for_restart:
            return
        self.game_active = False
        self.waiting_for_restart = True
        self.block_spawn_timer.stop()
        # High score logic
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
        # Shake effect
        self.shake_timer = 10  # 10 frames of shake
        self.abnormal_manager.deactivate_manual()  # Deactivate abnormal on death
        self.death_animation_timer = QTimer(self)
        self.death_animation_timer.timeout.connect(self._check_death_animation)
        self.death_animation_timer.start(50)
        
    def _check_death_animation(self):
        if self.shake_timer > 0:
            self.shake_timer -= 1
            self.shake_offset = (random.randint(-10, 10), random.randint(-10, 10))
        else:
            self.shake_offset = (0, 0)
        if self.player.die_animation.is_finished:
            self.death_animation_timer.stop()
            self.game_timer.stop()
            self.show_death_screen = True
            self.sound_manager.play_game_over()
            self.update()
        else:
            self.update()
            
    def _handle_game_over_response(self):
        self.waiting_for_restart = False
        self.show_death_screen = False
        self.start_game()
        
    def get_floor_height(self):
        return self.floor.get_height()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Glitch effect
        if self.glitch_timer > 0:
            for _ in range(20):
                x = random.randint(0, self.width())
                y = random.randint(0, self.height())
                w = random.randint(10, 80)
                h = random.randint(5, 30)
                color = QColor(random.randint(180,255), random.randint(0,80), random.randint(0,80), 180)
                painter.fillRect(x, y, w, h, color)
            painter.translate(random.randint(-20, 20), random.randint(-20, 20))
        else:
            # Flip the whole game if reverse_floor is active
            reverse_floor = self.abnormal_manager.is_active() and self.abnormal_manager.get_type() == 'reverse_floor'
            if reverse_floor:
                painter.scale(1, -1)
                painter.translate(0, -self.height())
            if self.shake_offset != (0, 0):
                painter.translate(*self.shake_offset)
        
        # Draw background first
        self.background.draw(painter)
        
        # Draw floor
        self.floor.draw(painter)
        
        # Draw player
        self.player.draw(painter)
        
        # Draw blocks
        for block in self.blocks:
            block.draw(painter)
            
        # Draw score
        painter.setPen(self.cached_color_white)
        painter.setFont(self.cached_font_20)
        painter.drawText(10, 30, f"Score: {self.score}")
        
        # Draw health after score
        self.health_system.draw(painter)
        
        # Draw death screen overlay
        if self.show_death_screen:
            # Semi-transparent black overlay
            painter.fillRect(self.rect(), self.cached_color_overlay)
            
            # Draw Game Over text with KarenFat font
            painter.setPen(self.cached_color_white)
            painter.setFont(self.cached_font_48)
            x = (self.width() - self.cached_rect_game_over.width()) // 2
            y = (self.height() - self.cached_rect_game_over.height()) // 2 - 40
            painter.drawText(x, y, "Game Over!")
            
            # Draw Score with KarenFat font
            painter.setFont(self.cached_font_32)
            score_text = f"Score: {self.score}"
            if score_text not in self.cached_dynamic_text_rects:
                self.cached_dynamic_text_rects[score_text] = painter.fontMetrics().boundingRect(score_text)
            text_rect = self.cached_dynamic_text_rects[score_text]
            x = (self.width() - text_rect.width()) // 2
            y += text_rect.height() + 20
            painter.drawText(x, y, score_text)
            
            # Draw restart instruction with KarenFat font
            painter.setFont(self.cached_font_22)
            restart_text = "Press R to restart"
            text_rect = self.cached_rect_restart
            x = (self.width() - text_rect.width()) // 2
            y += text_rect.height() + 30
            painter.drawText(x, y, restart_text)
            
            # Draw High Score
            painter.setFont(self.cached_font_22)
            hs_text = f"High Score: {self.high_score}"
            if hs_text not in self.cached_dynamic_text_rects:
                self.cached_dynamic_text_rects[hs_text] = painter.fontMetrics().boundingRect(hs_text)
            text_rect = self.cached_dynamic_text_rects[hs_text]
            x = (self.width() - text_rect.width()) // 2
            y += text_rect.height() + 20
            painter.drawText(x, y, hs_text)
        
        # Draw abnormal warning if active
        if self.abnormal_manager.is_active():
            abnormal_type = self.abnormal_manager.get_type()
            warning_text = self.warning_texts.get(abnormal_type, 'abnormal state')
            painter.setPen(self.cached_color_warning)
            painter.setFont(self.cached_font_28_bold)
            if warning_text not in self.cached_warning_rects:
                self.cached_warning_rects[warning_text] = painter.fontMetrics().boundingRect(warning_text)
            text_rect = self.cached_warning_rects[warning_text]
            x = (self.width() - text_rect.width()) // 2
            y = 60
            painter.drawText(x, y, warning_text)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            if not self.show_death_screen:
                self.toggle_pause()
        elif not self.is_paused and not self.show_death_screen:
            # Check if reverse control is active
            reverse = self.abnormal_manager.is_active() and self.abnormal_manager.get_type() == 'reverse_control'
            
            if event.key() == Qt.Key_Left:
                if reverse:
                    self.player.move_right()
                else:
                    self.player.move_left()
                self.pressed_keys.add(event.key())
            elif event.key() == Qt.Key_Right:
                if reverse:
                    self.player.move_left()
                else:
                    self.player.move_right()
                self.pressed_keys.add(event.key())
            elif event.key() == Qt.Key_Space:
                self.player.jump()
        elif self.show_death_screen and event.key() == Qt.Key_R:
            self.restart_game()
        # Manual abnormal test keys
        if event.key() == Qt.Key_F1:
            self.abnormal_manager.activate_manual('reverse_floor')
            self.update()
            return
        if event.key() == Qt.Key_F2:
            self.abnormal_manager.activate_manual('reverse_control')
            self.player.stop_movement()
            self.pressed_keys.clear()
            self.update()
            return
        if event.key() == Qt.Key_F3:
            self.abnormal_manager.activate_manual('random_blocks')
            self.update()
            return
        if event.key() == Qt.Key_F4:
            self.abnormal_manager.deactivate_manual()
            self.player.stop_movement()
            self.pressed_keys.clear()
            self.update()
            return
            
        if not self.game_active:
            if event.key() == Qt.Key_R and self.show_death_screen:
                self.parent.show_main_menu()
            return
            
        # Only add the key to pressed_keys if it's not a movement key
        if event.key() not in [Qt.Key_Left, Qt.Key_Right]:
            self.pressed_keys.add(event.key())
        
    def keyReleaseEvent(self, event):
        # Check if reverse control is active
        reverse = self.abnormal_manager.is_active() and self.abnormal_manager.get_type() == 'reverse_control'
        
        if event.key() == Qt.Key_Left:
            if reverse:
                self.player.stop_movement()
            else:
                self.player.stop_movement()
        elif event.key() == Qt.Key_Right:
            if reverse:
                self.player.stop_movement()
            else:
                self.player.stop_movement()
                
        self.pressed_keys.discard(event.key())
        
        # If no movement keys are pressed, stop movement
        if not any(key in self.pressed_keys for key in [Qt.Key_Left, Qt.Key_Right]):
            self.player.stop_movement()

    def load_high_score(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            highscore_path = os.path.join(current_dir, "highscore.txt")
            with open(highscore_path, "r") as f:
                return int(f.read().strip())
        except Exception:
            return 0

    def save_high_score(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            highscore_path = os.path.join(current_dir, "highscore.txt")
            with open(highscore_path, "w") as f:
                f.write(str(self.high_score))
        except Exception:
            pass

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            # Stop all game timers and elements
            self.game_timer.stop()
            self.block_spawn_timer.stop()
            self.pause_screen.show()
            self.pause_screen.setFocus()
        else:
            # Resume all game timers and elements
            self.game_timer.start(16)  # ~60 FPS
            self.block_spawn_timer.start(1000)  # Spawn a block every second
            self.pause_screen.hide()
            self.setFocus()
            
    def resume_game(self):
        self.is_paused = False
        # Resume all game timers and elements
        self.game_timer.start(16)  # ~60 FPS
        self.block_spawn_timer.start(1000)  # Spawn a block every second
        self.pause_screen.hide()
        self.setFocus()
        
    def restart_game(self):
        self.score = 0
        self.show_death_screen = False
        self.is_paused = False
        self.waiting_for_restart = False
        self.game_active = True
        self.player.reset()
        self.blocks.clear()
        self.pause_screen.hide()
        self.health_system.reset()  # Reset health system
        # Restart game timers
        self.game_timer.start(16)  # ~60 FPS
        self.block_spawn_timer.start(1000)  # Spawn a block every second
        self.setFocus()
        
    def return_to_menu(self):
        self.parent().show_main_menu()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec_()) 