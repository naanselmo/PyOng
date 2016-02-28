import pygame
import resources
from constants import *

from entity import Entity
from core.game_math import Vector2
from random import uniform, choice


class Ball(Entity):
    def __init__(self, position = Vector2(GAME_WIDTH/2, GAME_HEIGHT/2), velocity = None, width = BALL_WIDTH, height = BALL_HEIGHT, damage=BALL_DAMAGE, owner = None):
        if velocity is None: velocity = Vector2(uniform(BALL_MIN_START_SPEED, BALL_MAX_START_SPEED)*choice((-1, 1)), uniform(BALL_MIN_START_SPEED, BALL_MAX_START_SPEED)*choice((-1, 1)))
        super(Ball, self).__init__(position, velocity, width, height)
        self.damage = damage
        self.owner = owner

    def update(self, delta):
        self.position += self.velocity * delta
        self.update_bounds()

    def render(self, canvas):
        pygame.draw.rect(canvas, NOT_SO_BLACK, self.get_bounds())
