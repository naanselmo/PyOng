import pygame
import resources

from constants import *
from entity.powerups.powerup import PowerUp


class Extend(PowerUp):
    """docstring for Extend"""

    def __init__(self, position, velocity = (0, 0), width=POWERUP_WIDTH, height=POWERUP_HEIGHT):
        super(Extend, self).__init__(position, velocity, width, height)

    def update(self, delta):
        pass

    def render(self, canvas):
        pygame.draw.rect(canvas, NOT_SO_BLACK, self.get_bounds())

    def apply(self, state, ball):
        with state.game.rendering:
            if ball.owner is not None:
                ball.owner.pad.position.y -= ball.owner.pad.height * 0.25
                ball.owner.pad.height *= 1.5
