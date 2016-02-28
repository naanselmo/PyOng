import pygame
import resources

from constants import *
from entity.powerups.powerup import PowerUp

from os.path import join


class Multiplier(PowerUp):
    """docstring for Multiplier"""

    def __init__(self, position, velocity = (0, 0), width=POWERUP_WIDTH, height=POWERUP_HEIGHT):
        super(Multiplier, self).__init__(position, velocity, width, height)
        self.image = pygame.image.load(join("resources", "sprites", "multiplier.png")).convert()

    def update(self, delta):
        pass

    def apply(self, state, ball):
        state.score_multiplier *= POWERUP_MULTIPLIER
