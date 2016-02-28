import pygame
import resources

from constants import *
from entity.powerups.powerup import PowerUp


from entity.ball import Ball


class Duplicate(PowerUp):
    """docstring for Duplicate"""

    def __init__(self, position, velocity = (0, 0), width=POWERUP_WIDTH, height=POWERUP_HEIGHT):
        super(Duplicate, self).__init__(position, velocity, width, height)
        self.image = pygame.image.load(resources.get_sprite("duplicate.png")).convert()

    def update(self, delta):
        pass

    def apply(self, state, ball):
        with state.game.rendering:
            state.balls += [Ball(ball.position, (ball.velocity.x * -1, ball.velocity.y), ball.width, ball.height, ball.damage, ball.owner)]
