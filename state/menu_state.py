import pygame
import resources

from constants import *
from state.game_state import GameState


class MenuState(GameState):
    LISTEN_KEYS = (pygame.K_DOWN, pygame.K_UP, pygame.K_RETURN)
    PLAY_OPTION = 0
    HISCORES_OPTION = 1
    EXIT_OPTION = 2

    def __init__(self, game):
        super(MenuState, self).__init__(game)
        # Model of the menu
        self.title = GAME_TITLE
        self.options = ['Play', 'Hi-scores', 'Exit']
        self.selected = 0
        self.hiscore = str(self.game.hiscores.get_hiscore()[1])
        self.rights = u'\u00a9 Dezassete'

        # Surfaces
        self.hiscore_surface = None
        self.hiscore_label_surface = None
        self.title_surface = None
        self.options_surfaces = []
        self.rights_surface = None

    def show(self):
        # Get font name
        font = resources.get_font('prstartcustom.otf')

        # Make Hi-score and rights
        font_renderer = pygame.font.Font(font, 12)
        self.hiscore_label_surface = font_renderer.render('Hi-score', 1, NOT_SO_BLACK)
        self.hiscore_surface = font_renderer.render(self.hiscore, 1, NOT_SO_BLACK)
        self.rights_surface = font_renderer.render(self.rights, 1, NOT_SO_BLACK)

        # Make title
        font_renderer = pygame.font.Font(font, 36)
        self.title_surface = font_renderer.render(GAME_TITLE, 1, NOT_SO_BLACK)

        # Make options
        font_renderer = pygame.font.Font(font, 15)
        self.options_surfaces = [font_renderer.render(option, 1, NOT_SO_BLACK) for option in self.options]

    def update(self, delta):
        if self.input.key_clicked(pygame.K_DOWN):
            self.selected = (self.selected + 1) % len(self.options)
        if self.input.key_clicked(pygame.K_UP):
            self.selected = (self.selected - 1) % len(self.options)
        if self.input.key_clicked(pygame.K_RETURN):
            self.on_click(self.selected)

    def render(self, canvas):
        canvas.fill(NOT_SO_WHITE)
        # Render hiscore
        canvas.blit(self.hiscore_label_surface, (GAME_WIDTH / 2 - self.hiscore_label_surface.get_width() / 2, 15))
        canvas.blit(self.hiscore_surface, (
            GAME_WIDTH / 2 - self.hiscore_surface.get_width() / 2,
            (self.hiscore_label_surface.get_height() + 15) * 1.2
        ))

        # Render the title surface
        canvas.blit(self.title_surface, (
            GAME_WIDTH / 2 - self.title_surface.get_width() / 2,
            GAME_HEIGHT / 4 * 1.4 - self.title_surface.get_height() / 2
        ))

        # Render the options
        for i in range(len(self.options_surfaces)):
            option_surface = self.options_surfaces[i]
            surface_x = GAME_WIDTH / 2 - option_surface.get_width() / 2
            surface_y = i * option_surface.get_height() * 1.8 + GAME_HEIGHT / 4 * 2.2
            canvas.blit(option_surface, (surface_x, surface_y))
            # Draw arrow
            if self.selected == i:
                points = self.arrow_points(surface_x - 20, surface_y + 2, 10, 10)
                pygame.draw.polygon(canvas, NOT_SO_BLACK, points)

        # Draw rights
        canvas.blit(self.rights_surface, (
            GAME_WIDTH / 2 - self.rights_surface.get_width() / 2,
            GAME_HEIGHT - self.rights_surface.get_height() - 15
        ))

    def arrow_points(self, x, y, width, height):
        return (x, y), (x, y + height), (x + width, y + (height / 2))

    def on_click(self, option):
        print 'Option selected:', self.options[option]
        if option == MenuState.EXIT_OPTION:
            self.game.stop()
        elif option == MenuState.PLAY_OPTION:
            from state.play_state import PlayState
            self.state_manager.set_state(PlayState(self.game))
        elif option == MenuState.HISCORES_OPTION:
            from state.hiscores_state import HiscoresState
            self.state_manager.set_state(HiscoresState(self.game))

    def dispose(self):
        pass
