import pygame
import resources

from constants import *
from entity.powerups.powerup import PowerUp


class Life(PowerUp):
    """docstring for Life"""

    def __init__(self, position, velocity = (0, 0), width=POWERUP_WIDTH, height=POWERUP_HEIGHT):
        super(Life, self).__init__(position, velocity, width, height)
        self.image = pygame.image.load(resources.get_sprite("life.png")).convert()

    def update(self, delta):
        pass

    def apply(self, state, ball):
        if ball.owner is not None:
            ball.owner.lives += 1
