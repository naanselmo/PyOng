from pygame.mixer import Sound

import resources
from constants import *
from core.menu import VerticalMenuOptions
from state.game_state import GameState
from state.menu_state import MenuState


class PauseState(GameState):
    CONTINUE_OPTION = 0
    RESTART_OPTION = 1
    EXIT_OPTION = 2

    def __init__(self, game, restart_state):
        super(PauseState, self).__init__(game)
        self.listen_keys = (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RETURN)

        self.restart_state = restart_state
        self.options = VerticalMenuOptions(
            ['Continue', 'Restart', 'Exit'],
            self.on_click,
            self.on_change,
        )

        self.select_sound = None

    def show(self):
        # Initialize options
        font = resources.get_font('prstartcustom.otf')
        self.options.init(font, 15, True, MORE_WHITE)

        # Initialize sounds
        self.select_sound = Sound(resources.get_sound('menu_select.wav'))

    def update(self, delta):
        self.options.update(self.input)

    def render(self, canvas):
        canvas.fill(NOT_SO_BLACK)
        self.options.render(canvas, GAME_WIDTH / 2, GAME_HEIGHT / 2 - self.options.get_height() / 2)

    def on_click(self, option):
        self.select_sound.play()
        if option == PauseState.CONTINUE_OPTION:
            self.state_manager.pop_overlay()
        elif option == PauseState.RESTART_OPTION:
            self.state_manager.set_state(self.restart_state)
        elif option == PauseState.EXIT_OPTION:
            self.state_manager.set_state(MenuState(self.game))

    def on_change(self, old_option, new_option):
        self.select_sound.play()

    def dispose(self):
        pass
