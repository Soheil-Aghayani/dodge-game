from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QTimer
import os
import random
import json

class SoundEffect:
    def __init__(self, file_path, volume=50):
        self.player = QMediaPlayer()
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
        self.player.setVolume(volume)
    
    def play(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.stop()
        self.player.setPosition(0)
        self.player.play()

class SoundManager:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.sound_dir = os.path.join(current_dir, "asset", "sound_effect")
        self.music_dir = os.path.join(current_dir, "asset", "music")
        
        # Load saved settings
        self.settings_file = os.path.join(current_dir, "settings.json")
        self.load_settings()
        
        # Create and configure sound effects
        self.sound_effects = {
            'footstep': SoundEffect(os.path.join(self.sound_dir, "footstep_sound.mp3"), self.effects_volume),
            'collision': SoundEffect(os.path.join(self.sound_dir, "collision.mp3"), self.effects_volume),
            'cursor': SoundEffect(os.path.join(self.sound_dir, "Cursor.mp3"), self.effects_volume),
            'explosion': SoundEffect(os.path.join(self.sound_dir, "explosion.mp3"), self.effects_volume)
        }
        
        # Game over needs special handling
        self.game_over_player = QMediaPlayer()
        game_over_path = os.path.join(self.sound_dir, "game_over.mp3")
        self.game_over_player.setMedia(QMediaContent(QUrl.fromLocalFile(game_over_path)))
        self.game_over_player.setVolume(self.effects_volume)
        
        # Background music
        self.music_files = [
            os.path.join(self.music_dir, "Before the Dawn.mp3"),
            os.path.join(self.music_dir, "Hopeful Feeling.mp3"),
            os.path.join(self.music_dir, "Shelf Space.mp3"),
            os.path.join(self.music_dir, "Gone Fishing.mp3"),
            os.path.join(self.music_dir, "Fire in the Hole.mp3"),
            os.path.join(self.music_dir, "No Tomorrow.mp3"),
            os.path.join(self.music_dir, "Against All Odds.mp3"),
            os.path.join(self.music_dir, "The Extraordinary.mp3"),
            os.path.join(self.music_dir, "Singularity.mp3"),
            os.path.join(self.music_dir, "End of Monolith (Unused).mp3")
        ]
        self.music_player = QMediaPlayer()
        self.music_player.setVolume(self.music_volume)
        self.music_player.mediaStatusChanged.connect(self._on_music_status)
        self.music_paused_for_gameover = False
        self.music_timer = QTimer()
        self.music_timer.setSingleShot(True)
        self.music_timer.timeout.connect(self._play_random_music)
        self.current_music_path = None
        if self.sound_enabled:
            self._play_random_music()
        
        # Connect game over sound to resume music after finish
        self.game_over_player.mediaStatusChanged.connect(self._on_gameover_status)

    def load_settings(self):
        """Load sound settings from file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    self.sound_enabled = settings.get('sound_enabled', True)
                    self.music_volume = settings.get('music_volume', 40)
                    self.effects_volume = settings.get('effects_volume', 70)
            else:
                self.sound_enabled = True
                self.music_volume = 40
                self.effects_volume = 70
        except Exception:
            self.sound_enabled = True
            self.music_volume = 40
            self.effects_volume = 70

    def save_settings(self):
        """Save sound settings to file"""
        settings = {
            'sound_enabled': self.sound_enabled,
            'music_volume': self.music_volume,
            'effects_volume': self.effects_volume
        }
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f)
        except Exception:
            pass

    def set_music_volume(self, volume):
        """Set music volume (0-100)"""
        self.music_volume = max(0, min(100, volume))
        self.music_player.setVolume(self.music_volume)
        self.save_settings()

    def set_effects_volume(self, volume):
        """Set sound effects volume (0-100)"""
        self.effects_volume = max(0, min(100, volume))
        for effect in self.sound_effects.values():
            effect.player.setVolume(self.effects_volume)
        self.game_over_player.setVolume(self.effects_volume)
        self.save_settings()

    def toggle_sound(self, enabled):
        """Toggle all sound on/off"""
        self.sound_enabled = enabled
        if enabled:
            self.start_music()
        else:
            self.stop_music()
        self.save_settings()

    def _on_music_status(self, status):
        # When a track finishes, wait 2 seconds before playing the next one
        if status == QMediaPlayer.EndOfMedia:
            self.music_timer.start(2000)  # 2 second delay between tracks
    
    def _on_gameover_status(self, status):
        # Resume music after game over sound finished
        if status == QMediaPlayer.EndOfMedia and self.music_paused_for_gameover:
            self.music_paused_for_gameover = False
            self.music_timer.start(2000)  # Wait 2 seconds before resuming music
    
    def _play_random_music(self):
        # Stop any currently playing music
        if self.music_player.state() == QMediaPlayer.PlayingState:
            self.music_player.stop()
            
        # Select and play a new random track
        music_path = random.choice(self.music_files)
        while music_path == self.current_music_path and len(self.music_files) > 1:
            music_path = random.choice(self.music_files)  # Avoid playing same track twice in a row
            
        self.current_music_path = music_path
        self.music_player.setMedia(QMediaContent(QUrl.fromLocalFile(music_path)))
        self.music_player.play()
        
    def play_sound(self, sound_name):
        if sound_name == 'game_over':
            if self.music_player.state() == QMediaPlayer.PlayingState:
                self.music_player.pause()
                self.music_paused_for_gameover = True
            self.game_over_player.play()
        elif sound_name in self.sound_effects:
            self.sound_effects[sound_name].play()
        
    def play_footstep(self):
        self.sound_effects['footstep'].play()
        
    def play_collision(self):
        self.sound_effects['collision'].play()
        
    def play_game_over(self):
        if self.music_player.state() == QMediaPlayer.PlayingState:
            self.music_player.pause()
            self.music_paused_for_gameover = True
        self.game_over_player.play()
        
    def play_cursor(self):
        self.sound_effects['cursor'].play()
        
    def play_explosion(self):
        self.sound_effects['explosion'].play()
        
    def start_music(self):
        if self.music_player.state() != QMediaPlayer.PlayingState:
            self._play_random_music()
        
    def stop_music(self):
        if self.music_player.state() == QMediaPlayer.PlayingState:
            self.music_player.stop()
            self.current_music_path = None 