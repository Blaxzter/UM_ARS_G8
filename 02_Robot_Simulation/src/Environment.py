from typing import List, Tuple, Dict

import numpy as np

from Line import Line
from src.Constants import padding, width, height, robot_radius, padding_top
from src.MathUtils import line_intersection, distance_point_to_point, distance_point_to_line
from shapely.geometry import LineString


class Environment:
    def __init__(self):
        self.environment = [
            Line(start=np.array([padding, padding_top]), end=np.array([width - padding, padding_top])),
            Line(start=np.array([width - padding, padding_top]), end=np.array([width - padding, height - padding])),
            Line(start=np.array([width - padding, height - padding]), end=np.array([padding, height - padding])),
            Line(start=np.array([padding, height - padding]), end=np.array([padding, padding_top])),
            # Line(start=np.array([69, 69]), end=np.array([169, 196])),
        ]

    def draw(self, screen):
        for line in self.environment:
            line.draw(screen)

    def collides(self, robot_current_center: np.ndarray, robot_next_center: np.ndarray) -> List:
        collisions = []
        for line in self.environment:
            distance_to_line = distance_point_to_line(robot_next_center, line)
            intersection = line_intersection([robot_current_center, robot_next_center], [line.start, line.end])
            if distance_to_line <= robot_radius:
                collisions.append(line)
        return collisions
        # collisions = []
        #
        # for line in self.environment:
        #     intersection = line_intersection([robot_current_center, robot_next_center], [line.start, line.end])
        #     if intersection:
        #         collisions.append({
        #             'line': line,
        #             'intersect': intersection,
        #             'distance': distance_point_to_point(intersection, robot_current_center)
        #         })
        # return collisions


# Collision Test
if __name__ == '__main__':
    e = Environment()
    collisions = e.collides(np.array([10, 110]), np.array([20, 110]))
