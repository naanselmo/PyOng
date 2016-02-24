from constants import *
from core.game_math import Vector2
from entity import Entity


class Ball(Entity):
    def __init__(self, position, width, height):
        super(Ball, self).__init__(position, width, height)

    def update(self, delta):
        self.update_bounds()

    def render(self, canvas):
        pygame.draw.rect(canvas, NOT_SO_BLACK, self.get_bounds())
