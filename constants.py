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

# Pad
PAD_HEIGHT = 80
PAD_WIDTH = 10
PAD_SPEED = 0.2
PAD_DISTANCE = 10

# Ball
BALL_HEIGHT = 5
BALL_WIDTH = 5
BALL_MIN_START_SPEED = 0.1
BALL_MAX_START_SPEED = 0.3
BALL_SPEED_MULTIPLIER = 1.1
BALL_SPEED_LIMIT = 1
BALL_SPEED_TRANSFER = 0.5
BALL_SPEED_TRANSFER_DASH = 0.8
