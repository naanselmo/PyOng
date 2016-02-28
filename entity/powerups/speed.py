import pygame
import resources

from constants import *
from entity.powerups.powerup import PowerUp


class Speed(PowerUp):
    """docstring for Speed"""

    def __init__(self, position, velocity = (0, 0), width=POWERUP_WIDTH, height=POWERUP_HEIGHT):
        super(Speed, self).__init__(position, velocity, width, height)

    def update(self, delta):
        pass

    def render(self, canvas):
        pygame.draw.rect(canvas, NOT_SO_BLACK, self.get_bounds())

    def apply(self, state, ball):
        with state.game.rendering:
            ball.velocity *= 1.5
