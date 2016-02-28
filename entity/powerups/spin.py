import pygame
import resources

from constants import *
from entity.powerups.powerup import PowerUp

from random import randint


class Spin(PowerUp):
    """docstring for Spin"""

    def __init__(self, position, velocity = (0, 0), width=POWERUP_SIZE, height=POWERUP_SIZE):
        super(Spin, self).__init__(position, velocity, width, height)
        self.image = pygame.transform.scale(pygame.image.load(resources.get_sprite("spin.png")).convert(), (width, height))

    def update(self, delta):
        pass

    def apply(self, state, ball):
        ball.velocity.rotate(randint(0, 360))
