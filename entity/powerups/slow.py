import pygame
import resources

from constants import *
from entity.powerups.powerup import PowerUp


class Slow(PowerUp):
    """docstring for Slow"""

    def __init__(self, position, velocity = (0, 0), width=POWERUP_WIDTH, height=POWERUP_HEIGHT):
        super(Slow, self).__init__(position, velocity, width, height)

    def update(self, delta):
        pass

    def render(self, canvas):
        pygame.draw.rect(canvas, NOT_SO_BLACK, self.get_bounds())

    def apply(self, state, ball):
        ball.velocity /= 2
