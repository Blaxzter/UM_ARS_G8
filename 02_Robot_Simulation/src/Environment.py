from typing import List, Tuple, Dict

import numpy as np

from Line import Line
from src.Constants import PADDING, WIDTH, HEIGHT, ROBOT_RADIUS, PADDING_TOP, EPSILON
from src.MathUtils import line_intersection, distance_point_to_point, distance_point_to_line, \
    distance_point_to_line_seg, line_seg_intersection, outside_of_line


class Collision:
    def __init__(self, line, outside_of_line, true_intersection, extend_intersection, jumped_through, distance_to_line):
        self.line = line
        self.outside_of_line = outside_of_line
        self.extend_intersection = extend_intersection
        self.true_intersection = true_intersection
        self.jumped_through = jumped_through
        self.distance = distance_to_line


class Environment:
    def __init__(self):
        self.environment = [
            Line(WIDTH / 2, PADDING_TOP + 70, WIDTH / 2, HEIGHT / 2 + 50),
            Line(WIDTH / 2, HEIGHT / 2 + 50, WIDTH - PADDING, HEIGHT / 2 + 50),
            Line(PADDING, PADDING_TOP, WIDTH - PADDING, PADDING_TOP),
            Line(WIDTH - PADDING, PADDING_TOP, WIDTH - PADDING, HEIGHT - PADDING),
            Line(WIDTH - PADDING, HEIGHT - PADDING, PADDING, HEIGHT - PADDING),
            Line(PADDING, HEIGHT - PADDING, PADDING, PADDING_TOP),
            # Line(69, 69, 169, 196),
            # Line(width / 2 - ((width / 2) / 2), padding_top + 50, width / 2 + ((width / 2) / 2), (height + padding_top) / 2),
            # Line(width / 2 - ((width / 2) / 2), height - padding - 50, width / 2 + ((width / 2) / 2), (height + padding_top) / 2),
        ]

    def draw(self, screen):
        for line in self.environment:
            line.draw(screen)

    def collides(self, robot_current_center: np.ndarray, robot_next_center: np.ndarray) -> List[Collision]:
        collisions = []

        for line in self.environment:

            distance_to_line = distance_point_to_line_seg(robot_next_center, line.start, line.end)
            extend_intersection = line_seg_intersection(robot_current_center, robot_next_center, line.col_start, line.col_end)
            true_intersection = line_seg_intersection(robot_current_center, robot_next_center, line.start, line.end)
            jumped_through = False
            if extend_intersection is not None:
                jumped_through = distance_point_to_point(robot_current_center, robot_next_center) > distance_point_to_point(
                    robot_current_center, extend_intersection)

            if extend_intersection is not None and true_intersection is None and np.dot((robot_current_center - robot_next_center).T, line.vec) < EPSILON:
                continue

            if (ROBOT_RADIUS - distance_to_line > EPSILON) or jumped_through:
                collisions.append(Collision(
                    line,
                    outside_of_line(robot_current_center, line.start, line.end),
                    true_intersection,
                    extend_intersection,
                    jumped_through,
                    distance_to_line
                ))
        return collisions


# Collision Test
if __name__ == '__main__':
    e = Environment()
    collisions = e.collides(np.array([50, 150]), np.array([70, 150]))
    print(len(collisions))
