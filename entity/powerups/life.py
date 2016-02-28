import pygame
import resources

from constants import *
from entity.powerups.powerup import PowerUp


class Life(PowerUp):
    """docstring for Life"""

    def __init__(self, position, velocity = (0, 0), width=POWERUP_SIZE, height=POWERUP_SIZE):
        super(Life, self).__init__(position, velocity, width, height)
        self.image = pygame.transform.scale(pygame.image.load(resources.get_sprite("life.png"))

    def update(self, delta):
        pass

    def apply(self, state, ball):
        if ball.owner is not None:
            ball.owner.lives += 1
