from pygame.mixer import Sound

import resources

from constants import *
from core.menu import VerticalMenuOptions
from state.game_state import GameState


class MenuState(GameState):
    PLAY_OPTION = 0
    HISCORES_OPTION = 1
    EXIT_OPTION = 2

    ONE_PLAYER_OPTION = 0
    TWO_PLAYERS_OPTION = 1
    BACK_OPTION = 2

    KONAMI_CODE = (pygame.K_UP, pygame.K_UP, pygame.K_DOWN, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,
                   pygame.K_LEFT, pygame.K_RIGHT, pygame.K_b, pygame.K_a)

    def __init__(self, game):
        super(MenuState, self).__init__(game)
        # Listen to up, down, and enter and all of the Konami code ones
        self.set_listen_keys((pygame.K_DOWN, pygame.K_UP, pygame.K_RETURN) + MenuState.KONAMI_CODE)

        # Konami code step
        self.konami_code_step = 0

        # Model of the menu
        self.title = GAME_TITLE
        self.selected = 0
        self.hiscore = str(self.game.hiscores.get_hiscore().name) + " - " + str(self.game.hiscores.get_hiscore().score)
        self.rights = u'\u00a9 Dezassete'
        self.current_menu_options = None
        self.main_menu_options = VerticalMenuOptions(
            ['Play', 'Hi-scores', 'Exit'],
            self.main_menu_on_click,
            self.on_change
        )
        self.play_menu_options = VerticalMenuOptions(
            ['1 Player', '2 Players', 'Back'],
            self.play_menu_on_click,
            self.on_change
        )

        # Surfaces
        self.hiscore_surface = None
        self.hiscore_label_surface = None
        self.title_surface = None
        self.rights_surface = None

        # Sounds
        self.select_sound = None

    def set_listen_keys(self, listen_keys_tuple):
        listen_keys_list = []
        for key in listen_keys_tuple:
            if key not in listen_keys_list:
                listen_keys_list.append(key)
        self.listen_keys = tuple(listen_keys_list)

    def show(self):
        # Start the music
        pygame.mixer.music.load(resources.get_music('whatislove.ogg'))
        pygame.mixer.music.play(-1)

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
        self.play_menu_options.init(font, 15, True, NOT_SO_BLACK)
        self.main_menu_options.init(font, 15, True, NOT_SO_BLACK)
        self.change_menu_options(self.main_menu_options)

        # Load all sounds
        self.select_sound = Sound(resources.get_sound('menu_select.wav'))

    def update(self, delta):
        # Konami code listener
        for key in self.listen_keys:
            if self.input.key_clicked(key):
                if MenuState.KONAMI_CODE[self.konami_code_step] == key:
                    self.konami_code_step += 1
                    if self.konami_code_step >= len(MenuState.KONAMI_CODE):
                        from state.god_state import GodState
                        self.state_manager.push_overlay(GodState(self.game))
                        self.konami_code_step = 0
                        return
                else:
                    self.konami_code_step = 0

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

        # Render the current options in the middle of the screen
        self.current_menu_options.render(canvas, GAME_WIDTH / 2, GAME_HEIGHT / 4 * 2.2)

        # Draw rights
        canvas.blit(self.rights_surface, (
            GAME_WIDTH / 2 - self.rights_surface.get_width() / 2,
            GAME_HEIGHT - self.rights_surface.get_height() - 15
        ))

    def change_menu_options(self, menu_options):
        self.current_menu_options = menu_options
        self.current_menu_options.reset()

    def main_menu_on_click(self, option):
        self.select_sound.play()
        if option == MenuState.EXIT_OPTION:
            self.game.stop()
        elif option == MenuState.PLAY_OPTION:
            self.change_menu_options(self.play_menu_options)
        elif option == MenuState.HISCORES_OPTION:
            from state.hiscores_state import HiscoresState
            self.state_manager.push_overlay(HiscoresState(self.game))

    def play_menu_on_click(self, option):
        self.select_sound.play()
        if option == MenuState.ONE_PLAYER_OPTION:
            from state.singleplayer_state import SinglePlayerState
            self.state_manager.set_state(SinglePlayerState(self.game))
        elif option == MenuState.TWO_PLAYERS_OPTION:
            from state.multiplayer_state import MultiPlayerState
            self.state_manager.set_state(MultiPlayerState(self.game))
        elif option == MenuState.BACK_OPTION:
            self.change_menu_options(self.main_menu_options)

    def on_change(self, old_option, new_option):
        self.select_sound.play()

    def dispose(self):
        pygame.mixer.music.stop()
