import pygame

from constants import *
from game_state import GameState


class PlayState(GameState):
    LISTEN_KEYS = (pygame.K_UP,)

    def __init__(self, game):
        super(PlayState, self).__init__(game)
        self.y = 10
        self.vel_y = 0.2
        self.text = None

    def show(self):
        font_renderer = pygame.font.Font(None, 36)
        self.text = font_renderer.render('Hello There', 1, NOT_SO_BLACK)

    def update(self, delta):
        if self.input.key_clicked(pygame.K_UP):
            print "Up clicked!"
            self.state_manager.set_state(None)
        if self.y + self.text.get_rect().height >= GAME_HEIGHT or self.y < 0:
            self.vel_y *= -1
        self.y += delta * self.vel_y

    def render(self, canvas):
        canvas.fill(NOT_SO_WHITE)
        canvas.blit(self.text, (GAME_WIDTH / 2 - self.text.get_rect().width / 2, self.y))

    def dispose(self):
        pass
