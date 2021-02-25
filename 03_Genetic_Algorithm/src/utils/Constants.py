import numpy as np

# This was done by everyone piece by piece


# ENVIRONMENT
ENVIRONMENT_SPEED = 0.1  # Frederic fill this please
PADDING = 20  # Right, Left and Bottom padding
PADDING_TOP = 100  # Top padding to make space for data
# WIDTH = 1920  # Width of window
# HEIGHT = 1080  # Height of window

WIDTH = 800  # Width of window
HEIGHT = 500  # Height of window

EPSILON = 0.00001  # Workaround for floats with weird values

# ROBOT
START_X = 300  # Start X
START_Y = 250  # Start y
START_ROT = 0  # Starting rotation wrt to x-axis
START_POS = np.array([START_X, START_Y], dtype=float).reshape((2, 1))  # Starting position of Robot
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

# EVOLUTIONARY ALGORITHM
LIFE_STEPS = 200
LIFE_UPDATE = 1

N_INDIVIDUALS = 10
SELECT_AMOUNT = 4
ELITISM_AMOUNT = 2

GENOME_LENGTH = 20
N_GENERATION = 100
DRAW = False