import pygame
import resources

from entity import Entity


class Ball(Entity):
    def __init__(self, game, coordinates={'x':0, 'y':0}, dimensions={'x':0, 'y':0}, velocity={'x':0.0, 'y':0.0}):
        super(Ball, self).__init__(game, coordinates, dimensions, velocity)

    def update(self, delta):
        pass

    def render(self, canvas):
        pass
