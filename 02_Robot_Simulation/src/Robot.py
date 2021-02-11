from typing import List, Dict

import numpy as np
import pygame
import Constants as Const
from src.Line import Line
from src.MathUtils import rotate, distance_point_to_line, angle_between_lines, angle_between, line_intersection, \
    intersection, math_line, rotate_deg, side_of_point
from pygame import gfxdraw

import traceback


dt = 1


class Robot:
    def __init__(self, init_pos: np.ndarray):
        self.v_l = 0
        self.v_r = 0
        self.l = Const.robot_radius * 2
        self.pos: np.ndarray = init_pos

        self.theta = np.deg2rad(Const.start_rot)

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

        self.pos = self.check_collisions(environment, self.pos, d_position)

    def check_collisions(self, environment, current_pos: np.ndarray, next_pos: np.ndarray) -> np.ndarray:
        collisions = environment.collides(current_pos, next_pos)
        if len(collisions) == 0 or self.get_x_y(next_pos) == (0, 0):
            return next_pos
        else:
            closest_line = self.closest_collision(collisions, current_pos)
            t_current_pos, t_next_pos = self.recalc_next_pos(current_pos, next_pos, closest_line)
            new_collisions = environment.collides(t_current_pos, t_next_pos)
            if len(new_collisions) == 0:
                return t_next_pos
            else:
                return self.check_collisions(environment, t_current_pos, t_next_pos)

    def recalc_next_pos(self, current_pos: np.ndarray, next_pos: np.ndarray, collisions: Dict) -> (np.ndarray, np.ndarray):
        pos_x, pos_y = self.get_x_y(current_pos)
        npos_x, npos_y = self.get_x_y(next_pos)
        vec = next_pos - current_pos
        comp_line = collisions['line']

        vec_norm = np.linalg.norm(vec)
        if vec_norm == 0 or np.dot(comp_line.vec.T, vec) == 0:
            return current_pos, collisions['intersect'] + (vec / vec_norm) * Const.robot_radius * - 1

        # Get on the line
        vec_towards_robot = (rotate_deg(comp_line.nvec, 90) * -1
                             if side_of_point(comp_line.start, comp_line.end, self.pos)
                             else rotate_deg(comp_line.nvec, 90)) * Const.robot_radius

        new_line_start = comp_line.start + vec_towards_robot
        new_line_end = comp_line.end + vec_towards_robot
        pos_on_line = np.array(line_intersection(
            ([pos_x, pos_y], [npos_x, npos_y]),
            ([new_line_start[0], new_line_start[1]],
             [new_line_end[0], new_line_end[1]])
        )).reshape((2, 1))

        # t_pos_on_line = np.array(line_intersection(
        #     ([pos_x, pos_y], [npos_x, npos_y]),
        #     ([comp_line.start[0], comp_line.start[1]], [comp_line.end[0], comp_line.end[1]])
        # )).reshape((2, 1))
        # pos_on_line = t_pos_on_line + (vec * -1 / np.linalg.norm(vec)) * Const.robot_radius

        remaining_length = (np.linalg.norm(vec) - np.linalg.norm(pos_on_line - self.pos)) * abs(np.cos(angle_between(vec, comp_line.vec)))
        parallel_vector = comp_line.nvec if np.dot(comp_line.vec.T, vec) > 0 else comp_line.nvec * -1
        new_next_pos = pos_on_line + parallel_vector * remaining_length

        return pos_on_line, new_next_pos

        # pos_x, pos_y = self.get_x_y(self.pos)
        # vec_x, vec_y = self.get_x_y(vec)
        # vec_angle = (pos_y - (pos_y + vec_y)) / (pos_x - (pos_x + vec_x)) if (pos_x - (pos_x + vec_x)) != 0 else np.inf
        # alpha = angle_between(vec, line.vec)
        # parallel_component = np.cos(alpha) * np.linalg.norm(vec)
        # perpendicular_component = distance_point_to_line(self.pos, line)[0,0] - Const.robot_radius
        # return np.array([parallel_component, perpendicular_component]).reshape((2, 1))
        # perpendicular_component = distance_point_to_line(self.pos, line) - Const.robot_radius
        # return rotate(np.array([parallel_component, perpendicular_component], dtype=float).reshape((2, 1)), alpha)

    def closest_collision(self, collisions: List[Dict], position) -> Dict:
        min = np.inf
        closest = None

        for collision in collisions:
            dist = distance_point_to_line(position, collision['line'])
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
        if vec is None or vec[0] is None:
            print("test")
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
        self.theta += np.deg2rad(1)
        self.theta = self.theta % (2 * np.pi)

    def rotate_right(self):
        self.theta -= np.deg2rad(1)
        self.theta = self.theta % (2 * np.pi)

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


if __name__ == '__main__':
    robot = Robot(init_pos=np.array([0, 0]).reshape((2, 1)))
    next_pos = np.array([2, 2]).reshape((2, 1))

    vec = next_pos - robot.pos

    line = Line(start=np.array([1, 0]).reshape((2, 1)), end=np.array([1, 2]).reshape((2, 1)))
    robot.recalc_next_pos(next_pos, line)
