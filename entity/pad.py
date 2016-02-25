import pygame
from pygame.rect import Rect

import resources

from constants import *
from entity import Entity
from core.game_math import Vector2


class Pad(Entity):
    def __init__(self, position, width = PAD_WIDTH, height = PAD_HEIGHT, velocity = Vector2(0, 0), speed = PAD_SPEED):
        super(Pad, self).__init__(position, width, height)
        self.velocity = velocity
        self.speed = speed

    def update(self, delta):
        self.position.y += self.velocity.y * delta
        self.update_bounds()

    def move_up(self, delta):
        self.velocity.y = self.speed * -1

    def move_down(self, delta):
        self.velocity.y = self.speed * 1

    def stop_movement(self, delta):
        self.velocity.y = 0

    def dash(self, delta):
        pass

    def render(self, canvas):
        pygame.draw.rect(canvas, NOT_SO_BLACK, self.get_bounds())
