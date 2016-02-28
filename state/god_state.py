from abc import abstractmethod, ABCMeta

import resources
from constants import *
from core.menu import MenuSlider, VerticalMenuOptions, HorizontalMenuOptions
from state.game_state import GameState


class GodState(GameState):
    def __init__(self, game):
        super(GodState, self).__init__(game)
        self.listen_keys = (pygame.K_ESCAPE, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RETURN)

        # Model of the state
        self.menu = MainMenu(self)

    def show(self):
        # Start the music and loop it forever
        pygame.mixer.music.load(resources.get_music('anthem.wav'))
        pygame.mixer.music.play(-1)

        self.menu.init()

    def update(self, delta):
        self.menu.update(self.input, delta)

    def render(self, canvas):
        canvas.fill(NOT_SO_BLACK)
        self.menu.render(canvas)

    def set_menu(self, menu):
        with self.game.rendering:
            if self.menu is not None:
                self.menu.dispose()
            self.menu = menu
            if self.menu is not None:
                self.menu.init()

    def dispose(self):
        pygame.mixer.music.stop()


class Menu:
    __metaclass__ = ABCMeta

    def __init__(self, components, state):
        self.state_manager = state.state_manager
        self.state = state

        self.active_component = 0
        self.components = components
        for component in components:
            component.active = False
        self.components[self.active_component].active = True
        self.disable_update = [VerticalMenuOptions]

    @abstractmethod
    def init(self):
        pass

    def update(self, input_handler, delta):
        # If active component is not in the disabled classes for update, update it and only update the components in
        # the next loop to consume the events
        active_component = self.components[self.active_component]
        if not any([isinstance(active_component, disable_class) for disable_class in self.disable_update]):
            if input_handler.key_clicked(pygame.K_UP):
                self.move_up()
                return
            if input_handler.key_clicked(pygame.K_DOWN):
                self.move_down()
                return

        # Update menu components
        self.update_menu(input_handler, delta)

    def move_up(self):
        if self.active_component != 0:
            self.components[self.active_component].active = False
            self.active_component -= 1
            self.components[self.active_component].active = True

    def move_down(self):
        if self.active_component != len(self.components) - 1:
            self.components[self.active_component].active = False
            self.active_component += 1
            self.components[self.active_component].active = True

    @abstractmethod
    def update_menu(self, input_handler, delta):
        pass

    @abstractmethod
    def render(self, canvas):
        pass

    @abstractmethod
    def dispose(self):
        pass


class TestMenu(Menu):
    def __init__(self, state):
        self.slider = MenuSlider(300, 500, 700)
        self.slider2 = MenuSlider(400, 600, 800)
        self.options = VerticalMenuOptions(['Back'], self.on_click, self.on_change, True, False)
        components = [self.slider, self.slider2, self.options]
        super(TestMenu, self).__init__(components, state)

    def init(self):
        self.slider.init(300, 7, NOT_SO_WHITE, NOT_SO_WHITE)
        self.slider2.init(300, 7, NOT_SO_WHITE, NOT_SO_WHITE)

        font = resources.get_font('prstartcustom.otf')
        self.options.init(font, 15, True, NOT_SO_WHITE)

    def update_menu(self, input_handler, delta):
        self.slider.update(input_handler, delta)
        self.slider2.update(input_handler, delta)
        self.options.update(input_handler)

    def render(self, canvas):
        self.slider.render(canvas, GAME_WIDTH / 2, 100)
        self.slider2.render(canvas, GAME_WIDTH / 2, 200)
        self.options.render(canvas, GAME_WIDTH / 6 * 5, GAME_HEIGHT - 20)

    def on_change(self, old_option, new_option):
        if old_option == new_option == 0:
            self.move_up()

    def on_click(self, option):
        self.state_manager.pop_overlay()

    def dispose(self):
        pass


