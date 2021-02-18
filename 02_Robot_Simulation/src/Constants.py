import numpy as np
import pygame

# ENVIRONMENT
ENVIRONMENT_SPEED = 0.1
PADDING = 20
PADDING_TOP = 100
WIDTH = 1100
HEIGHT = 700
EPSILON = 0.00001

# ROBOT
START_X = 300
START_Y = 250
START_ROT = 270
START_POS = np.array([START_X, START_Y], dtype=float).reshape((2, 1))
NUMBER_OF_SENSORS = 12
ROBOT_RADIUS = 30
ROBOT_VELOCITY_STEPS = 0.1

# VISUALIZATION
pygame.init()
FONT = pygame.font.SysFont(None, 24)
FONT_SENSORS = pygame.font.SysFont(None, 18)
COLORS = dict(
    black=(0, 0, 0),
    robot=(0, 128, 255),
    green=(0, 255, 128),
    white=(255, 255, 255),
    yellow=(255, 255, 0),
    pink=(255, 192, 203),
    red=(255, 99, 71)
)
