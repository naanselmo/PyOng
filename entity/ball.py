import pygame
import resources
from constants import *

from entity import Entity
from core.math import Vector2


class Ball(Entity):
    def __init__(self, position, width, height, velocity = Vector2(0.5, 0.5)):
        super(Ball, self).__init__(position, width, height)
        self.velocity = velocity

    def update(self, delta):
        self.position += self.velocity * delta
        self.update_bounds()

    def render(self, canvas):
        pygame.draw.rect(canvas, NOT_SO_BLACK, self.get_bounds())
