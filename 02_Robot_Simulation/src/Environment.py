from typing import List

import numpy as np

from Line import Line
from src.Constants import padding, width, height, robot_radius, padding_top


class Environment:
    def __init__(self):
        self.environment = [
            Line(start=np.array([padding, padding_top]), end=np.array([width - padding, padding_top])),
            Line(start=np.array([width - padding, padding_top]), end=np.array([width - padding, height - padding])),
            Line(start=np.array([width - padding, height - padding]), end=np.array([padding, height - padding])),
            Line(start=np.array([padding, height - padding]), end=np.array([padding, padding_top])),
        ]

    def draw(self, screen):
        for line in self.environment:
            line.draw(screen)

    def collides(self, robot_center: np.ndarray) -> List[Line]:
        collisions = []
        for line in self.environment:
            distance_to_line = self.distance_point_to_line(robot_center, line)
            if distance_to_line <= robot_radius:
                collisions.append(line)
        return collisions

    @staticmethod
    def distance_point_to_line(point: np.ndarray, line: Line) -> float:
        return np.abs(
            (line.end[0] - line.start[0]) * (line.start[1] - point[1]) -
            (line.start[0] - point[0]) * (line.end[1] - line.start[1])
        ) / np.sqrt(
            (line.end[0] - line.start[0]) ** 2 +
            (line.end[1] - line.start[1]) ** 2
        )

# Collision Test
if __name__ == '__main__':
    e = Environment()
    collisions = e.collides(np.array([10, 10]))
