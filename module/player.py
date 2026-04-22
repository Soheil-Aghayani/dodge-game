from PyQt5.QtCore import QRect, QTime
from PyQt5.QtGui import QPainter, QTransform, QColor
from module.idle_player import IdlePlayer
from module.moving_player import MovingPlayer
from module.die_player import DiePlayer
from module.shield import Shield
from module.jump import JumpPlayer

class Player:
    def __init__(self, game_widget):
        self.game_widget = game_widget
        # Set dimensions with correct ratio (27:16)
        self.width = 48  # Base width (multiple of 16)
        self.height = 81  # Corresponding height (multiple of 27)
        self.speed = 6  # Increased speed for faster movement
        self.x = 0
        self.y = 0
        
        # Initialize animations
        self.idle_animation = IdlePlayer()
        self.moving_animation = MovingPlayer()
        self.die_animation = DiePlayer()
        self.jump_animation = JumpPlayer()
        self.current_animation = self.idle_animation
        
        # Initialize shield
        self.shield = Shield(self)
        
        # Movement state
        self.is_moving = False
        self.is_dead = False
        self.facing_right = True  # For flipping the sprite
        self.movement_direction = 0  # -1 for left, 0 for none, 1 for right
        self.last_movement_time = QTime.currentTime().msecsSinceStartOfDay()
        self.movement_delay = 2  # Reduced delay for more responsive movement (~500 FPS)
        
        self.last_update = QTime.currentTime().msecsSinceStartOfDay()
        
    def reset_position(self):
        if self.game_widget.height() > 0:
            self.x = (self.game_widget.width() - self.width) // 2
            self.y = self.game_widget.floor.get_y_position() - self.height
            self.is_dead = False
            self.current_animation = self.idle_animation
            self.movement_direction = 0
            self.jump_animation.is_jumping = False
            self.jump_animation.current_y_offset = 0
        
    def move_left(self):
        if self.is_dead:
            return
        self.movement_direction = -1
        self.is_moving = True
        self.facing_right = False
        
    def move_right(self):
        if self.is_dead:
            return
        self.movement_direction = 1
        self.is_moving = True
        self.facing_right = True
        
    def stop_movement(self):
        self.movement_direction = 0
        self.is_moving = False
        
    def jump(self):
        if not self.is_dead and not self.jump_animation.is_jumping:
            self.jump_animation.start_jump(self.y)
            self.current_animation = self.jump_animation
        
    def update(self, current_time):
        delta_time = current_time - self.last_update
        if delta_time < 0:  # Handle day rollover
            delta_time += 24 * 60 * 60 * 1000  # Add 24 hours in milliseconds
        self.last_update = current_time
        
        # Update jump state
        if self.jump_animation.is_jumping:
            if self.jump_animation.update(delta_time):  # Jump complete
                self.current_animation = self.idle_animation
                self.jump_animation.is_jumping = False
            self.y = self.game_widget.floor.get_y_position() - self.height + self.jump_animation.get_y_offset()
        
        # Update position based on movement direction with consistent timing
        # Allow movement during jumps
        if self.movement_direction != 0 and current_time - self.last_movement_time >= self.movement_delay:
            new_x = self.x + (self.movement_direction * self.speed)
            if self.movement_direction < 0:  # Moving left
                self.x = max(0, new_x)
                self.facing_right = False
            else:  # Moving right
                self.x = min(self.game_widget.width() - self.width, new_x)
                self.facing_right = True
            self.last_movement_time = current_time
            self.is_moving = True  # Set moving state when actually moving
        else:
            self.is_moving = False  # Reset moving state when not moving
        
        # Update animation state with smoother transitions
        if self.is_dead:
            if not self.die_animation.is_finished:
                self.current_animation = self.die_animation
                self.current_animation.update(delta_time)
        elif self.jump_animation.is_jumping:
            self.current_animation = self.jump_animation
            self.current_animation.update(delta_time)
        else:
            if self.is_moving:
                self.current_animation = self.moving_animation
            else:
                self.current_animation = self.idle_animation
            self.current_animation.update(delta_time)
            
    def draw(self, painter):
        if self.current_animation:
            frame = self.current_animation.get_current_frame(self.facing_right)
            if frame:
                # Draw shield first if invincible (so it appears behind the player)
                if hasattr(self.game_widget, 'health_system') and \
                   self.game_widget.health_system.is_invincible and \
                   not self.is_dead:
                    self.shield.draw(painter)
                
                # Save the current painter state
                painter.save()
                
                # The frame is already flipped if needed by the Animation class
                painter.drawPixmap(int(self.x), int(self.y), frame)
                
                # Restore the painter state
                painter.restore()
                    
    def get_rect(self):
        # If invincible, use shield hitbox
        if hasattr(self.game_widget, 'health_system') and \
           self.game_widget.health_system.is_invincible:
            return self.shield.get_rect()
            
        # Otherwise use normal player hitbox
        hitbox_width = int(self.width * 0.7)
        hitbox_height = self.height
        hitbox_x = int(self.x + (self.width - hitbox_width) // 2)
        return QRect(hitbox_x, int(self.y), hitbox_width, hitbox_height)
            
    def die(self):
        if not self.is_dead:
            self.is_dead = True
            self.current_animation = self.die_animation
            # Make sure character is on the ground
            self.y = self.game_widget.floor.get_y_position() - self.height
            # Reset death animation state
            self.die_animation.is_finished = False
            self.die_animation.played_once = False
            self.die_animation.current_frame = 0

    def reset(self):
        """Reset player to initial state"""
        self.x = 400  # Center of screen
        self.y = self.game_widget.floor.get_y_position() - self.height
        self.velocity_y = 0
        self.is_jumping = False
        self.is_moving = False
        self.facing_right = True
        self.state = "idle"
        self.current_frame = 0
        self.animation_timer = 0
        # Reset death animation properly
        self.die_animation = DiePlayer()
        self.current_animation = self.idle_animation
        self.is_dead = False
        self.jump_animation.is_jumping = False
        self.jump_animation.current_y_offset = 0 