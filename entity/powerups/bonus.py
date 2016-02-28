import pygame
import resources

from constants import *
from entity.powerups.powerup import PowerUp

from os.path import join


class Bonus(PowerUp):
    """docstring for Bonus"""

    def __init__(self, position, velocity = (0, 0), width=POWERUP_WIDTH, height=POWERUP_HEIGHT):
        super(Bonus, self).__init__(position, velocity, width, height)
        self.image = pygame.image.load(join("resources", "sprites", "bonus.png")).convert()

    def update(self, delta):
        pass

    def apply(self, state, ball):
        state.score += POWERUP_BONUS*state.score_multiplier
