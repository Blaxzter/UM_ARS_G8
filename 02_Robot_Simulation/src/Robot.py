import numpy as np
import pygame
import Constatns as Const
from src.MathUtils import rotate
from pygame import gfxdraw


class Robot:
    def __init__(self, init_pos: np.ndarray):
        self.left_vel = 0
        self.right_vel = 0
        self.location: np.ndarray = init_pos

        self.theta = 45

    def update(self, environment):
        # TODO do collision checks here?

        self.location += np.array([self.left_vel, self.right_vel], dtype=float).reshape(
            (2, 1)) * Const.environment_speed
        pass

    def draw(self, s):
        s_x, s_y = self.np_pos_to_pygame_pos()
        gfxdraw.aacircle(s,
                         int(s_x),
                         int(s_y),
                         Const.robot_radius,
                         Const.colors['robot'],
                         )
        e_x, e_y = self.get_orientation_vector()
        gfxdraw.line(s,
                     int(s_x),
                     int(s_y),
                     int(e_x),
                     int(e_y),
                     Const.colors['green']
                     )

    def np_pos_to_pygame_pos(self):
        return self.location[0][0], self.location[1][0]

    def get_orientation_vector(self):
        default_vec = np.array([Const.robot_radius, 0]).reshape((2, 1))
        rotated = rotate(default_vec, self.theta)
        vec = self.location + rotated
        return vec[0, 0], vec[1, 0]

    def stop(self):
        self.left_vel = 0
        self.right_vel = 0

    def increase_both(self):
        self.left_vel += Const.robot_velocity_steps
        self.right_vel += Const.robot_velocity_steps

    def decrease_both(self):
        self.left_vel -= Const.robot_velocity_steps
        self.right_vel -= Const.robot_velocity_steps

    def rotate_left(self):
        self.theta += 0.1

    def rotate_right(self):
        self.theta -= 0.1

    def increase_left(self):
        self.left_vel += Const.robot_velocity_steps

    def decrease_left(self):
        self.left_vel -= Const.robot_velocity_steps

    def increase_right(self):
        self.right_vel += Const.robot_velocity_steps

    def decrease_right(self):
        self.right_vel -= Const.robot_velocity_steps
