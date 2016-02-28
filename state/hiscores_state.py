import pygame
from pygame.mixer import Sound

import resources

from constants import *
from core.menu import HorizontalMenuOptions
from state.game_state import GameState


class HiscoresState(GameState):
    def __init__(self, game):
        super(HiscoresState, self).__init__(game)
        # Listen to escape only
        self.listen_keys = (pygame.K_ESCAPE, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN)

        # Model of the hiscores
        self.scores = self.hiscores.get_scores(10)
        self.back_options = HorizontalMenuOptions(['Back'], self.on_click, self.on_change, True, False)

        # Surfaces
        self.title_surface = None
        self.scores_surfaces = []

        # Sounds
        self.select_sound = None

    def show(self):
        font = resources.get_font('prstartcustom.otf')

        # Make title
        font_renderer = pygame.font.Font(font, 15)
        self.title_surface = font_renderer.render('Hi-scores', True, NOT_SO_BLACK)

        # Make all scores
        # Get the score with highest width
        max_width_score = max(self.scores, key=self.score_width)
        # Calculate its width, and add 4 dots
        max_width = self.score_width(max_width_score) + 4
        font_renderer = pygame.font.Font(font, 12)
        for score in self.scores:
            self.scores_surfaces.append(
                font_renderer.render(
                    score.name + '.' * (max_width - self.score_width(score)) + str(score.score),
                    True,
                    NOT_SO_BLACK
                )
            )

        # Make the back option
        self.back_options.init(font, 15, True, NOT_SO_BLACK)

        # Load all sounds
        self.select_sound = Sound(resources.get_sound('menu_select.wav'))

    def update(self, delta):
        self.back_options.update(self.input)

    def render(self, canvas):
        canvas.fill(NOT_SO_WHITE)
        # Draw title
        canvas.blit(self.title_surface, (GAME_WIDTH / 2 - self.title_surface.get_width() / 2, 30))

        # Draw scores
        for i in range(len(self.scores_surfaces)):
            score_surface = self.scores_surfaces[i]
            surface_x = GAME_WIDTH / 2 - score_surface.get_width() / 2
            surface_y = i * score_surface.get_height() * 1.8 + (self.title_surface.get_height() + 15) * 2.5
            canvas.blit(score_surface, (surface_x, surface_y))

        # Draw back option
        self.back_options.render(canvas, GAME_WIDTH * 0.80, GAME_HEIGHT - 20 - self.back_options.get_height())

    def score_width(self, score):
        return len(score.name) + len(str(score.score))

    def on_click(self, option):
        from menu_state import MenuState
        self.state_manager.set_state(MenuState(self.game))
        self.select_sound.play()

    def on_change(self, old_option, new_option):
        self.select_sound.play()

    def dispose(self):
        pass
