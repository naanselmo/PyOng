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
MORE_WHITE = (254, 253, 253)
WINDOWS_98 = (0, 128, 128)

# Controls
PLAYER1 = {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'dash': pygame.K_LEFT}
PLAYER2 = {'up': pygame.K_w, 'down': pygame.K_s, 'dash': pygame.K_d}

# Players
PLAYER1_DASH = -1
PLAYER2_DASH = 1

# Pad
PAD_HEIGHT = 80
PAD_WIDTH = 20
PAD_SPEED = 0.35
PAD_DISTANCE = 10
PAD_DASH_DISTANCE = 50
PAD_INITIAL_CHARGE = 0
PAD_MAX_CHARGE = 50
PAD_CHARGING_RATE = 2

# Ball
BALL_RADIUS = 7
BALL_MIN_START_SPEED = 0.1
BALL_MAX_START_SPEED = 0.3
BALL_SPEED_MULTIPLIER = 1.1
BALL_SPEED_LIMIT = 0.75
BALL_SPEED_TRANSFER = 0.35
BALL_SPEED_TRANSFER_DASH = 0.8

# Math
COLLISION_INTERPOLATION = 100.0

# Powerups
POWERUP_SIZE = 20
POWERUP_TIMER = 2500
POWERUP_PROBABILITY = 1
POWERUP_MAX = 3
POWERUP_INVISIBLE_DURATION = 5000
POWERUP_INVISIBLE_COLOR = (220, 215, 195)
POWERUP_STUN_DURATION = 2500
POWERUP_STUNNED_COLOR = (100, 100, 100)
POWERUP_DAMAGE_FACTOR = 2
POWERUP_EXTEND_FACTOR = 1.5
POWERUP_SHRINK_FACTOR = 0.6
POWERUP_SIZE_RESTITUTION_RATE = 10
POWERUP_CHARGE = 15
POWERUP_MULTIPLIER = 1
POWERUP_BONUS = 100

# Game Constants
MULTIPLAYER_LIVES = 25
SINGLEPLAYER_LIVES = 1
SINGLEPLAYER_SCORE_MULTIPLIER = 1
BALL_DAMAGE = 1

# Cheating prevention
VIRGINITY = True
