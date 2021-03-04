import numpy as np

# This was done by everyone piece by piece

# ENVIRONMENT

"""
Author Frederic Abraham, Guillaume Franzoni Darnois & Theodoros Giannilias
"""

ENVIRONMENT_SPEED = 0.1  # Frederic fill this please
PADDING = 20  # Right, Left and Bottom padding
PADDING_TOP = 100  # Top padding to make space for data
# WIDTH = 1920  # Width of window
# HEIGHT = 1080  # Height of window

WIDTH = 800  # Width of window
HEIGHT = 500  # Height of window

EPSILON = 0.00001  # Workaround for floats with weird values

ORIGIN = [PADDING, PADDING_TOP]
MAP_WIDTH = WIDTH - 2 * PADDING
MAP_HEIGHT = HEIGHT - PADDING_TOP - PADDING

# ROBOT
START_X = 300  # Start X
START_Y = 250  # Start y
START_ROT = 0  # Starting rotation wrt to x-axis
START_POS = [START_X, START_Y]  # Starting position of Robot
NUMBER_OF_SENSORS = 12  # Number of sensor for Robot
ROBOT_RADIUS = 30  # Radius of the robot
ROBOT_VELOCITY_STEPS = 0.1  # Maximum increment of velocity per wheel
SENSOR_MAX_LENGTH = 200  # The maximum length of the sensor reading

# VISUALIZATION
COLORS = dict(  # Colors usable in application
    black=(0, 0, 0),
    robot=(0, 128, 255),
    green=(0, 255, 128),
    white=(255, 255, 255),
    yellow=(255, 255, 0),
    pink=(255, 192, 203),
    red=(255, 99, 71)
)
FPS = 144

# Decoder NN
HIDDEN_SIZE = 4
INPUT_SIZE = NUMBER_OF_SENSORS + HIDDEN_SIZE
OUTPUT_SIZE = 2
INPUT_WEIGHTS_SIZE = INPUT_SIZE * HIDDEN_SIZE
HIDDEN_WEIGHTS_SIZE = HIDDEN_SIZE * OUTPUT_SIZE

DENSITY = 20

# EVOLUTIONARY ALGORITHM
LIFE_STEPS = 10
LIFE_UPDATE = 1

N_INDIVIDUALS = 20
CROSSOVER_MUTATION_PERCENTAGE = 0.5
SELECT_PERCENTAGE = 0.4
ELITISM_PERCENTAGE = 0.1

MUTATION_PROBABILITY = 0.08

GENOME_LENGTH = INPUT_WEIGHTS_SIZE + HIDDEN_WEIGHTS_SIZE  # Number of sensors * Number of components of the velocity
GENOME_BOUNDS = 10
INIT_SIZE = 0.1
N_GENERATION = 2
GRAPH_WINDOW = -1
DRAW = False
