import numpy as np

environment_speed = 0.1

padding = 10
padding_top = 100

width = 400
height = 400

start_x = width / 2 + 150
start_y = height / 2

start_pos = np.array([start_x, start_y], dtype=float).reshape((2, 1))

robot_radius = 30
robot_velocity_steps = 0.1

colors = dict(
    black=(0, 0, 0),
    robot=(0, 128, 255),
    green=(0, 255, 128),
    white=(255, 255, 255),
)