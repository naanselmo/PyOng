import pygame
import resources

from constants import *
from entity.powerups.powerup import PowerUp


class Speed(PowerUp):
    """docstring for Speed"""

    def __init__(self, position, velocity = (0, 0), width=POWERUP_WIDTH, height=POWERUP_HEIGHT):
        super(Speed, self).__init__(position, velocity, width, height)
        self.image = pygame.image.load(resources.get_sprite("speed.png")).convert()

    def update(self, delta):
        pass

    def apply(self, state, ball):
        ball.velocity *= 1.5
