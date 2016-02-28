import pygame
import resources

from constants import *
from entity.powerups.powerup import PowerUp


class Stun(PowerUp):
    """docstring for Stun"""

    def __init__(self, position, velocity = (0, 0), width=POWERUP_SIZE, height=POWERUP_SIZE):
        super(Stun, self).__init__(position, velocity, width, height)
        self.image = pygame.image.load(resources.get_sprite("stun.png")).convert()

    def update(self, delta):
        pass

    def apply(self, state, ball):
        ball.stunning = True
