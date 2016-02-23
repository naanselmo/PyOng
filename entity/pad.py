import pygame
import resources


from constants import *
from entity import Entity
from core.math import Vec2d


class Pad(Entity):
    def __init__(self, coords=Vec2d(10, 10), bounds=Vec2d(10, 10), velocity=Vec2d(0, 0.02)):
        super(Pad, self).__init__(coords, bounds, velocity)
        self.up = False

    def update(self, delta):
        pass

    def render(self, canvas):
        pygame.draw.rect(canvas, NOT_SO_BLACK, self)

    def move_up(self, delta):
        new_position = Vec2d(self.left, self.top) * self.velocity * -delta
        self.move_ip(new_position.x, new_position.y)

    def move_down(self, delta):
        new_position = Vec2d(self.left, self.top) * self.delta
        self.move_ip(new_position.x, new_position.y)


    def dash(self, delta):
        pass