class MainMenu(Menu):
    PAD_SETTINGS = 0
    BALL_SETTINGS = 1
    EXIT_OPTION = 2

    def __init__(self, state):
        # Model of the menu
        self.menu_options = VerticalMenuOptions(
            ['Pad Settings', 'Ball Settings', 'Exit'],
            self.on_click
        )

        # Run super __init__
        components = [self.menu_options]
        super(MainMenu, self).__init__(components, state)

    def init(self):
        font = resources.get_font('prstartcustom.otf')
        self.menu_options.init(font, 15, True, MORE_WHITE)

    def update_menu(self, input_handler, delta):
        self.menu_options.update(input_handler)

    def render(self, canvas):
        self.menu_options.render(canvas, GAME_WIDTH / 2, GAME_HEIGHT / 2 - self.menu_options.get_height() / 2)

    def on_click(self, option):
        if option == MainMenu.PAD_SETTINGS:
            self.state.set_menu(PadSettingsMenu(self.state))
        elif option == MainMenu.BALL_SETTINGS:
            self.state.set_menu(BallSettingsMenu(self.state))
        elif option == MainMenu.EXIT_OPTION:
            self.state_manager.pop_overlay()

    def dispose(self):
        pass


class PadSettingsMenu(Menu):
    APPLY_OPTION = 0
    BACK_OPTION = 1

    LABELS_SPACE = 40
    LABEL_SLIDER_SPACE = 10

    def __init__(self, state):
        self.__height = None

        # Menu components
        import constants
        self.speed_slider = MenuSlider(0, constants.PAD_SPEED, 2)
        self.height_slider = MenuSlider(30, constants.PAD_HEIGHT, GAME_HEIGHT - 30)
        self.charge_rate_slider = MenuSlider(0, constants.PAD_CHARGING_RATE, PAD_MAX_CHARGE)
        self.options = HorizontalMenuOptions(['Apply', 'Back'], self.on_click, self.on_change, True)
        components = [self.speed_slider, self.height_slider, self.charge_rate_slider, self.options]
        super(PadSettingsMenu, self).__init__(components, state)

        # Surfaces
        self.speed_label_surface = None
        self.height_label_surface = None
        self.charge_rate_surface = None

        # All slider/label pairs for easy render and updating
        self.sliders = None

    def init(self):
        font = resources.get_font('prstartcustom.otf')
        # Initialize all sliders
        self.speed_slider.init(300, 7, MORE_WHITE, MORE_WHITE)
        self.height_slider.init(300, 7, MORE_WHITE, MORE_WHITE)
        self.charge_rate_slider.init(300, 7, MORE_WHITE, MORE_WHITE)
        # Initialize back option
        self.options.init(font, 15, True, MORE_WHITE)

        # Initialize surfaces
        font_renderer = pygame.font.Font(font, 15)
        self.speed_label_surface = font_renderer.render('Speed:', True, MORE_WHITE)
        self.height_label_surface = font_renderer.render('Height:', True, MORE_WHITE)
        self.charge_rate_surface = font_renderer.render('Charging rate:', True, MORE_WHITE)

        # Update the sliders tuple
        self.sliders = (
            (self.speed_label_surface, self.speed_slider),
            (self.height_label_surface, self.height_slider),
            (self.charge_rate_surface, self.charge_rate_slider)
        )

    def update_menu(self, input_handler, delta):
        for _, slider in self.sliders:
            slider.update(input_handler, delta)
        self.options.update(input_handler)

    def render(self, canvas):
        # Render all sliders
        label_slider_space = PadSettingsMenu.LABEL_SLIDER_SPACE
        labels_space = PadSettingsMenu.LABELS_SPACE
        y = GAME_HEIGHT / 2 - self.get_height() / 1.8
        for label, slider in self.sliders:
            canvas.blit(label, (GAME_WIDTH / 2 - label.get_width() / 2, y))
            slider.render(canvas, GAME_WIDTH / 2, y + label.get_height() + label_slider_space)
            y += label.get_height() + label_slider_space + slider.bar_height + labels_space

        # Render back and apply options
        self.options.render(canvas, GAME_WIDTH * 0.80, GAME_HEIGHT - 20 - self.options.get_height())

    def get_height(self):
        if self.__height is None:
            self.__height = 0
            sliders_len = len(self.sliders)
            for i in range(sliders_len):
                label, slider = self.sliders[i]
                space = PadSettingsMenu.LABELS_SPACE if i != sliders_len - 1 else 0
                self.__height += label.get_height() + PadSettingsMenu.LABEL_SLIDER_SPACE + slider.bar_height + space
        return self.__height

    def on_change(self, old_option, new_option):
        pass

    def on_click(self, option):
        if option == PadSettingsMenu.APPLY_OPTION:
            self.save_changes()
        self.state.set_menu(MainMenu(self.state))

    def save_changes(self):
        import constants
        constants.PAD_SPEED = self.speed_slider.value
        constants.PAD_HEIGHT = self.height_slider.value
        constants.PAD_CHARGING_RATE = self.charge_rate_slider.value
        constants.VIRGINITY = False

    def dispose(self):
        pass


