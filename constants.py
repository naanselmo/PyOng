import pygame

# Game configuration
GAME_WIDTH = 640
GAME_HEIGHT = 360
GAME_TITLE = 'PyOng'
GAME_SCALE = 2
GAME_MAX_FPS = 144

HISCORES_FILENAME = 'hiscores'

# Colors
NOT_SO_WHITE = (244, 241, 221)
NOT_SO_BLACK = (5, 5, 5)

# Controls
PLAYER1 = {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'dash': pygame.K_LEFT}
PLAYER2 = {'up': pygame.K_w, 'down': pygame.K_s, 'dash': pygame.K_d}
