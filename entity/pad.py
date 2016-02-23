import pygame
import resources


from constants import *
from entity import Entity
from core.math import Vec2d


class Pad(Entity):
    def __init__(self, coords=Vec2d(10, 10), bounds=Vec2d(10, 10), velocity=Vec2d(0, 0)):
        super(Pad, self).__init__(coords, bounds, velocity)

    def update(self, delta):
        pass

    def render(self, canvas):
        pygame.draw.rect(canvas, NOT_SO_BLACK, self)

    def move_up(self):
        pass

    def move_down(self):
        pass

    def dash(self):
        pass