class BallSettingsMenu(Menu):
    APPLY_OPTION = 0
    BACK_OPTION = 1

    LABELS_SPACE = 40
    LABEL_SLIDER_SPACE = 10

    def __init__(self, state):
        self.__height = None

        # Menu components
        import constants
        self.speed_limit_slider = MenuSlider(0, constants.BALL_SPEED_LIMIT, 1)
        self.speed_multiplier_slider = MenuSlider(1, constants.BALL_SPEED_MULTIPLIER, 4)
        self.radius_slider = MenuSlider(2, constants.BALL_RADIUS, 30)
        self.options = HorizontalMenuOptions(['Apply', 'Back'], self.on_click, self.on_change, True)
        components = [self.speed_limit_slider, self.speed_multiplier_slider, self.radius_slider, self.options]
        super(BallSettingsMenu, self).__init__(components, state)

        # Surfaces
        self.speed_limit_label_surface = None
        self.speed_multiplier_label_surface = None
        self.radius_surface = None

        # All slider/label pairs for easy render and updating
        self.sliders = None

    def init(self):
        font = resources.get_font('prstartcustom.otf')
        # Initialize all sliders
        self.speed_limit_slider.init(300, 7, MORE_WHITE, MORE_WHITE)
        self.speed_multiplier_slider.init(300, 7, MORE_WHITE, MORE_WHITE)
        self.radius_slider.init(300, 7, MORE_WHITE, MORE_WHITE)
        # Initialize back option
        self.options.init(font, 15, True, MORE_WHITE)

        # Initialize surfaces
        font_renderer = pygame.font.Font(font, 15)
        self.speed_limit_label_surface = font_renderer.render('Speed limit:', True, MORE_WHITE)
        self.speed_multiplier_label_surface = font_renderer.render('Speed multiplier:', True, MORE_WHITE)
        self.radius_surface = font_renderer.render('Radius:', True, MORE_WHITE)

        # Update the sliders tuple
        self.sliders = (
            (self.speed_limit_label_surface, self.speed_limit_slider),
            (self.speed_multiplier_label_surface, self.speed_multiplier_slider),
            (self.radius_surface, self.radius_slider)
        )

    def update_menu(self, input_handler, delta):
        for _, slider in self.sliders:
            slider.update(input_handler, delta)
        self.options.update(input_handler)

    def render(self, canvas):
        # Render all sliders
        label_slider_space = BallSettingsMenu.LABEL_SLIDER_SPACE
        labels_space = BallSettingsMenu.LABELS_SPACE
        y = GAME_HEIGHT / 2 - self.get_height() / 1.8
        for label, slider in self.sliders:
            canvas.blit(label, (GAME_WIDTH / 2 - label.get_width() / 2, y))
            slider.render(canvas, GAME_WIDTH / 2, y + label.get_height() + label_slider_space)
            y += label.get_height() + label_slider_space + slider.bar_height + labels_space

        # Render back and apply options
        self.options.render(canvas, GAME_WIDTH * 0.80, GAME_HEIGHT - 20 - self.options.get_height())

    def get_height(self):
        if self.__height is None:
            self.__height = 0
            sliders_len = len(self.sliders)
            for i in range(sliders_len):
                label, slider = self.sliders[i]
                space = BallSettingsMenu.LABELS_SPACE if i != sliders_len - 1 else 0
                self.__height += label.get_height() + BallSettingsMenu.LABEL_SLIDER_SPACE + slider.bar_height + space
        return self.__height

    def on_change(self, old_option, new_option):
        pass

    def on_click(self, option):
        if option == BallSettingsMenu.APPLY_OPTION:
            self.save_changes()
        self.state.set_menu(MainMenu(self.state))

    def save_changes(self):
        import constants
        constants.BALL_SPEED_LIMIT = self.speed_limit_slider.value
        constants.BALL_SPEED_MULTIPLIER = self.speed_multiplier_slider.value
        constants.BALL_RADIUS = self.radius_slider.value
        constants.VIRGINITY = False

    def dispose(self):
        pass
