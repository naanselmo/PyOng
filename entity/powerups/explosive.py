import pygame
import resources

from constants import *
from entity.powerups.powerup import PowerUp


class Explosive(PowerUp):
    """docstring for Explosive"""

    def __init__(self, position, velocity = (0, 0), width=POWERUP_SIZE, height=POWERUP_SIZE):
        super(Explosive, self).__init__(position, velocity, width, height)
        self.image = pygame.transform.scale(pygame.image.load(resources.get_sprite("explosive.png")).convert(), (width, height))

    def update(self, delta):
        pass

    def apply(self, state, ball):
        ball.damage *= POWERUP_DAMAGE_FACTOR
