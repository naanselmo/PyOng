import pygame
import resources

from constants import *
from entity.powerups.powerup import PowerUp

from random import randint


class Teleport(PowerUp):
    """docstring for Teleport"""

    def __init__(self, position, velocity = (0, 0), width=POWERUP_WIDTH, height=POWERUP_HEIGHT):
        super(Teleport, self).__init__(position, velocity, width, height)

    def update(self, delta):
        pass

    def render(self, canvas):
        pygame.draw.rect(canvas, NOT_SO_BLACK, self.get_bounds())

    def apply(self, state, ball):
        ball.position.x = randint(GAME_WIDTH * 0.3, GAME_WIDTH * 0.7)
        ball.position.y = randint(ball.height, GAME_HEIGHT - ball.height)
