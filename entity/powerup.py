import pygame
import resources

from entity import Entity
from core.game_math import Vector2


class PowerUp(Entity):
    def __init__(self, position, width, height):
        super(PowerUp, self).__init__(position, width, height)

    def update(self, delta):
        pass

    def render(self, canvas):
        pass
