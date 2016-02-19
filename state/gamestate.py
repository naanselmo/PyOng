from abc import ABCMeta, abstractmethod


class GameState(object):
    __metaclass__ = ABCMeta

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
    game_state = None

    def setState(self, game_state):
        if (self.game_state != None):
            self.game_state.dispose()
        self.game_state = game_state
        if (self.game_state != None):
            self.game_state.show()

    def render(self, canvas):
        if (self.game_state != None):
            self.game_state.render(canvas)

    def update(self, delta):
        if (self.game_state != None):
            self.game_state.update(delta)
