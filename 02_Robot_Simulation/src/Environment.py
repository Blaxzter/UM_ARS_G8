from typing import List

import numpy as np
import pygame

from Line import Line
from src.Constants import PADDING, WIDTH, HEIGHT, ROBOT_RADIUS, PADDING_TOP, EPSILON
from src.MathUtils import distance_point_to_point, distance_point_to_line_seg, line_seg_intersection, outside_of_line


class Collision:
    def __init__(self, line: Line, outside_of_line: (np.ndarray, np.ndarray), true_intersection: np.ndarray, extend_intersection: np.ndarray, jumped_through: bool, distance_to_line: float):
        self.line: Line = line                                              # Line that generated the collision
        self.outside_of_line: (np.ndarray, np.ndarray) = outside_of_line    # (None, None) if inside of the line otherwise the end and
        self.extend_intersection: np.ndarray = extend_intersection          # Frederic fill this
        self.true_intersection: np.ndarray = true_intersection              # Frederic fill this
        self.jumped_through: bool = jumped_through                          # Robot jumped through the line
        self.distance: float = distance_to_line                             # Distance from the collision


class Environment:
    def __init__(self):
        self.environment: List[Line] = [
            # OBSTACLES
            Line(WIDTH / 2, PADDING_TOP + 70, WIDTH / 2, HEIGHT / 2 + 50),
            Line(WIDTH / 2, HEIGHT / 2 + 50, WIDTH - PADDING, HEIGHT / 2 + 50),
            # EXTERNAL BOX
            Line(PADDING, PADDING_TOP, WIDTH - PADDING, PADDING_TOP),
            Line(WIDTH - PADDING, PADDING_TOP, WIDTH - PADDING, HEIGHT - PADDING),
            Line(WIDTH - PADDING, HEIGHT - PADDING, PADDING, HEIGHT - PADDING),
            Line(PADDING, HEIGHT - PADDING, PADDING, PADDING_TOP),
            # RIGHT ARROW
            Line(PADDING + 50, PADDING_TOP + 50, PADDING + 500, PADDING_TOP + 500),
            Line(PADDING + 500, PADDING_TOP + 500, PADDING + 650, PADDING_TOP + 1000)
        ]   # Group of boundaries that make up the environment in which the robot moves

    def draw(self, screen: pygame.display) -> None:
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
