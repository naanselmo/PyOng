import pygame
import resources

from entity import Entity
from core.math import Vec2d


class Ball(Entity):
    def __init__(self, coords=Vec2d(0, 0), bounds=Vec2d(0, 0), velocity=Vec2d(0, 0)):
        super(Ball, self).__init__(coords, bounds, velocity)

    def update(self, delta):
        pass

    def render(self, canvas):
        pass
