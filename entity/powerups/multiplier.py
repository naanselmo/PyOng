import pygame
import resources

from constants import *
from entity.powerups.powerup import PowerUp


class Multiplier(PowerUp):
    """docstring for Multiplier"""

    def __init__(self, position, velocity = (0, 0), width=POWERUP_SIZE, height=POWERUP_SIZE):
        super(Multiplier, self).__init__(position, velocity, width, height)
        self.image = pygame.transform.scale(pygame.image.load(resources.get_sprite("multiplier.png")).convert(), (width, height))

    def update(self, delta):
        pass

    def apply(self, state, ball):
        state.score_multiplier *= POWERUP_MULTIPLIER
