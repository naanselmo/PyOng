import pygame

from config import *
from pygame.time import Clock
from state.gamestate import GameStateManager
from state.states import PlayState
from input_handler import InputHandler


class Game:
    def __init__(self):
        self.InputHandler = InputHandler()
        self.GameStateManager = GameStateManager()
        self.Clock = Clock()
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
        # Set state to None so it clears the current state and runs it's dispose method
        self.GameStateManager.set_state(None)

    def init(self):
        # Init pygame
        pygame.init()
        pygame.display.set_caption(GAME_TITLE)
        # Set screen size
        self.screen = pygame.display.set_mode((GAME_WIDTH * GAME_SCALE, GAME_HEIGHT * GAME_SCALE), pygame.DOUBLEBUF)
        # Set canvas size
        self.canvas = pygame.Surface((GAME_WIDTH, GAME_HEIGHT)).convert()

        # Change to playstate
        self.GameStateManager.set_state(PlayState())

    def loop(self):
        while self.running:
            # Let the clock do the math
            delta = self.Clock.tick(GAME_MAX_FPS)

            # Catch events
            self.InputHandler.catch_events()

            # Update game
            self.update(delta)

            # Render game
            self.render()

            # pygame.display.set_caption('FPS: '+str(self.Clock.get_fps()))

        # Quit pygame
        pygame.quit()

    def update(self, delta):
        # Update input handler
        self.InputHandler.update()

        # Quit game if close is clicked
        if self.InputHandler.quit:
            self.stop()

        # Update the game with delta given from clock
        self.GameStateManager.update(delta)

    def render(self):
        # Clear screen
        self.canvas.fill((255, 255, 255))

        # Render game state manager on canvas
        self.GameStateManager.render(self.canvas)

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
