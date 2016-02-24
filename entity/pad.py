from constants import *
from core.game_math import Vector2
from entity import Entity


class Pad(Entity):
    COLLIDE_THRESHOLD = 16

    def __init__(self, position, width=20, height=100, velocity=Vector2(0, 0)):
        super(Pad, self).__init__(position, width, height)

    def update(self, delta):
        self.update_bounds()

    def move_up(self, delta):
        pass

    def move_down(self, delta):
        pass

    def dash(self, delta):
        pass

    def idle(self, delta):
        pass

    def collides(self, ball):
        if self.position.y < ball.position.y < self.position.y + self.height:
            return self.position.x + self.width >= ball.position.x >= \
                   self.position.x + self.width / Pad.COLLIDE_THRESHOLD
        return False

    def render(self, canvas):
        pygame.draw.rect(canvas, NOT_SO_BLACK, self.get_bounds())
