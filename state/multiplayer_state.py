import pygame
import math

from pygame.mixer import Sound

import resources
from constants import *
from core.game_math import Vector2
from entity.ball import Ball
from game_state import GameState

from player import Player
from entity.pad import Pad

from entity.virtual_entity import VirtualEntity

from entity.powerups.powerup import PowerUp

from random import randint


class MultiPlayerState(GameState):
    def __init__(self, game):
        super(MultiPlayerState, self).__init__(game)
        self.player1 = Player(game.input, PLAYER1, Pad(Vector2(GAME_WIDTH - PAD_DISTANCE - PAD_WIDTH, GAME_HEIGHT/2 - PAD_HEIGHT/2), dash_direction=PLAYER1_DASH), MULTIPLAYER_LIVES)
        self.player2 = Player(game.input, PLAYER2, Pad(Vector2(0 + PAD_DISTANCE, GAME_HEIGHT/2 - PAD_HEIGHT/2), dash_direction=PLAYER2_DASH), MULTIPLAYER_LIVES)
        self.balls = [Ball()]
        self.powerups = []
        self.time_since_powerup_check = 0
        self.winner = None

        # Text rendering
        self.font = None
        self.font_renderer = None

        # Player 1 Text
        self.player1_lives_label_surface = None
        self.player1_lives_surface = None
        self.player1_charge_label_surface = None
        self.player1_charge_surface = None

        # Player 2 Text
        self.player2_lives_label_surface = None
        self.player2_lives_surface = None
        self.player2_charge_label_surface = None
        self.player2_charge_surface = None

        # Sounds
        self.wall_hit_sound = None
        self.pad_hit_sound = None
        self.powerup_sound = None

    def show(self):
        # Start the music
        pygame.mixer.music.load(resources.get_music('mortalkombat.ogg'))
        pygame.mixer.music.play(-1)

        self.font = resources.get_font('prstartcustom.otf')
        self.font_renderer = pygame.font.Font(self.font, 12)

        # Player 1 Text
        self.player1_lives_label_surface = self.font_renderer.render('Lives: ', True, NOT_SO_BLACK)
        self.player1_lives_surface = self.font_renderer.render(str(self.player1.lives), True, NOT_SO_BLACK)
        self.player1_charge_label_surface = self.font_renderer.render('Charge: ', True, NOT_SO_BLACK)
        self.player1_charge_surface = self.font_renderer.render(str(self.player1.pad.charge), True, NOT_SO_BLACK)

        # Player 2 Text
        self.player2_lives_label_surface = self.font_renderer.render('Lives: ', True, NOT_SO_BLACK)
        self.player2_lives_surface = self.font_renderer.render(str(self.player2.lives), True, NOT_SO_BLACK)
        self.player2_charge_label_surface = self.font_renderer.render('Charge: ', True, NOT_SO_BLACK)
        self.player2_charge_surface = self.font_renderer.render(str(self.player2.pad.charge), True, NOT_SO_BLACK)

        # Initialize the sounds
        self.wall_hit_sound = Sound(resources.get_sound('on_wall_hit.wav'))
        self.pad_hit_sound = Sound(resources.get_sound('on_pad_hit.wav'))
        self.powerup_sound = Sound(resources.get_sound('powerup.wav'))

    def add_listeners(self):
        super(MultiPlayerState, self).add_listeners()
        self.player1.add_listeners()
        self.player2.add_listeners()

    def update(self, delta):
        # Check pads
        self.player1.update(delta)
        self.check_upper_bottom_boundaries(self.player1.pad)
        self.player2.update(delta)
        self.check_upper_bottom_boundaries(self.player2.pad)

        # Increment counter
        self.time_since_powerup_check += delta

        if self.time_since_powerup_check > POWERUP_TIMER:
            if len(self.powerups) < POWERUP_MAX and randint(0, POWERUP_PROBABILITY) == 0:
                self.powerups += [PowerUp.get_random_powerup((randint(GAME_WIDTH * 0.3, GAME_WIDTH * 0.7), randint(POWERUP_SIZE, GAME_HEIGHT - POWERUP_SIZE)))]
            self.time_since_powerup_check = 0

        # Check balls
        for b in self.balls:
            b.update(delta)

            # Check each ball
            if self.check_upper_bottom_boundaries(b):
                self.on_wall_hit()

            # Check each pad
            for p in (self.player1, self.player2):
                if self.check_entity_collision(delta, p.pad, b):
                    self.on_pad_hit()
                    self.calculate_collision(p.pad, b)
                    if b.velocity.x < BALL_SPEED_LIMIT:
                        b.velocity.x *= BALL_SPEED_MULTIPLIER
                    else:
                        b.velocity.x /= BALL_SPEED_MULTIPLIER

                    # Transfer a portion of the speed to the ball
                    b.velocity.y += BALL_SPEED_TRANSFER * p.pad.velocity.y
                    b.velocity.x += BALL_SPEED_TRANSFER_DASH * p.pad.velocity.x

                    # Add dash charge to the pad
                    if p.pad.charge < PAD_MAX_CHARGE:
                        p.pad.charge += p.pad.charging_rate

                    if b.stunning and randint(0, 4) == 0:
                        b.stunning = False
                        p.pad.stunned = True
                        p.pad.stunned_timer = POWERUP_STUN_DURATION

                    b.owner = p

                    break

            # Check each powerup
            if b.owner != None:
                for p in self.powerups:
                    if self.check_entity_collision(delta, p, b):
                        self.on_powerup()
                        p.apply(self, b)
                        self.powerups.remove(p)

                        break

            # Check scoring
            if self.check_left_boundary(b, self.player1, self.player2) or \
            self.check_right_boundary(b, self.player1, self.player2):
                with self.game.rendering:
                    self.balls.remove(b)
                    if not self.balls:
                        self.balls += [Ball()]

                    break

    def check_upper_bottom_boundaries(self, entity):
        # Check top boundary
        if entity.position.y < 0:
            entity.position.y *= -1
            entity.velocity.y *= -1
            return True

        # Check bottom boundary
        elif entity.position.y + entity.height > GAME_HEIGHT:
            entity.position.y -= (entity.position.y + entity.height - GAME_HEIGHT)*2
            entity.velocity.y *= -1
            return True

        return False

    def check_right_boundary(self, ball, player1, player2):
        if ball.position.x + ball.width >= GAME_WIDTH:
            player1.lives -= ball.damage
            print "Player 1 lost a life"
            if player1.lives <= 0:
                self.winner = player2
                print "Player 2 won"
            return True
        return False

    def check_left_boundary(self, ball, player1, player2):
        if ball.position.x <= 0:
            player2.lives -= ball.damage
            print "Player 2 lost a life"
            if player2.lives <= 0:
                self.winner = player1
                print "Player 1 won"
            return True
        return False

    def check_entity_collision(self, delta, static, moving):
        # Maybe a collision should've happened but wasn't detected
        i = 0
        collision = False
        virtualmoving = VirtualEntity(moving.position-delta*moving.velocity, width=moving.width, height=moving.height, velocity=moving.velocity)
        virtualstatic = VirtualEntity(static.position-delta*static.velocity, width=static.width, height=static.height, velocity=static.velocity)
        while not(collision) and i < COLLISION_INTERPOLATION:
            virtualmoving.update(delta/COLLISION_INTERPOLATION)
            virtualstatic.update(delta/COLLISION_INTERPOLATION)
            collision = virtualmoving.get_bounds().colliderect(virtualstatic.get_bounds())
            i += 1

        # We were right!
        if collision:
            # Copy the virtual ball's variables
            moving.position = virtualmoving.position
            moving.velocity = virtualmoving.velocity
            moving.update_bounds()

        return collision

    def calculate_collision(self, entity, point):
        entity_angle = math.atan2(entity.height/2, entity.width/2)
        collision_angle = math.atan2(entity.bounds.centery - point.bounds.centery, point.bounds.centerx - entity.bounds.centerx) + entity_angle

        if collision_angle < 0:
            collision_angle += 2*math.pi

        if collision_angle < 2*entity_angle or (point.velocity.x < 0 and collision_angle < math.pi+2*entity_angle):
            point.position.x = entity.position.x + entity.width
            point.velocity.x *= -1
        elif collision_angle < math.pi:
            point.position.y = entity.position.y - point.height
            point.velocity.y *= -1
        elif collision_angle < math.pi+2*entity_angle or (point.velocity.x > 0 and collision_angle < 2*entity_angle):
            point.position.x = entity.position.x - point.width
            point.velocity.x *= -1
        elif collision_angle < 2*math.pi:
            point.position.y = entity.position.y + entity.height
            point.velocity.y *= -1

    def render(self, canvas):
        canvas.fill(NOT_SO_WHITE)
        self.player1.render(canvas)
        self.player2.render(canvas)

        for b in self.balls:
            b.render(canvas)

        for p in self.powerups:
            p.render(canvas)

        # Render player 1 Text
        self.player1_lives_surface = self.font_renderer.render(str(self.player1.lives), True, NOT_SO_BLACK)
        self.player1_charge_surface = self.font_renderer.render(str(100*self.player1.pad.charge/PAD_MAX_CHARGE) + '%', True, NOT_SO_BLACK)
        canvas.blit(self.player1_lives_label_surface, (GAME_WIDTH - 20 - self.player1_lives_surface.get_width() - self.player1_lives_label_surface.get_width(), 15))
        canvas.blit(self.player1_lives_surface, (GAME_WIDTH - 20 - self.player1_lives_surface.get_width(), 15))
        canvas.blit(self.player1_charge_label_surface, (GAME_WIDTH - 20 - self.player1_charge_surface.get_width() - self.player1_charge_label_surface.get_width(), 35))
        canvas.blit(self.player1_charge_surface, (GAME_WIDTH - 20 - self.player1_charge_surface.get_width(), 35))

        # Render player 2 Text
        self.player2_lives_surface = self.font_renderer.render(str(self.player2.lives), True, NOT_SO_BLACK)
        self.player2_charge_surface = self.font_renderer.render(str(100*self.player2.pad.charge/PAD_MAX_CHARGE) + '%', True, NOT_SO_BLACK)
        canvas.blit(self.player2_lives_label_surface, (20, 15))
        canvas.blit(self.player2_lives_surface, (20 + self.player2_lives_label_surface.get_width(), 15))
        canvas.blit(self.player2_charge_label_surface, (20, 35))
        canvas.blit(self.player2_charge_surface, (20 + self.player2_charge_label_surface.get_width(), 35))

    def on_wall_hit(self):
        self.wall_hit_sound.play()

    def on_pad_hit(self):
        self.pad_hit_sound.play()

    def on_powerup(self):
        self.powerup_sound.play()

    def remove_listeners(self):
        super(MultiPlayerState, self).remove_listeners()
        self.player1.remove_listeners()
        self.player2.remove_listeners()

    def dispose(self):
        pygame.mixer.music.stop()
