import pygame
import resources

from constants import *
from entity.powerups.powerup import PowerUp

from os.path import join


class Shrink(PowerUp):
    """docstring for Shrink"""

    def __init__(self, position, velocity = (0, 0), width=POWERUP_WIDTH, height=POWERUP_HEIGHT):
        super(Shrink, self).__init__(position, velocity, width, height)
        self.image = pygame.image.load(join("resources", "sprites", "shrink.png")).convert()

    def update(self, delta):
        pass

    def apply(self, state, ball):
        if ball.owner is not None:
            ball.owner.pad.position.y += ball.owner.pad.height * (1 - POWERUP_SHRINK_FACTOR)/2
            ball.owner.pad.height *= POWERUP_SHRINK_FACTOR
