import numpy as np
import pygame

# ENVIRONMENT
ENVIRONMENT_SPEED = 0.1                                                 # Frederic fill this please
PADDING = 20                                                            # Right, Left and Bottom padding
PADDING_TOP = 100                                                       # Top padding to make space for data
WIDTH = 1100                                                            # Width of window
HEIGHT = 700                                                            # Height of window
EPSILON = 0.00001                                                       # Workaround for floats with weird values

# ROBOT
START_X = 300                                                           # Start X
START_Y = 250                                                           # Start y
START_ROT = 270                                                         # Starting rotation wrt to x-axis
START_POS = np.array([START_X, START_Y], dtype=float).reshape((2, 1))   # Starting position of Robot
NUMBER_OF_SENSORS = 12                                                  # Number of sensor for Robot
ROBOT_RADIUS = 30                                                       # Radius of the robot
ROBOT_VELOCITY_STEPS = 0.1                                              # Maximum increment of velocity per wheel

# VISUALIZATION
pygame.init()
FONT = pygame.font.SysFont(None, 24)                                    # Font used for data visualization on top
FONT_SENSORS = pygame.font.SysFont(None, 18)                            # Font to display distance of sensor from wall
COLORS = dict(                                                          # Colors usable in application
    black=(0, 0, 0),
    robot=(0, 128, 255),
    green=(0, 255, 128),
    white=(255, 255, 255),
    yellow=(255, 255, 0),
    pink=(255, 192, 203),
    red=(255, 99, 71)
)
