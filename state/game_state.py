from abc import ABCMeta, abstractmethod


class GameState(object):
    __metaclass__ = ABCMeta

    def __init__(self, game):
        self.game = game
        self.input = game.input
        self.state_manager = game.state_manager
        self.hiscores = game.hiscores
        self.listen_keys = ()

    @abstractmethod
    def show(self):
        pass

    def add_listeners(self):
        for key in self.listen_keys:
            self.input.add_listener(key)

    @abstractmethod
    def render(self, canvas):
        pass

    @abstractmethod
    def update(self, delta):
        pass

    def remove_listeners(self):
        for key in self.listen_keys:
            self.input.remove_listener(key)

    @abstractmethod
    def dispose(self):
        pass


class GameStateManager:
    def __init__(self):
        self.game_state = None

    def set_state(self, game_state):
        if self.game_state is not None:
            self.game_state.remove_listeners()
            self.game_state.dispose()
        self.game_state = game_state
        if self.game_state is not None:
            self.game_state.show()
            self.game_state.add_listeners()

    def render(self, canvas):
        if self.game_state is not None:
            self.game_state.render(canvas)

    def update(self, delta):
        if self.game_state is not None:
            self.game_state.update(delta)
