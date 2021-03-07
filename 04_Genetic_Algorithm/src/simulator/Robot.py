from typing import List

from pygame import gfxdraw
from src.genetic.Decoder import robot_decoder
from src.simulator.Environment import Collision, Environment
from src.genetic.Genome import Genome
import src.utils.Constants as Const
from src.utils.MathUtils import *
from src.simulator.Sensors import Sensors

dt = 1


class Robot:
    """
    Author Frederic Abraham, Guillaume Franzoni Darnois & Theodoros Giannilias
    """

    id = 0

    def __init__(self, init_pos: np.ndarray, init_rotation: float, genome: Genome):
        self.id = Robot.id
        Robot.id += 1

        self.v_l = 0
        self.v_r = 0
        self.l = Const.ROBOT_RADIUS * 2
        self.pos: np.ndarray = init_pos
        self.sensors: Sensors = Sensors()
        self.theta = np.deg2rad(init_rotation)
        self.sensor_hidden = False
        self.genome = genome
        self.number_of_total_collisions = 0
        self.dist_covered = 0
        self.prev_pos = None
        self.prev_rotation = 0
        self.previous_hidden = np.zeros(shape=(Const.HIDDEN_SIZE, 1))
        self.dust: List = self.generate_dust()
        self.dust_collected = 0
        self.life = 0
        self.stop_update = False

    def reset(self, init_pos: np.ndarray, init_rotation: float, genome: Genome):
        self.v_l = 0
        self.v_r = 0
        self.theta = np.deg2rad(init_rotation)
        self.pos: np.ndarray = init_pos

        self.dust: List = self.generate_dust()
        self.prev_pos = None
        self.previous_hidden = np.zeros(shape = (Const.HIDDEN_SIZE, 1))
        self.genome = genome
        self.number_of_total_collisions = 0
        self.dist_covered = 0
        self.dust_collected = 0
        self.life = 0
        self.stop_update = False

    def update(self, environment):

        if self.stop_update:
            return

        # If the bot collided with a wall we stop updating it
        # if self.number_of_total_collisions > 0:
        #     return

        prev_theta = self.theta
        self.life += 1
        # Update sensors and collision counter
        self.sensors.update(environment, self.theta, self.pos)

        # Get decoded value from NN and update previous_hidden
        new_vel, self.previous_hidden = robot_decoder(self.genome, self.sensors, self.previous_hidden)

        # Assign newly calculated velocity
        self.v_r, self.v_l = new_vel[0, 0], new_vel[1, 0]

        self.prev_pos = self.pos

        # Update position
        if not (self.v_r == 0 and self.v_l == 0):
            self.pos = self.check_collisions(environment, self.pos, self.get_position_update(), [])

        self.dist_covered = np.linalg.norm(self.pos - self.prev_pos)

        self.check_dust_particles(self.pos)

    def check_dust_particles(self, robot_current_center: np.ndarray):
        for i in range(len(self.dust) - 1, -1, -1):
            dust = self.dust[i]
            if np.linalg.norm(robot_current_center - dust) < Const.ROBOT_RADIUS:
                self.dust_collected += 1
                del self.dust[i]

    def calc_fitness(self):
        # TODO do correct fitness calculation for roombot (for week 2)
        # self.genome.set_fitness((self.life / Const.LIFE_STEPS + 2 * self.dust_collected / Const.N_PARTICLES) * 100 / 3)
        self.genome.set_fitness(((1 / (1 + self.number_of_total_collisions)) + 2 * self.dust_collected / Const.N_PARTICLES) * 100 / 3)
        # self.genome.set_fitness(self.dust_collected/Const.N_PARTICLES * 100)

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
            self.number_of_total_collisions += 1
            closest_line = self.closest_collision(collisions, current_pos)
            t_current_pos, t_next_pos = self.recalc_next_pos(current_pos, next_pos, closest_line)
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

    def draw(self, screen, pygame) -> None:
        # Draw robot body
        self.draw_robot(screen)
        # Draw sensors
        if self.sensor_hidden:
            self.sensors.draw(screen)

        if self.id == 0:
            for dust in self.dust:
                pygame.draw.circle(screen, Const.COLORS["red"], dust.flatten(), 2)

    def draw_robot(self, screen) -> None:
        s_x, s_y = get_x_y(self.pos)
        gfxdraw.aacircle(
            screen,
            int(np.round(s_x)),
            int(np.round(s_y)),
            Const.ROBOT_RADIUS,
            Const.COLORS['robot'],
        )
        # Draw orientation line ("front" of the robot)
        e_x, e_y = self.get_orientation_vector()
        gfxdraw.line(
            screen,
            int(np.round(s_x)),
            int(np.round(s_y)),
            int(np.round(e_x)),
            int(np.round(e_y)),
            Const.COLORS['green']
        )

    def get_orientation_vector(self, degree: float = None) -> (float, float):
        default_vec = np.array([Const.ROBOT_RADIUS, 0]).reshape((2, 1))
        rotated = rotate(default_vec, self.theta if degree is None else degree)
        vec = self.pos + rotated
        return vec[0, 0], vec[1, 0]

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

    @staticmethod
    def generate_dust() -> List:
        X, Y = np.meshgrid(
            np.linspace(Const.ORIGIN[0] + 20, Const.ORIGIN[0] + Const.MAP_WIDTH - 20, Const.DUST_X_AMOUNT),
            np.linspace(Const.ORIGIN[1] + 20, Const.ORIGIN[1] + Const.MAP_HEIGHT - 20, Const.DUST_Y_AMOUNT)
        )
        return list(map(lambda x: np.reshape(x, (2, 1)), np.column_stack([X.ravel(), Y.ravel()])))
        # n = int(MAP_WIDTH * MAP_HEIGHT / ROBOT_RADIUS)
        # xy_min = ORIGIN
        # xy_max = [MAP_WIDTH, MAP_HEIGHT]
        # return list(np.random.uniform(low = xy_min, high = xy_max, size = (n, 2)))
