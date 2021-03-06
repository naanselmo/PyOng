import pygame
import resources

from constants import *
from entity.powerups.powerup import PowerUp

from random import randint


class Teleport(PowerUp):
    """docstring for Teleport"""

    def __init__(self, position, velocity = (0, 0), width=POWERUP_SIZE, height=POWERUP_SIZE):
        super(Teleport, self).__init__(position, velocity, width, height)
        self.image = pygame.transform.scale(pygame.image.load(resources.get_sprite("teleport.png")).convert(), (width, height))

    def update(self, delta):
        pass

    def apply(self, state, ball):
        ball.position.x = randint(GAME_WIDTH * 0.3, GAME_WIDTH * 0.7)
        ball.position.y = randint(ball.height, GAME_HEIGHT - ball.height)
