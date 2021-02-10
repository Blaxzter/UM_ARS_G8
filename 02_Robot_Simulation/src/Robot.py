from typing import List

import numpy as np
import pygame
import Constants as Const
from src.Line import Line
from src.MathUtils import rotate, distance_point_to_line, angle_between_lines
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
        if self.v_r == 0 and self.v_l == 0:
            return
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
            next_pos = np.matrix([[np.cos(w * dt), np.sin(w * dt), 0],
                                  [-np.sin(w * dt), np.cos(w * dt), 0],
                                  [0, 0, 1]]) \
                       * np.array([x - icc_x, y - icc_y, self.theta]).reshape((3, 1)) \
                       + np.array([icc_x, icc_y, w * dt]).reshape((3, 1))

            d_position = next_pos[:2]
            self.theta = next_pos[2, 0] % (2 * np.pi)

        self.pos = self.pos + self.check_collisions(environment, d_position - self.pos)

    def check_collisions(self, environment, vec) -> np.ndarray:
        collisions = environment.collides(self.pos, self.pos + vec)
        if len(collisions) == 0 or self.get_x_y(vec) == (0, 0):
            return vec
        else:
            vec = self.recalc_next_pos(vec, self.closest_collision(collisions))
            new_collisions = environment.collides(self.pos, self.pos + vec)
            if len(new_collisions) == 0:
                return vec
            else:
                return self.check_collisions(environment, vec)

    def recalc_next_pos(self, vec: np.ndarray, line: Line) -> np.ndarray:
        pos_x, pos_y = self.get_x_y(self.pos)
        vec_x, vec_y = self.get_x_y(vec)
        vec_angle = (pos_y - (pos_y + vec_y)) / (pos_x - (pos_x + vec_x)) if (pos_x - (pos_x + vec_x)) != 0 else np.inf
        alpha = angle_between_lines(vec_angle, line.angle)
        parallel_component = np.cos(alpha) * np.linalg.norm(vec)
        perpendicular_component = distance_point_to_line(self.pos, line) - Const.robot_radius
        return rotate(np.array([parallel_component, perpendicular_component], dtype=float).reshape((2, 1)), alpha)


    def closest_collision(self, collisions: List[Line]) -> Line:
        min = np.inf
        closest = None

        for collision in collisions:
            dist = distance_point_to_line(self.pos, collision)
            if dist <= min:
                min = dist
                closest = collision
        return closest


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
        self.v_l = np.round(self.v_l, decimals=3)
        self.v_r = np.round(self.v_r, decimals=3)

    def decrease_both(self):
        self.v_l -= Const.robot_velocity_steps
        self.v_r -= Const.robot_velocity_steps
        self.v_l = np.round(self.v_l, decimals=3)
        self.v_r = np.round(self.v_r, decimals=3)

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
