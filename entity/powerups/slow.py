import pygame
import resources

from constants import *
from entity.powerups.powerup import PowerUp

from os.path import join


class Slow(PowerUp):
    """docstring for Slow"""

    def __init__(self, position, velocity = (0, 0), width=POWERUP_WIDTH, height=POWERUP_HEIGHT):
        super(Slow, self).__init__(position, velocity, width, height)
        self.image = pygame.image.load(join("resources", "sprites", "slow.png")).convert()

    def update(self, delta):
        pass

    def apply(self, state, ball):
        ball.velocity /= 2
