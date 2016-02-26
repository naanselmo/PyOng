import pygame

import resources
from constants import *
from pygame.time import Clock

from hiscores import Hiscores
from state.game_state import GameStateManager
from state.menu_state import MenuState
from input_handler import InputHandler
from threading import Thread

class Game:
    def __init__(self):
        self.input = InputHandler()
        self.state_manager = GameStateManager()
        self.hiscores = Hiscores(resources.get_hiscores(HISCORES_FILENAME))
        self.logic_clock = Clock()
        self.render_clock = Clock()
        self.renderer = Thread(target=self.render_loop, args=())
        self.renderer.daemon = True
        self.rendering = True
        self.running = False
        self.screen = None
        self.canvas = None

    def start(self):
        # Set running to true
        self.running = True
        # Init the game
        self.init()
        # Start the renderer
        self.renderer.start()
        # Start running the game loop
        self.logic_loop()

    def stop(self):
        # Set running to false
        self.running = False

    def init(self):
        # Init mixer for sound specifications
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
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

    def render_loop(self):
        while self.running:
            # Tick the clock
            self.render_clock.tick(GAME_MAX_FPS)

            # Render game
            if self.rendering:
                self.render()

    def logic_loop(self):
        while self.running:
            # Let the clock do the math
            delta = self.logic_clock.tick(1000)
            print self.logic_clock.get_rawtime()

            # Catch events
            self.input.catch_events()

            # Update game
            self.update(delta)

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
