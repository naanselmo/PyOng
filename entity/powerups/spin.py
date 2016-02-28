import pygame
import resources

from constants import *
from entity.powerups.powerup import PowerUp

from os.path import join

from random import randint


class Spin(PowerUp):
    """docstring for Spin"""

    def __init__(self, position, velocity = (0, 0), width=POWERUP_WIDTH, height=POWERUP_HEIGHT):
        super(Spin, self).__init__(position, velocity, width, height)
        self.image = pygame.image.load(join("resources", "sprites", "spin.png")).convert()

    def update(self, delta):
        pass

    def apply(self, state, ball):
        ball.velocity.rotate(randint(0, 360))
