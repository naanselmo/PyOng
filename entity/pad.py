import pygame
from pygame.rect import Rect

import resources

from constants import *
from entity import Entity
from core.game_math import Vector2


class Pad(Entity):
    def __init__(self, position, width = 20, height = 100, velocity = Vector2(0, 0.8)):
        super(Pad, self).__init__(position, width, height)
        self.velocity = velocity # Movement velocity

    def update(self, delta):
        pass

    def move_up(self, delta):
        self.position += self.velocity * delta * -1
        self.update_bounds()

    def move_down(self, delta):
        self.position += self.velocity * delta * 1
        self.update_bounds()

    def dash(self, delta):
        pass

    def render(self, canvas):
        pygame.draw.rect(canvas, NOT_SO_BLACK, self.get_bounds())
