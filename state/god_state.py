import resources
from constants import *
from core.menu import MenuSlider, MenuOptions
from state.game_state import GameState


class GodState(GameState):
    def __init__(self, game):
        super(GodState, self).__init__(game)
        self.listen_keys = (pygame.K_ESCAPE, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RETURN)

        # Model of the state
        self.slider = MenuSlider(300, 500, 700)
        self.slider2 = MenuSlider(400, 600, 800)
        self.options = MenuOptions(['Back', 'Kappa'], self.on_click, self.on_change, True, False)
        self.menu = Menu([self.slider, self.slider2, self.options])

    def show(self):
        # Start the music and loop it forever
        pygame.mixer.music.load(resources.get_music('anthem.wav'))
        pygame.mixer.music.play(-1)

        # Init all sliders
        self.slider.init(300, 7, NOT_SO_WHITE, NOT_SO_WHITE)
        self.slider2.init(300, 7, NOT_SO_WHITE, NOT_SO_WHITE)
        font = resources.get_font('prstartcustom.otf')
        self.options.init(font, 15, True, NOT_SO_WHITE)

    def update(self, delta):
        if self.input.key_clicked(pygame.K_ESCAPE):
            self.state_manager.pop_overlay()

        self.slider.update(self.input, delta)
        self.slider2.update(self.input, delta)
        self.options.update(self.input)
        self.menu.update(self.input, delta)

    def render(self, canvas):
        canvas.fill(NOT_SO_BLACK)

        self.slider.render(canvas, GAME_WIDTH / 2, 100)
        self.slider2.render(canvas, GAME_WIDTH / 2, 200)
        self.options.render(canvas, GAME_WIDTH / 6 * 5, GAME_HEIGHT - 20)

    def on_change(self, old_option, new_option):
        if old_option == new_option == 1:
            self.menu.move_up()
        # print old_option, new_option
        pass

    def on_click(self, option):
        self.state_manager.pop_overlay()

    def dispose(self):
        pygame.mixer.music.stop()


class Menu:
    DISABLE_UPDATE = [MenuOptions]

    def __init__(self, components):
        self.active_component = 0
        self.components = [] + components
        for component in components:
            component.active = False
        self.components[0].active = True

    def update(self, input_handler, delta):
        for disable_class in Menu.DISABLE_UPDATE:
            if isinstance(self.components[self.active_component], disable_class):
                return

        if input_handler.key_clicked(pygame.K_UP):
            self.move_up()
        if input_handler.key_clicked(pygame.K_DOWN):
            self.move_down()

    def move_up(self):
        if self.active_component != 0:
            self.components[self.active_component].active = False
            self.active_component -= 1
            self.components[self.active_component].active = True
        print self.active_component

    def move_down(self):
        if self.active_component != len(self.components) - 1:
            self.components[self.active_component].active = False
            self.active_component += 1
            self.components[self.active_component].active = True
