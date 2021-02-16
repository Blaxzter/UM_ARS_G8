import numpy as np
import pygame

environment_speed = 0.1

padding = 20
padding_top = 100

width = 1100
height = 700

start_x = 300
start_y = 250

start_rot = 270

start_pos = np.array([start_x, start_y], dtype=float).reshape((2, 1))

number_of_sensors = 12


robot_radius = 30
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

pygame.init()
font = pygame.font.SysFont(None, 24)
font_sensor = pygame.font.SysFont(None, 18)