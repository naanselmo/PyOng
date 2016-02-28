import pygame
import resources

from constants import *
from entity.powerups.powerup import PowerUp


from entity.ball import Ball


class Duplicate(PowerUp):
    """docstring for Duplicate"""

    def __init__(self, position, velocity = (0, 0), width=POWERUP_SIZE, height=POWERUP_SIZE):
        super(Duplicate, self).__init__(position, velocity, width, height)
        self.image = pygame.transform.scale(pygame.image.load(resources.get_sprite("duplicate.png")).convert(), (width, height))

    def update(self, delta):
        pass

    def apply(self, state, ball):
        with state.game.rendering:
            state.balls += [Ball(ball.position, (ball.velocity.x * -1, ball.velocity.y), ball.width, ball.height, ball.damage, ball.owner)]
