from typing import List, Tuple, Dict

import numpy as np

from Line import Line
from src.Constants import padding, width, height, robot_radius, padding_top, epsilon
from src.MathUtils import line_intersection, distance_point_to_point, distance_point_to_line, \
    distance_point_to_line_seg, line_seg_intersection


class Collision:
    def __init__(self, line, true_intersection, extend_intersection, jumped_through, distance_to_line):
        self.line = line
        self.extend_intersection = extend_intersection
        self.true_intersection = true_intersection
        self.jumped_through = jumped_through
        self.distance = distance_to_line


class Environment:
    def __init__(self):
        self.environment = [
            Line(width / 2,         padding_top + 70,   width / 2,                    height / 2 + 50),
            Line(width / 2,         height / 2 + 50,    width - padding,              height / 2 + 50),
            Line(padding,           padding_top,        width - padding,    padding_top),
            Line(width - padding,   padding_top,        width - padding,    height - padding),
            Line(width - padding,   height - padding,   padding,            height - padding),
            Line(padding,           height - padding,   padding,            padding_top),
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

            if extend_intersection is not None and true_intersection is None and np.dot((robot_current_center - robot_next_center).T, line.vec) < epsilon:
                continue

            if (robot_radius - distance_to_line > epsilon) or jumped_through:
                collisions.append(Collision(
                    line,
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
