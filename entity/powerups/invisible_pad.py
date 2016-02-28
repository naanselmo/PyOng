import pygame
import resources

from constants import *
from entity.powerups.powerup import PowerUp


class InvisiblePad(PowerUp):
    """docstring for InvisiblePad"""

    def __init__(self, position, velocity = (0, 0), width=POWERUP_SIZE, height=POWERUP_SIZE):
        super(InvisiblePad, self).__init__(position, velocity, width, height)
        self.image = pygame.image.load(resources.get_sprite("invisible_pad.png")).convert()

    def update(self, delta):
        pass

    def apply(self, state, ball):
        ball.owner.pad.invisible = True
        ball.owner.pad.invisible_timer = POWERUP_INVISIBLE_DURATION
