import pygame
import resources

from constants import *
from entity.powerups.powerup import PowerUp


class InvisibleBall(PowerUp):
    """docstring for InvisibleBall"""

    def __init__(self, position, velocity = (0, 0), width=POWERUP_SIZE, height=POWERUP_SIZE):
        super(InvisibleBall, self).__init__(position, velocity, width, height)
        self.image = pygame.transform.scale(pygame.image.load(resources.get_sprite("invisible_ball.png")).convert(), (width, height))

    def update(self, delta):
        pass

    def apply(self, state, ball):
        ball.invisible = True
        ball.invisible_timer = POWERUP_INVISIBLE_DURATION
