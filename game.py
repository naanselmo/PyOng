import pygame

import resources
from constants import *
from pygame.time import Clock

from hiscores import Hiscores
from state.game_state import GameStateManager
from state.menu_state import MenuState
from input_handler import InputHandler


class Game:
    def __init__(self):
        self.input = InputHandler()
        self.state_manager = GameStateManager()
        self.hiscores = Hiscores(resources.get_hiscores(HISCORES_FILENAME))
        self.clock = Clock()
        self.running = False
        self.screen = None
        self.canvas = None

    def start(self):
        # Set running to true
        self.running = True
        # Init the game
        self.init()
        # Start running the game loop
        self.loop()

    def stop(self):
        # Set running to false
        self.running = False

    def init(self):
        # Init pygame
        pygame.init()
        pygame.display.set_caption(GAME_TITLE)
        # Set screen size
        self.screen = pygame.display.set_mode((GAME_WIDTH * GAME_SCALE, GAME_HEIGHT * GAME_SCALE), pygame.DOUBLEBUF)
        # Set canvas size
        self.canvas = pygame.Surface((GAME_WIDTH, GAME_HEIGHT)).convert()
        # Init the Input handler
        self.input.init()
        # Change to play state
        self.state_manager.set_state(MenuState(self))

    def loop(self):
        while self.running:
            # Let the clock do the math
            delta = self.clock.tick(GAME_MAX_FPS)

            # Catch events
            self.input.catch_events()

            # Update game
            self.update(delta)

            # Render game
            self.render()

            pygame.display.set_caption('FPS: '+str(self.clock.get_fps()))

        # Quit pygame
        pygame.quit()

    def update(self, delta):
        # Update input handler
        self.input.update()

        # Quit game if close is clicked
        if self.input.quit:
            self.stop()

        # Update the game with delta given from clock
        self.state_manager.update(delta)

    def render(self):
        # Clear screen
        self.canvas.fill((255, 255, 255))

        # Render game state manager on canvas
        self.state_manager.render(self.canvas)

        # Scale the canvas to the screen
        scale_canvas = pygame.transform.scale(self.canvas, (self.screen.get_size()))
        # Blit canvas to screen
        self.screen.blit(scale_canvas, (0, 0))
        # Render screen
        pygame.display.flip()


def main():
    # Start new game
    Game().start()


if __name__ == '__main__':
    main()
