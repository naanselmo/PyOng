import pygame
import resources

from constants import *
from entity.powerups.powerup import PowerUp

from os.path import join


class Charge(PowerUp):
    """docstring for Charge"""

    def __init__(self, position, velocity = (0, 0), width=POWERUP_WIDTH, height=POWERUP_HEIGHT):
        super(Charge, self).__init__(position, velocity, width, height)
        self.image = pygame.image.load(join("resources", "sprites", "charge.png")).convert()

    def update(self, delta):
        pass

    def apply(self, state, ball):
        if ball.owner is not None:
            ball.owner.pad.charge += POWERUP_CHARGE
