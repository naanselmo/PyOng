import pygame
import math

from pygame.mixer import Sound

import resources
import hiscores

from platform import node

from constants import *
from core.game_math import Vector2
from entity.ball import Ball
from game_state import GameState

from player import Player
from entity.pad import Pad

from entity.virtual_entity import VirtualEntity

from entity.powerups.powerup import PowerUp

from random import randint


class SinglePlayerState(GameState):
    def __init__(self, game):
        super(SinglePlayerState, self).__init__(game)
        self.listen_keys = (pygame.K_ESCAPE,)
        self.player = Player(game.input, PLAYER1, Pad(Vector2(0 + PAD_DISTANCE, GAME_HEIGHT/2 - PAD_HEIGHT/2)), SINGLEPLAYER_LIVES)
        self.balls = []
        self.powerups = []
        self.score_multiplier = SINGLEPLAYER_SCORE_MULTIPLIER
        self.time_since_powerup_check = 0
        self.score = 0
        self.gameover = False
        self.instructions = True

        # Text rendering
        self.font = None
        self.font_renderer = None

        # Player Text
        self.player_lives_label_surface = None
        self.player_lives_surface = None
        self.player_score_label_surface = None
        self.player_score_surface = None
        self.player_multiplier_label_surface = None
        self.player_multiplier_surface = None

        # Sounds
        self.wall_hit_sound = None
        self.pad_hit_sound = None
        self.powerup_sound = None

    def show(self):
        # Start the music
        pygame.mixer.music.load(resources.get_music('battleofheroes.ogg'))
        pygame.mixer.music.play(-1)

        self.font = resources.get_font('prstartcustom.otf')
        self.font_renderer = pygame.font.Font(self.font, 12)

        # Player Text
        self.player_lives_label_surface = self.font_renderer.render('Lives: ', True, NOT_SO_BLACK)
        self.player_lives_surface = self.font_renderer.render(str(self.player.lives), True, NOT_SO_BLACK)
        self.player_score_label_surface = self.font_renderer.render('Score: ', True, NOT_SO_BLACK)
        self.player_score_surface = self.font_renderer.render(str(self.score), True, NOT_SO_BLACK)
        self.player_multiplier_label_surface = self.font_renderer.render('Multiplier: ', True, NOT_SO_BLACK)
        self.player_multiplier_surface = self.font_renderer.render(str(self.score_multiplier), True, NOT_SO_BLACK)

        # Initialize the sounds
        self.wall_hit_sound = Sound(resources.get_sound('on_wall_hit.wav'))
        self.pad_hit_sound = Sound(resources.get_sound('on_pad_hit.wav'))
        self.powerup_sound = Sound(resources.get_sound('powerup.wav'))

    def add_listeners(self):
        super(SinglePlayerState, self).add_listeners()
        self.player.add_listeners()

    def update(self, delta):
        if self.instructions:
            pygame.time.wait(4750)
            self.instructions = False
            pygame.time.wait(250)
            self.game.logic_clock.tick()
            self.balls = [Ball()]

        # Check if paused
        if self.input.key_clicked(pygame.K_ESCAPE):
            from pause_state import PauseState
            self.state_manager.push_overlay(PauseState(self.game, SinglePlayerState(self.game)))
            return

        # Check pads
        self.player.update(delta)
        self.check_upper_bottom_right_boundaries(self.player.pad)

        # Increment counter
        self.time_since_powerup_check += delta

        if self.time_since_powerup_check > POWERUP_TIMER:
            if len(self.powerups) < POWERUP_MAX and randint(0, POWERUP_PROBABILITY/2) == 0:
                self.powerups += [PowerUp.get_random_powerup((randint(GAME_WIDTH * 0.3, GAME_WIDTH * 0.7), randint(POWERUP_SIZE, GAME_HEIGHT - POWERUP_SIZE)), False)]
            self.time_since_powerup_check = 0

        # Check balls
        for b in self.balls:
            b.update(delta)

            # Check each ball
            if self.check_upper_bottom_right_boundaries(b):
                self.on_wall_hit()

            # Check each pad
            if self.check_entity_collision(delta, self.player.pad, b):
                self.on_pad_hit()
                self.calculate_collision(self.player.pad, b)
                if b.velocity.x < BALL_SPEED_LIMIT:
                    b.velocity.x *= BALL_SPEED_MULTIPLIER
                else:
                    b.velocity.x /= BALL_SPEED_MULTIPLIER

                # Transfer a portion of the speed to the ball
                b.velocity.y += BALL_SPEED_TRANSFER * self.player.pad.velocity.y
                b.velocity.x += BALL_SPEED_TRANSFER_DASH * self.player.pad.velocity.x

                # Add score
                self.score += self.score_multiplier

                b.owner = self.player

            # Check each powerup
            if b.owner != None:
                for p in self.powerups:
                    if self.check_entity_collision(delta, p, b):
                        self.on_powerup()
                        p.apply(self, b)
                        self.powerups.remove(p)

                        break

            # Check scoring
            if self.check_left_boundary(b, self.player):
                with self.game.rendering:
                    self.balls.remove(b)
                    if not self.balls:
                        self.balls += [Ball()]

                    break


    def check_upper_bottom_right_boundaries(self, entity):
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

        # Check right boundary
        elif entity.position.x + entity.width >= GAME_WIDTH:
            entity.position.x -= (entity.position.x + entity.width - GAME_WIDTH)*2
            entity.velocity.x *= -1
            return True

        return False

    def check_left_boundary(self, ball, player):
        if ball.position.x <= 0:
            player.lives -= ball.damage
            if player.lives <= 0 and VIRGINITY:
                self.game.hiscores.add_score(node(), self.score)
                self.gameover = True
                pygame.time.wait(5000)
                from menu_state import MenuState
                self.state_manager.set_state(MenuState(self.game))
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

        if self.instructions:
            font = resources.get_font('prstartcustom.otf')
            font_renderer = pygame.font.Font(self.font, 15)
            instructions_surface = font_renderer.render("USE THE UP & DOWN ARROW KEYS", True, NOT_SO_BLACK)
            goodluck_surface = font_renderer.render("GOOD LUCK.", True, NOT_SO_BLACK)
            canvas.blit(instructions_surface, (GAME_WIDTH/2 - instructions_surface.get_width()/2, GAME_HEIGHT/2 - instructions_surface.get_height() - 10))
            canvas.blit(goodluck_surface, (GAME_WIDTH/2 - goodluck_surface.get_width()/2, GAME_HEIGHT/2 + 10))
            return

        elif self.gameover:
            font = resources.get_font('prstartcustom.otf')
            font_renderer = pygame.font.Font(self.font, 18)
            end_surface = font_renderer.render("GAME OVER. FINAL SCORE: " + str(self.score), True, NOT_SO_BLACK)
            canvas.blit(end_surface, (GAME_WIDTH/2 - end_surface.get_width()/2, GAME_HEIGHT/2 - end_surface.get_height()/2))
            return

        self.player.render(canvas)

        for b in self.balls:
            b.render(canvas)

        for p in self.powerups:
            p.render(canvas)

        # Render Score Text
        self.player_lives_surface = self.font_renderer.render(str(self.player.lives), True, NOT_SO_BLACK)
        self.player_score_surface = self.font_renderer.render(str(self.score), True, NOT_SO_BLACK)
        self.player_multiplier_surface = self.font_renderer.render(str(self.score_multiplier), True, NOT_SO_BLACK)
        canvas.blit(self.player_lives_label_surface, (GAME_WIDTH/3 - self.player_lives_label_surface.get_width(), 15))
        canvas.blit(self.player_lives_surface, (GAME_WIDTH/3, 15))
        canvas.blit(self.player_score_label_surface, (GAME_WIDTH/3 - self.player_score_label_surface.get_width(), 30))
        canvas.blit(self.player_score_surface, (GAME_WIDTH/3, 30))
        canvas.blit(self.player_multiplier_label_surface, (GAME_WIDTH/3 - self.player_multiplier_label_surface.get_width(), 45))
        canvas.blit(self.player_multiplier_surface, (GAME_WIDTH/3, 45))

    def on_wall_hit(self):
        self.wall_hit_sound.play()

    def on_pad_hit(self):
        self.pad_hit_sound.play()

    def on_powerup(self):
        self.powerup_sound.play()


    def remove_listeners(self):
        super(SinglePlayerState, self).remove_listeners()
        self.player.remove_listeners()

    def dispose(self):
        pygame.mixer.music.stop()
