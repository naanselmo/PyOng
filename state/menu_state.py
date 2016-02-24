import resources

from constants import *
from state.game_state import GameState


class MenuState(GameState):
    PLAY_OPTION = 0
    HISCORES_OPTION = 1
    EXIT_OPTION = 2

    ONE_PLAYER_OPTION = 0
    TWO_PLAYERS_OPTION = 1
    BACK_OPTION = 2

    def __init__(self, game):
        super(MenuState, self).__init__(game)
        # Listen to up, down, and enter
        self.listen_keys = (pygame.K_DOWN, pygame.K_UP, pygame.K_RETURN)

        # Model of the menu
        self.title = GAME_TITLE
        self.selected = 0
        self.hiscore = str(self.game.hiscores.get_hiscore().score)
        self.rights = u'\u00a9 Dezassete'
        self.current_menu_options = None
        self.main_menu_options = MenuOptions(['Play', 'Hi-scores', 'Exit'], self.main_menu_on_click)
        self.play_menu_options = MenuOptions(['1 Player', '2 Players', 'Back'], self.play_menu_on_click)

        # Surfaces
        self.hiscore_surface = None
        self.hiscore_label_surface = None
        self.title_surface = None
        self.rights_surface = None

    def show(self):
        # Get font name
        font = resources.get_font('prstartcustom.otf')

        # Make Hi-score and rights
        font_renderer = pygame.font.Font(font, 12)
        self.hiscore_label_surface = font_renderer.render('Hi-score', True, NOT_SO_BLACK)
        self.hiscore_surface = font_renderer.render(self.hiscore, True, NOT_SO_BLACK)
        self.rights_surface = font_renderer.render(self.rights, True, NOT_SO_BLACK)

        # Make title
        font_renderer = pygame.font.Font(font, 36)
        self.title_surface = font_renderer.render(GAME_TITLE, False, NOT_SO_BLACK)

        # Make all options and change to the main menu
        self.play_menu_options.init(font, 15)
        self.main_menu_options.init(font, 15)
        self.change_menu_options(self.main_menu_options)

    def update(self, delta):
        self.current_menu_options.update(self.input)

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

        # Render the current options
        self.current_menu_options.render(canvas)

        # Draw rights
        canvas.blit(self.rights_surface, (
            GAME_WIDTH / 2 - self.rights_surface.get_width() / 2,
            GAME_HEIGHT - self.rights_surface.get_height() - 15
        ))

    def change_menu_options(self, menu_options):
        self.current_menu_options = menu_options
        self.current_menu_options.reset()

    def main_menu_on_click(self, option):
        if option == MenuState.EXIT_OPTION:
            self.game.stop()
        elif option == MenuState.PLAY_OPTION:
            self.change_menu_options(self.play_menu_options)
        elif option == MenuState.HISCORES_OPTION:
            from state.hiscores_state import HiscoresState
            self.state_manager.set_state(HiscoresState(self.game))

    def play_menu_on_click(self, option):
        if option == MenuState.ONE_PLAYER_OPTION:
            from state.play_state import PlayState
            self.state_manager.set_state(PlayState(self.game))
        elif option == MenuState.TWO_PLAYERS_OPTION:
            from state.play_state import PlayState
            self.state_manager.set_state(PlayState(self.game))
        elif option == MenuState.BACK_OPTION:
            self.change_menu_options(self.main_menu_options)

    def dispose(self):
        pass


class MenuOptions:
    def __init__(self, options, on_click):
        self.menu_options = options
        self.on_click = on_click
        self.selected = 0
        self.menu_options_surfaces = []

        self.reset()

    def init(self, font, font_size):
        font_renderer = pygame.font.Font(font, font_size)
        self.menu_options_surfaces = [font_renderer.render(option, True, NOT_SO_BLACK) for option in self.menu_options]

    def update(self, input_handler):
        if input_handler.key_clicked(pygame.K_DOWN):
            self.selected = (self.selected + 1) % len(self.menu_options)
        if input_handler.key_clicked(pygame.K_UP):
            self.selected = (self.selected - 1) % len(self.menu_options)
        if input_handler.key_clicked(pygame.K_RETURN):
            self.on_click(self.selected)

    def render(self, canvas):
        for i in range(len(self.menu_options_surfaces)):
            option_surface = self.menu_options_surfaces[i]
            surface_x = GAME_WIDTH / 2 - option_surface.get_width() / 2
            surface_y = i * option_surface.get_height() * 1.8 + GAME_HEIGHT / 4 * 2.2
            canvas.blit(option_surface, (surface_x, surface_y))
            # Draw arrow
            if self.selected == i:
                points = self.arrow_points(surface_x - 20, surface_y + 2, 10, 10)
                pygame.draw.polygon(canvas, NOT_SO_BLACK, points)

    def arrow_points(self, x, y, width, height):
        return (x, y), (x, y + height), (x + width, y + (height / 2))

    def reset(self):
        self.selected = 0
