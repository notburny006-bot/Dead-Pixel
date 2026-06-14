"""Game-wide constants. Single source of truth for sizes, speeds, etc."""

# Entity sizes
PLAYER_SIZE = 48
ENEMY_SIZE = 40
BULLET_SIZE = (8, 16)

# Player
PLAYER_SPEED = 300.0  # pixels per second
PLAYER_START_Y_RATIO = 0.1  # 10% from bottom, scales to any screen
TOUCH_SENSITIVITY = 0.8  # 1.0 = raw, <1 = smoothed
