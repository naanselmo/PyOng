import pygame
import math

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
        self.player = Player(game.input, PLAYER1, Pad(Vector2(0 + PAD_DISTANCE, GAME_HEIGHT/2 - PAD_HEIGHT/2)), SINGLEPLAYER_LIVES)
        self.balls = [Ball()]
        self.powerups = []
        self.score_multiplier = SINGLEPLAYER_SCORE_MULTIPLIER
        self.time_since_powerup_check = 0
        self.score = 0

    def show(self):
        pass

    def add_listeners(self):
        super(SinglePlayerState, self).add_listeners()
        self.player.add_listeners()

    def update(self, delta):
        # Check pads
        self.player.update(delta)
        self.check_upper_bottom_right_boundaries(self.player.pad)

        # Increment counter
        self.time_since_powerup_check += delta

        if self.time_since_powerup_check > POWERUP_TIMER:
            if len(self.powerups) < POWERUP_MAX and randint(0, POWERUP_PROBABILITY) == 0:
                self.powerups += [PowerUp.get_random_powerup((randint(GAME_WIDTH * 0.3, GAME_WIDTH * 0.7), randint(POWERUP_HEIGHT, GAME_HEIGHT - POWERUP_HEIGHT)), False)]
            self.time_since_powerup_check = 0

        # Check balls
        for b in self.balls:
            b.update(delta)

            # Check each ball
            self.check_upper_bottom_right_boundaries(b)

            # Check each pad
            if self.check_entity_collision(delta, self.player.pad, b):
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

            # Check each powerup
            if b.owner != None:
                for p in self.powerups:
                    if self.check_entity_collision(delta, p, b):
                        p.apply(self, b)
                        self.powerups.remove(p)

                        break

            # Check scoring
            if self.check_left_boundary(b, self.player):
                with self.game.rendering:
                    self.balls = [Ball()]
                    self.balls[0].update_bounds()
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
            print "Player lost a life"
            if player.lives <= 0:
                print "Player lost"
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
        self.player.render(canvas)

        for b in self.balls:
            b.render(canvas)

        for p in self.powerups:
            p.render(canvas)

    def remove_listeners(self):
        super(SinglePlayerState, self).remove_listeners()
        self.player.remove_listeners()

    def dispose(self):
        pass
