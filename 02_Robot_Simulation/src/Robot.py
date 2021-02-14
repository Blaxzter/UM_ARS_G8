from typing import List, Dict

import numpy as np
from pygame import gfxdraw

import Constants as Const
from src.Line import Line
from src.MathUtils import rotate, distance_point_to_line, angle_between, line_intersection, \
    rotate_deg, side_of_point, outside_of_line, get_orientation_vector, distance_point_to_line_seg

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

        self.pos = self.check_collisions(environment, self.pos, d_position, [])

    def check_collisions(self, environment, current_pos: np.ndarray, next_pos: np.ndarray,
                         prev_collision) -> np.ndarray:
        collisions = environment.collides(current_pos, next_pos)
        if len(collisions) == 0 or self.get_x_y(next_pos) == (0, 0):
            return next_pos
        else:
            closest_line = self.closest_collision(collisions, current_pos)
            t_current_pos, t_next_pos = self.recalc_next_pos(current_pos, next_pos, closest_line)
            # if self.recalc_next_pos(current_pos, next_pos, closest_line)[1].shape == (2,2):
            #     t_current_pos, t_next_pos = self.recalc_next_pos(current_pos, next_pos, closest_line)
            new_collisions = environment.collides(t_current_pos, t_next_pos)
            prev_collision.append(closest_line['line'])
            if len(new_collisions) == 0:
                return t_next_pos
            else:
                if new_collisions[0]['line'] not in prev_collision:
                    return self.check_collisions(environment, t_current_pos, t_next_pos, prev_collision)
                else:
                    return current_pos

    def recalc_next_pos(self, current_pos: np.ndarray, next_pos: np.ndarray, collisions: Dict) -> (np.ndarray, np.ndarray):
        pos_x, pos_y = self.get_x_y(current_pos)
        npos_x, npos_y = self.get_x_y(next_pos)
        vec = next_pos - current_pos
        vec_norm = np.linalg.norm(vec)
        n_vec = vec / vec_norm
        comp_line: Line = collisions['line']

        # We are going perpendicular to the wall
        if np.abs(vec_norm) < Const.epsilon or np.abs(np.dot(comp_line.vec.T, vec)) < Const.epsilon:
            new_intersection = line_intersection(
                ([pos_x, pos_y], [npos_x, npos_y]),
                ([comp_line.start[0], comp_line.start[1]], [comp_line.end[0], comp_line.end[1]])
            )
            return current_pos, new_intersection + (vec / vec_norm) * Const.robot_radius * - 1

        line_vec_towards_robot = comp_line.get_vec_towards_point(current_pos)
        same_direct = np.dot(line_vec_towards_robot.T, vec)

        closest_point, further_point = outside_of_line(current_pos, comp_line.start, comp_line.end)
        if closest_point is not None and same_direct > 0:

            end_point = get_orientation_vector(self.theta, current_pos)
            direct_vector = (rotate_deg(n_vec, 90) if side_of_point(further_point, closest_point, end_point)
                                         else rotate_deg(n_vec, 90) * -1)

            temp_line_start = closest_point
            temp_line_end = closest_point + direct_vector
            new_distance_to_line = distance_point_to_line(current_pos, temp_line_start, temp_line_end)
            perp_line_start = temp_line_start + n_vec * -1 * new_distance_to_line
            perp_line_end = temp_line_end + n_vec * -1 * new_distance_to_line

            robot_angle = abs(np.cos(angle_between(vec, comp_line.vec)))
            pos_on_line = line_intersection(([pos_x, pos_y], [npos_x, npos_y]), ([perp_line_start[0], perp_line_start[1]], [perp_line_end[0], perp_line_end[1]]))
            remaining_length = (np.linalg.norm(vec) - np.linalg.norm(pos_on_line - current_pos)) * robot_angle
            new_next_pos = pos_on_line + direct_vector * remaining_length
        else:
            # Find the position of the robot if it would collide with the wall by using a shifted line towards the robot
            dist_to_line = distance_point_to_line(current_pos, comp_line.start, comp_line.end)
            nvec_towards_robot = (rotate_deg(comp_line.nvec, 90) * -1
                                  if side_of_point(comp_line.start, comp_line.end, current_pos)
                                  else rotate_deg(comp_line.nvec, 90))
            vec_towards_robot = nvec_towards_robot * (dist_to_line if dist_to_line < Const.robot_radius else Const.robot_radius)

            new_line_start = comp_line.start + vec_towards_robot
            new_line_end = comp_line.end + vec_towards_robot
            intersection = line_intersection(([pos_x, pos_y], [npos_x, npos_y]),
                                             ([new_line_start[0], new_line_start[1]],
                                              [new_line_end[0], new_line_end[1]]))
            if intersection is None:
                return current_pos, current_pos

            parallel_vector = comp_line.nvec if np.dot(comp_line.vec.T, vec) > 0 else comp_line.nvec * -1
            pos_on_line = np.array(intersection).reshape((2, 1))
            robot_angle = abs(np.cos(angle_between(vec, comp_line.vec)))
            remaining_length = (np.linalg.norm(vec) - np.linalg.norm(pos_on_line - current_pos)) * robot_angle
            new_next_pos = pos_on_line + parallel_vector * remaining_length

        return pos_on_line, new_next_pos

    def closest_collision(self, collisions: List[Dict], position) -> Dict:
        min = np.inf
        closest = None
        dist_to_projection = -np.inf

        for collision in collisions:
            line_: Line = collision['line']
            dist = distance_point_to_line_seg(position, line_.start, line_.end)

            if dist <= min:
                if len(collisions) > 1:
                    new_dist_to_projection = distance_point_to_line(position, line_.start, line_.end)
                    if new_dist_to_projection > dist_to_projection:
                        min = dist
                        closest = collision
                        dist_to_projection = new_dist_to_projection
                else:
                    min = dist
                    closest = collision
        return closest

    def draw(self, s):
        s_x, s_y = self.get_x_y(self.pos)
        gfxdraw.aacircle(s,
                         int(np.round(s_x)),
                         int(np.round(s_y)),
                         Const.robot_radius,
                         Const.colors['robot'],
                         )
        e_x, e_y = self.get_orientation_vector()
        gfxdraw.line(s,
                     int(np.round(s_x)),
                     int(np.round(s_y)),
                     int(np.round(e_x)),
                     int(np.round(e_y)),
                     Const.colors['green']
                     )
        # # Lines initialization & rotation
        # degree = self.theta
        # x = 0
        # while (x < 11 ):
        #     e_x, e_y = self.get_sensor_vector(degree)
        #     gfxdraw.line(s, int(np.round(s_x)), int(np.round(s_y)), int(np.round(e_x)), int(np.round(e_y)),Const.colors['red'])
        #     degree = degree - 20
        #     x += 1

    def get_x_y(self, vec):
        if vec is None or vec[0] is None:
            print("test")
        return vec[0, 0], vec[1, 0]

#It might be the same code but we don't want for theta to change when we initialize the lines
    def get_sensor_vector(self, degree):
        default_vec = np.array([Const.robot_radius, 0]).reshape((2, 1))
        rotated = rotate(default_vec, degree)
        vec = self.pos + rotated
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
