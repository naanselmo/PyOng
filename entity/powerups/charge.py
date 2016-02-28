import pygame
import resources

from constants import *
from entity.powerups.powerup import PowerUp


class Charge(PowerUp):
    """docstring for Charge"""

    def __init__(self, position, velocity = (0, 0), width=POWERUP_SIZE, height=POWERUP_SIZE):
        super(Charge, self).__init__(position, velocity, width, height)
        self.image = pygame.transform.scale(pygame.image.load(resources.get_sprite("charge.png")).convert(), (width, height))

    def update(self, delta):
        pass

    def apply(self, state, ball):
        if ball.owner is not None:
            ball.owner.pad.charge += POWERUP_CHARGE
