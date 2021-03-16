import pygame

from typing import List

import scipy as scipy
from pygame import gfxdraw
from scipy.optimize import minimize

from kalman.KalmanFilter import KalmanFilter
from simulator.Environment import Collision, Environment
from simulator.MathUtils import *
from simulator.MathUtils import get_x_y
from simulator.Sensors import Sensors

# Mostly done by frederic

dt = 1


class Robot:
    def __init__(self, init_pos: np.ndarray):
        self.v_l: float = 0  # Velocity of left wheel
        self.v_r: float = 0  # Velocity of right wheel
        self.l: int = Const.ROBOT_RADIUS * 2  # distance between the motors
        self.pos: np.ndarray = init_pos  # Current position of the robot
        self.sensors: Sensors = Sensors()  # Sensor used by the robots
        self.theta: float = np.deg2rad(Const.START_ROT)  # Rotation of the robot (wrt the "front")
        self.sensor_hidden: bool = False  # Show/Hide sensors
        self.dragging = False

        # Localization variables
        self.mu = np.array([
            self.pos[0, 0] + np.random.normal(scale=Const.GAUSSIAN_SCALE),
            self.pos[1, 0] + np.random.normal(scale=Const.GAUSSIAN_SCALE),
            self.theta + np.random.normal(scale=Const.GAUSSIAN_SCALE)]
        ).reshape(3, 1)  # Initial position when initializing, contains the belief state
        self.sigma = np.identity(3) * np.array([
            np.random.normal(scale=Const.GAUSSIAN_SCALE),
            np.random.normal(scale=Const.GAUSSIAN_SCALE),
            np.random.normal(scale=Const.GAUSSIAN_SCALE)]
        ).reshape(3, 1)  # Covariance matrix
        self.u = None    # Linear Combined Velocity, Rotation of motion
        self.z = None    # Sensor observed state
        self.localization_kf = KalmanFilter(1, self.theta)  # Kalman Filter

    def drag(self, x, y):
        if Const.PADDING + Const.ROBOT_RADIUS < x < Const.WIDTH - Const.PADDING - Const.ROBOT_RADIUS \
                and Const.PADDING_TOP + Const.ROBOT_RADIUS < y < Const.HEIGHT - Const.PADDING - Const.ROBOT_RADIUS:
            self.pos = np.array([x, y], dtype=float).reshape(2, 1)

    def update(self, environment: Environment, landmarks) -> None:

        # Update position
        if not (self.v_r == 0 and self.v_l == 0):
            self.localization_kf.update_B(1, self.mu[2].item())

            v = (self.v_r + self.v_l) / 2  # AVG velocity of wheels
            w = (self.v_r - self.v_l) / self.l  # Rate of rotation
            self.u = np.array([v, -w]).reshape(2, 1)

            self.z = self.compute_sensors_state(landmarks)

            self.mu, self.sigma = self.localization_kf.kalman_filter(self.mu, self.sigma, self.u, self.z)

            self.pos = self.check_collisions(environment, self.pos, self.get_position_update(), [])

        # TODO: move LIDAR detecting landmarks inside robot
        # Update sensors | No need for sensors in this assignment
        # self.sensors.update(environment, self.theta, self.pos)

    def get_position_update(self) -> np.ndarray:
        # Rotate on the spot
        if self.v_r - self.v_l == 0:
            default_vec = np.array([self.v_r, 0]).reshape((2, 1))
            rotated = rotate(default_vec, self.theta)
            d_position = self.pos + rotated
        # Move
        else:
            R = (self.l / 2) * ((self.v_l + self.v_r) / (self.v_r - self.v_l))
            w = (self.v_r - self.v_l) / self.l

            icc = self.pos - R * np.array([np.sin(self.theta), np.cos(self.theta)]).reshape((2, 1))

            x, y = get_x_y(self.pos)
            icc_x, icc_y = get_x_y(icc)
            next_pos = np.matrix([[np.cos(w * dt), np.sin(w * dt), 0],
                                  [-np.sin(w * dt), np.cos(w * dt), 0],
                                  [0, 0, 1]]) \
                       * np.array([x - icc_x, y - icc_y, self.theta]).reshape((3, 1)) \
                       + np.array([icc_x, icc_y, w * dt]).reshape((3, 1))

            d_position = next_pos[:2]
            self.theta = next_pos[2, 0] % (2 * np.pi)
        return d_position

    def check_collisions(self, environment: Environment, current_pos: np.ndarray, next_pos: np.ndarray,
                         prev_collision: List[Collision]) -> np.ndarray:
        collisions = environment.collides(current_pos, next_pos)
        if len(collisions) == 0 or get_x_y(next_pos) == (0, 0):
            return next_pos
        else:
            closest_line = self.closest_collision(collisions, current_pos)
            t_current_pos, t_next_pos = self.recalc_next_pos(current_pos, next_pos, closest_line)
            # if self.recalc_next_pos(current_pos, next_pos, closest_line)[1].shape == (2,2):
            #     t_current_pos, t_next_pos = self.recalc_next_pos(current_pos, next_pos, closest_line)
            new_collisions = environment.collides(t_current_pos, t_next_pos)
            prev_collision.append(closest_line.line)
            if len(new_collisions) == 0:
                return t_next_pos
            else:
                if new_collisions[0].line in prev_collision:
                    return current_pos
                else:
                    return self.check_collisions(environment, t_current_pos, t_next_pos, prev_collision)

    def recalc_next_pos(self, current_pos: np.ndarray, next_pos: np.ndarray, collisions: Collision) -> (
            np.ndarray, np.ndarray):
        pos_x, pos_y = get_x_y(current_pos)
        npos_x, npos_y = get_x_y(next_pos)
        vec = next_pos - current_pos
        vec_norm = np.linalg.norm(vec)
        n_vec = vec / vec_norm
        comp_line: Line = collisions.line

        # We are going perpendicular to the wall
        if (np.abs(vec_norm) < Const.EPSILON or np.abs(np.dot(comp_line.vec.T, vec)) < Const.EPSILON) \
                and collisions.true_intersection is not None:
            new_intersection = line_intersection(
                ([pos_x, pos_y], [npos_x, npos_y]),
                ([comp_line.start[0], comp_line.start[1]], [comp_line.end[0], comp_line.end[1]])
            )
            return current_pos, new_intersection + (vec / vec_norm) * Const.ROBOT_RADIUS * - 1

        line_vec_towards_robot = comp_line.get_vec_towards_point(current_pos)
        same_direct = np.dot(line_vec_towards_robot.T, vec)

        closest_point, further_point = outside_of_line(current_pos, comp_line.start, comp_line.end)
        if closest_point is not None and same_direct > 0:

            curr_orientation = angle_between(n_vec, x_axes)
            curr_orientation = (2 * np.pi - curr_orientation) % (2 * np.pi)
            end_point = get_orientation_vector(curr_orientation, current_pos)
            direct_vector = (rotate_deg(n_vec, 90) if side_of_point(further_point, closest_point, end_point)
                             else rotate_deg(n_vec, 90) * -1)

            temp_line_start = closest_point
            temp_line_end = closest_point + direct_vector
            new_distance_to_line = distance_point_to_line(current_pos, temp_line_start, temp_line_end)
            perp_line_start = temp_line_start + n_vec * -1 * new_distance_to_line
            perp_line_end = temp_line_end + n_vec * -1 * new_distance_to_line

            robot_angle = abs(np.cos(angle_between(vec, comp_line.vec)))
            pos_on_line = line_intersection(([pos_x, pos_y], [npos_x, npos_y]), (
                [perp_line_start[0], perp_line_start[1]], [perp_line_end[0], perp_line_end[1]]))
            remaining_length = (np.linalg.norm(vec) - np.linalg.norm(pos_on_line - current_pos)) * robot_angle
            new_next_pos = pos_on_line + direct_vector * remaining_length
        else:
            # Find the position of the robot if it would collide with the wall by using a shifted line towards the robot
            dist_to_line = distance_point_to_line(current_pos, comp_line.start, comp_line.end)
            nvec_towards_robot = (rotate_deg(comp_line.nvec, 90) * -1
                                  if side_of_point(comp_line.start, comp_line.end, current_pos)
                                  else rotate_deg(comp_line.nvec, 90))
            vec_towards_robot = nvec_towards_robot * (
                dist_to_line if dist_to_line < Const.ROBOT_RADIUS else Const.ROBOT_RADIUS)

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

    def draw(self, screen: pygame.display) -> None:
        # Draw robot body
        self.draw_robot(screen)
        # Draw sensors
        if self.sensor_hidden:
            self.sensors.draw(screen)

    def draw_robot(self, screen: pygame.display) -> None:
        s_x, s_y = get_x_y(self.pos)
        gfxdraw.aacircle(
            screen,
            int(np.round(s_x)),
            int(np.round(s_y)),
            Const.ROBOT_RADIUS,
            Const.COLORS.black,
        )

        # Draw orientation line ("front" of the robot)
        e_x, e_y = self.get_orientation_vector()
        gfxdraw.line(
            screen,
            int(np.round(s_x)),
            int(np.round(s_y)),
            int(np.round(e_x)),
            int(np.round(e_y)),
            Const.COLORS.black
        )

    def get_orientation_vector(self, degree: float = None) -> (float, float):
        default_vec = np.array([Const.ROBOT_RADIUS, 0]).reshape((2, 1))
        rotated = rotate(default_vec, self.theta if degree is None else degree)
        vec = self.pos + rotated
        return vec[0, 0], vec[1, 0]

    def stop(self) -> None:
        self.v_l = 0
        self.v_r = 0

    def increase_both(self) -> None:
        self.v_l += Const.ROBOT_VELOCITY_STEPS
        self.v_r += Const.ROBOT_VELOCITY_STEPS
        self.v_l = np.round(self.v_l, decimals=3)
        self.v_r = np.round(self.v_r, decimals=3)

    def decrease_both(self) -> None:
        self.v_l -= Const.ROBOT_VELOCITY_STEPS
        self.v_r -= Const.ROBOT_VELOCITY_STEPS
        self.v_l = np.round(self.v_l, decimals=3)
        self.v_r = np.round(self.v_r, decimals=3)

    def rotate_left(self) -> None:
        # self.theta += np.deg2rad(1)
        # self.theta = self.theta % (2 * np.pi)
        self.v_l -= Const.ROBOT_VELOCITY_STEPS
        self.v_l = np.round(self.v_l, decimals=3)
        self.v_r += Const.ROBOT_VELOCITY_STEPS
        self.v_r = np.round(self.v_r, decimals=3)

    def rotate_right(self) -> None:
        # self.theta -= np.deg2rad(1)
        # self.theta = self.theta % (2 * np.pi)
        self.v_l += Const.ROBOT_VELOCITY_STEPS
        self.v_l = np.round(self.v_l, decimals=3)
        self.v_r -= Const.ROBOT_VELOCITY_STEPS
        self.v_r = np.round(self.v_r, decimals=3)

    def increase_left(self) -> None:
        self.v_l += Const.ROBOT_VELOCITY_STEPS
        self.v_l = np.round(self.v_l, decimals=3)

    def decrease_left(self) -> None:
        self.v_l -= Const.ROBOT_VELOCITY_STEPS
        self.v_l = np.round(self.v_l, decimals=3)

    def increase_right(self) -> None:
        self.v_r += Const.ROBOT_VELOCITY_STEPS
        self.v_r = np.round(self.v_r, decimals=3)

    def decrease_right(self) -> None:
        self.v_r -= Const.ROBOT_VELOCITY_STEPS
        self.v_r = np.round(self.v_r, decimals=3)

    def toggle_sensor(self) -> None:
        self.sensor_hidden = not self.sensor_hidden

    @staticmethod
    def closest_collision(collisions: List[Collision], position) -> Collision:
        minimum = np.inf
        closest = None

        for collision in collisions:
            line_: Line = collision.line
            dist = distance_point_to_line_seg(position, line_.start, line_.end)

            if dist <= minimum:
                minimum = dist
                closest = collision
        return closest

    def compute_sensors_state(self, landmarks: List[np.ndarray]):

        position = minimize(
            self.mse_position,  # The error function
            np.array([self.mu[0, 0], self.mu[1, 0]]),  # The initial guess
            args=([(l['pos'][0, 0], l['pos'][1, 0]) for l in landmarks], [f['dist'] for f in landmarks]),  # Additional parameters for mse
            method='L-BFGS-B',  # The optimisation algorithm
            options={
                'ftol': 1e-5,  # Tolerance
                'maxiter': 1e+10  # Maximum iterations
            })
        np.seterr(all='raise')

        theta = self.theta  #sum([f['bearing'] for f in landmarks])/len([f['bearing'] for f in landmarks])

        return np.array([position.x[0], position.x[1], theta]).reshape(3, 1) + np.array([np.random.normal(scale=Const.GAUSSIAN_SCALE), np.random.normal(scale=Const.GAUSSIAN_SCALE), np.random.normal(scale=Const.GAUSSIAN_SCALE)]).reshape(3, 1) # Return observed state with noise

    # https://www.alanzucconi.com/2017/03/13/positioning-and-trilateration/
    @staticmethod
    def mse_position(x, locations, distances):
        mse = 0.0
        for location, distance in zip(locations, distances):
            distance_calculated = math.dist((x[0], x[1]), (location[0], location[1]))
            mse += np.square(distance_calculated - distance)
        return mse / len(distances)
