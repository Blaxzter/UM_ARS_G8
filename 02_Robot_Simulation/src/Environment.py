from typing import List, Tuple, Dict

import numpy as np

from Line import Line
from src.Constants import padding, width, height, robot_radius, padding_top, epsilon
from src.MathUtils import line_intersection, distance_point_to_point, distance_point_to_line, \
    distance_point_to_line_seg, line_seg_intersection


class Environment:
    def __init__(self):
        self.environment = [
            Line(width / 2, padding_top + 70, width / 2, height / 2 + 50),
            Line(width / 2, height / 2 + 50, width - padding, height / 2 + 50),
            Line(padding, padding_top, width - padding, padding_top),
            Line(width - padding, padding_top, width - padding, height - padding),
            Line(width - padding, height - padding, padding, height - padding),
            Line(padding, height - padding, padding, padding_top),
            # Line(69, 69, 169, 196),
            # Line(width / 2 - ((width / 2) / 2), padding_top + 50, width / 2 + ((width / 2) / 2), (height + padding_top) / 2),
            # Line(width / 2 - ((width / 2) / 2), height - padding - 50, width / 2 + ((width / 2) / 2), (height + padding_top) / 2),
        ]

    def draw(self, screen):
        for line in self.environment:
            line.draw(screen)

    def collides(self, robot_current_center: np.ndarray, robot_next_center: np.ndarray) -> List:
        collisions = []

        for line in self.environment:
            distance_next_center_to_line = distance_point_to_line_seg(robot_next_center, line.start, line.end)
            intersection = line_seg_intersection(robot_current_center, robot_next_center, line.start, line.end)
            occurs_before_next = False
            if intersection is not None:
                occurs_before_next = distance_point_to_point(robot_current_center, robot_next_center) > distance_point_to_point(robot_current_center, intersection)

            if (robot_radius - distance_next_center_to_line > epsilon) or occurs_before_next:
                collisions.append({
                    'line': line,
                    'intersect': intersection,
                    # 'jumped_through': occurs_before_next,
                    'distance': distance_next_center_to_line
                })
        return collisions


# Collision Test
if __name__ == '__main__':
    e = Environment()
    collisions = e.collides(np.array([50, 150]), np.array([70, 150]))
    print(len(collisions))
