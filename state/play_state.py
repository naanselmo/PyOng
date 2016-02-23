import pygame

from constants import *
from game_state import GameState

from player import Player
from entity.pad import Pad

class PlayState(GameState):
    def __init__(self, game):
        super(PlayState, self).__init__(game)
        self.player1 = Player(game.input, PLAYER1, Pad())

    def show(self):
        pass

    def update(self, delta):
        pass

    def render(self, canvas):
        canvas.fill(NOT_SO_WHITE)
        self.player1.render(canvas)

    def dispose(self):
        pass
