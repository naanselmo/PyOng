import pygame

from config import *
from gamestate import GameState


class PlayState(GameState):
    def __init__(self):
        self.y = 10
        self.vel_y = 0.2
        self.text = None

    def show(self):
        font_renderer = pygame.font.Font(None, 36)
        self.text = font_renderer.render('Hello There', 1, (10, 10, 10))

    def update(self, delta):
        if self.y + self.text.get_rect().height >= GAME_HEIGHT or self.y < 0:
            self.vel_y *= -1
        self.y += delta * self.vel_y

    def render(self, canvas):
        canvas.blit(self.text, (GAME_WIDTH / 2 - self.text.get_rect().width / 2, self.y))

    def dispose(self):
        pass
