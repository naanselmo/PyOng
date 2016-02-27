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
        self.overlay_states = []

    def set_state(self, game_state):
        with game_state.game.rendering:
            if self.game_state is not None:
                # Clear all overlays
                while len(self.overlay_states):
                    self.pop_overlay()
                # Remove listeners and run dispose
                self.game_state.remove_listeners()
                self.game_state.dispose()

        # Set game state
        self.game_state = game_state

        if self.game_state is not None:
            # Show the new game state and add its listeners
            self.game_state.show()
            self.game_state.add_listeners()

    def push_overlay(self, overlay_state):
        # If pushed None send an exception
        if overlay_state is None:
            raise ValueError('None is not a valid overlay')

        # Remove listeners
        if len(self.overlay_states) == 0:
            if self.game_state is not None:
                self.game_state.remove_listeners()
        else:
            self.overlay_states[-1].remove_listeners()

        # Append the overlay to the list, show it and add its listeners
        self.overlay_states.append(overlay_state)
        overlay_state.show()
        overlay_state.add_listeners()

    def pop_overlay(self):
        # Pop the current overlay, remove the listeners and dispose it.
        overlay_state = self.overlay_states.pop()
        overlay_state.remove_listeners()
        overlay_state.dispose()

        if len(self.overlay_states) == 0:
            # Add the game state listeners if stack is empty
            self.game_state.add_listeners()
        else:
            # Add the previous overlay listeners
            self.overlay_states[-1].add_listeners()

    def render(self, canvas):
        # If there is no overlay to render, render game
        if len(self.overlay_states) == 0:
            if self.game_state is not None:
                self.game_state.render(canvas)
        else:
            self.overlay_states[-1].render(canvas)

    def update(self, delta):
        # If there is no overlay to update, update game
        if len(self.overlay_states) == 0:
            if self.game_state is not None:
                self.game_state.update(delta)
        else:
            self.overlay_states[-1].update(delta)
