import pygame
import resources
from constants import *

from entity import Entity
from core.game_math import Vector2
from random import uniform, choice


class VirtualBall(Entity):
    def __init__(self, position = Vector2(GAME_WIDTH/2, GAME_HEIGHT/2), width = BALL_WIDTH, height = BALL_HEIGHT, velocity = Vector2(uniform(BALL_MIN_START_SPEED, BALL_MAX_START_SPEED)*choice((-1, 1)), uniform(BALL_MIN_START_SPEED, BALL_MAX_START_SPEED)*choice((-1, 1)))):
        super(VirtualBall, self).__init__(position, width, height)
        self.velocity = velocity

    def update(self, delta):
        self.position += self.velocity * delta
        self.update_bounds()

    def render(self, canvas):
        pass
