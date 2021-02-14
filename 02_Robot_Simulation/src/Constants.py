import numpy as np

environment_speed = 0.1

padding = 10
padding_top = 100

width = 1000
height = 700

# start_x = width / 2 + 150
# start_y = height / 2
#
# start_rot = 180

# start_x = 213
# start_y = 143
#
# start_rot = 283
start_x = 300
start_y = 250

start_rot = 283

start_pos = np.array([start_x, start_y], dtype=float).reshape((2, 1))


robot_radius = 100
robot_velocity_steps = 0.1

epsilon = 0.00001

colors = dict(
    black=(0, 0, 0),
    robot=(0, 128, 255),
    green=(0, 255, 128),
    white=(255, 255, 255),
    yellow=(255, 255, 0),
    pink=(255, 192, 203),
    red=(255, 99, 71)
)