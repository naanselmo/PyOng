import pygame
import math

from constants import *
from core.game_math import Vector2
from entity.ball import Ball
from game_state import GameState

from player import Player
from entity.pad import Pad

class MultiPlayerState(GameState):
    def __init__(self, game):
        super(MultiPlayerState, self).__init__(game)
        self.player1 = Player(game.input, PLAYER1, Pad(Vector2(GAME_WIDTH - PAD_DISTANCE - PAD_WIDTH, GAME_HEIGHT/2 - PAD_HEIGHT/2)))
        self.player2 = Player(game.input, PLAYER2, Pad(Vector2(0 + PAD_DISTANCE, GAME_HEIGHT/2 - PAD_HEIGHT/2)))
        self.ball = Ball()

    def show(self):
        pass

    def add_listeners(self):
        super(MultiPlayerState, self).add_listeners()
        self.player1.add_listeners()
        self.player2.add_listeners()

    def update(self, delta):
        self.player1.update(delta)
        self.player2.update(delta)
        self.ball.update(delta)

        # Check pads
        self.check_upper_bottom_boundaries(self.player1.pad)
        self.check_upper_bottom_boundaries(self.player2.pad)

        # Check ball
        self.check_upper_bottom_boundaries(self.ball)
        self.check_ball_collision(self.ball, self.player1.pad)
        self.check_ball_collision(self.ball, self.player2.pad)

        # Check scoring
        self.check_left_boundary(self.ball)
        self.check_right_boundary(self.ball)

    def check_upper_bottom_boundaries(self, entity):
        # Check top boundary
        if entity.position.y < 0:
            entity.position.y *= -1
            entity.velocity.y *= -1

        # Check bottom boundary
        elif entity.position.y + entity.height > GAME_HEIGHT:
            entity.position.y -= (entity.position.y + entity.height - GAME_HEIGHT)*2
            entity.velocity.y *= -1

    def check_left_boundary(self, entity):
        if entity.position.x <= 0:
            entity.position.x *= -1
            entity.velocity.x *= -1

    def check_right_boundary(self, entity):
        if entity.position.x + entity.width >= GAME_WIDTH:
            entity.position.x -= (entity.position.x + entity.width - GAME_WIDTH)*2
            entity.velocity.x *= -1

    def check_ball_collision(self, ball, pad):
        collision = ball.get_bounds().colliderect(pad.get_bounds())

        # Maybe a collision should've happened but wasn't detected
        if (not collision):
            i = 0
            while not(collision) and i < COLLISION_INTERPOLATION:
                i += 1

        if collision:
            self.calculate_collision(pad, ball)

            if ball.velocity.x < BALL_SPEED_LIMIT:
                ball.velocity.x *= BALL_SPEED_MULTIPLIER
            else:
                ball.velocity.x /= BALL_SPEED_MULTIPLIER

            ball.velocity.y += BALL_SPEED_TRANSFER * pad.velocity.y
            ball.velocity.x += BALL_SPEED_TRANSFER_DASH * pad.velocity.x

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
        self.ball.render(canvas)

    def remove_listeners(self):
        super(MultiPlayerState, self).remove_listeners()
        self.player1.remove_listeners()
        self.player2.remove_listeners()

    def dispose(self):
        pass
