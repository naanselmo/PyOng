from abc import ABCMeta, abstractmethod


class GameState(object):
    __metaclass__ = ABCMeta

    def __init__(self, game):
        self.input = game.input
        self.state_manager = game.state_manager

    @abstractmethod
    def show(self):
        pass

    @abstractmethod
    def render(self, canvas):
        pass

    @abstractmethod
    def update(self, delta):
        pass

    @abstractmethod
    def dispose(self):
        pass


class GameStateManager:
    def __init__(self):
        self.game_state = None

    def set_state(self, game_state):
        if self.game_state is not None:
            self.game_state.dispose()
        self.game_state = game_state
        if self.game_state is not None:
            self.game_state.show()

    def render(self, canvas):
        if self.game_state is not None:
            self.game_state.render(canvas)

    def update(self, delta):
        if self.game_state is not None:
            self.game_state.update(delta)
