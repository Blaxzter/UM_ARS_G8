import numpy as np
import pygame
import Constants as Const
from src.MathUtils import rotate
from pygame import gfxdraw

dt = 1


class Robot:
    def __init__(self, init_pos: np.ndarray):
        self.v_l = 0
        self.v_r = 0
        self.l = Const.robot_radius * 2
        self.pos: np.ndarray = init_pos

        self.theta = 0

    def update(self, environment):
        # TODO do collision checks here?
        if self.v_r - self.v_l == 0:
            default_vec = np.array([self.v_r, 0]).reshape((2, 1))
            rotated = rotate(default_vec, self.theta)
            d_position = self.pos + rotated
        else:
            R = (self.l / 2) * ((self.v_l + self.v_r) / (self.v_r - self.v_l))
            w = (self.v_r - self.v_l) / self.l

            icc = self.pos - R * np.array([np.sin(self.theta), np.cos(self.theta)]).reshape((2, 1))

            x, y = self.get_x_y(self.pos)
            icc_x, icc_y = self.get_x_y(icc)
            next_pos = np.matrix([[np.cos(w * dt),  np.sin(w * dt), 0],
                                  [-np.sin(w * dt), np.cos(w * dt), 0],
                                  [0,               0,              1]]) \
                       * np.array([x - icc_x, y - icc_y, self.theta]).reshape((3, 1)) \
                       + np.array([icc_x, icc_y, w * dt]).reshape((3, 1))

            d_position = next_pos[:2]
            self.theta = next_pos[2, 0]

        if len(environment.collides(d_position)) > 0:
            # TODO: check if velocity perpendicular to collision line, if not move robot by parallel velocity component
            return
        else:
            self.pos = d_position

    def draw(self, s):
        s_x, s_y = self.get_x_y(self.pos)
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

    def get_x_y(self, vec):
        return vec[0, 0], vec[1, 0]

    def get_orientation_vector(self):
        default_vec = np.array([Const.robot_radius, 0]).reshape((2, 1))
        rotated = rotate(default_vec, self.theta)
        vec = self.pos + rotated
        return vec[0, 0], vec[1, 0]

    def stop(self):
        self.v_l = 0
        self.v_r = 0

    def increase_both(self):
        self.v_l += Const.robot_velocity_steps
        self.v_r += Const.robot_velocity_steps

    def decrease_both(self):
        self.v_l -= Const.robot_velocity_steps
        self.v_r -= Const.robot_velocity_steps

    def rotate_left(self):
        self.theta += 0.1

    def rotate_right(self):
        self.theta -= 0.1

    def increase_left(self):
        self.v_l += Const.robot_velocity_steps
        self.v_l = np.round(self.v_l, decimals=3)

    def decrease_left(self):
        self.v_l -= Const.robot_velocity_steps
        self.v_l = np.round(self.v_l, decimals=3)

    def increase_right(self):
        self.v_r += Const.robot_velocity_steps
        self.v_r = np.round(self.v_r, decimals=3)

    def decrease_right(self):
        self.v_r -= Const.robot_velocity_steps
        self.v_r = np.round(self.v_r, decimals=3)
