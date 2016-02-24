import pygame
import resources

from constants import *
from state.game_state import GameState


class HiscoresState(GameState):
    def __init__(self, game):
        super(HiscoresState, self).__init__(game)
        # Listen to escape only
        self.listen_keys = (pygame.K_ESCAPE,)

        # Model of the hiscores
        self.scores = self.hiscores.get_scores(10)

        # Surfaces
        self.title_surface = None
        self.scores_surfaces = []

    def show(self):
        font = resources.get_font('prstartcustom.otf')

        # Make title
        font_renderer = pygame.font.Font(font, 15)
        self.title_surface = font_renderer.render('Hi-scores', 1, NOT_SO_BLACK)

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
                    1,
                    NOT_SO_BLACK
                )
            )

    def update(self, delta):
        if self.input.key_clicked(pygame.K_ESCAPE):
            from menu_state import MenuState
            self.state_manager.set_state(MenuState(self.game))

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

    def score_width(self, score):
        return len(score.name) + len(str(score.score))

    def dispose(self):
        pass
