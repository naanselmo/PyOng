import pygame
import resources

from constants import *
from entity.powerups.powerup import PowerUp


class Speed(PowerUp):
    """docstring for Speed"""

    def __init__(self, position, velocity = (0, 0), width=POWERUP_SIZE, height=POWERUP_SIZE):
        super(Speed, self).__init__(position, velocity, width, height)
        self.image = pygame.transform.scale(pygame.image.load(resources.get_sprite("speed.png")).convert(), (width, height))

    def update(self, delta):
        pass

    def apply(self, state, ball):
        ball.velocity *= 1.5
