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

    def add_listeners(self):
        super(PlayState, self).add_listeners()
        self.player1.add_listeners()

    def update(self, delta):
        self.player1.update(delta)

    def render(self, canvas):
        canvas.fill(NOT_SO_WHITE)
        self.player1.render(canvas)

    def remove_listeners(self):
        super(PlayState, self).remove_listeners()
        self.player1.remove_listeners()

    def dispose(self):
        pass
