import pygame

from constants import *
from core.math import Vector2
from entity.ball import Ball
from game_state import GameState

from player import Player
from entity.pad import Pad

class PlayState(GameState):
    def __init__(self, game):
        super(PlayState, self).__init__(game)
        self.player1 = Player(game.input, PLAYER1, Pad(Vector2(5, 10)))
        self.ball = Ball(Vector2(100, 100), 10, 10)

    def show(self):
        pass

    def add_listeners(self):
        super(PlayState, self).add_listeners()
        self.player1.add_listeners()

    def update(self, delta):
        self.player1.update(delta)

        if self.ball.get_bounds().colliderect(self.player1.pad.get_bounds()):
            self.ball.velocity.x *= -1

        if self.ball.position.x + self.ball.width >= GAME_WIDTH:
            self.ball.velocity.x *= -1

        if self.ball.position.y + self.ball.height >= GAME_HEIGHT or self.ball.position.y < 0:
            self.ball.velocity.y *= -1

        if self.ball.position.x + self.ball.width > GAME_WIDTH:
            self.ball.position.x = GAME_WIDTH - self.ball.width

        if self.ball.position.y < 0:
            self.ball.position.y = 0

        if self.ball.position.y + self.ball.height > GAME_HEIGHT:
            self.ball.position.y = GAME_HEIGHT - self.ball.height

        self.ball.update(delta)

    def render(self, canvas):
        canvas.fill(NOT_SO_WHITE)
        self.player1.render(canvas)
        self.ball.render(canvas)

    def remove_listeners(self):
        super(PlayState, self).remove_listeners()
        self.player1.remove_listeners()

    def dispose(self):
        pass
