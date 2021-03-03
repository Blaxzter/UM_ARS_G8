from typing import List

import numpy as np
import pygame

from src.simulator.Line import Line
from src.simulator.Room import Room
import src.utils.Constants as Const
from src.utils.MathUtils import distance_point_to_point, distance_point_to_line_seg, line_seg_intersection, outside_of_line

# This class was mostly created by Guillaume


class Collision:
    """
    Author Frederic Abraham & Guillaume Franzoni Darnois
    """
    def __init__(self, line: Line, outside_of_line: (np.ndarray, np.ndarray), true_intersection: np.ndarray, extend_intersection: np.ndarray, jumped_through: bool, distance_to_line: float):
        self.line: Line = line                                              # Line that generated the collision
        self.outside_of_line: (np.ndarray, np.ndarray) = outside_of_line    # (None, None) if inside of the line otherwise the end
        self.extend_intersection: np.ndarray = extend_intersection          # Frederic fill this
        self.true_intersection: np.ndarray = true_intersection              # Frederic fill this
        self.jumped_through: bool = jumped_through                          # Robot jumped through the line
        self.distance: float = distance_to_line                             # Distance from the collision


class Environment:
    def __init__(self):
        self.environment: Room = Room(0) # parameter: room number

    def draw(self, screen: pygame.display) -> None:
        for line in self.environment.map:
            line.draw(screen)

    def collides(self, robot_current_center: np.ndarray, robot_next_center: np.ndarray) -> List[Collision]:
        collisions = []

        dist_traveled = np.linalg.norm(robot_current_center - robot_next_center)

        for line in self.environment.map:
            distance_to_line = distance_point_to_line_seg(robot_next_center, line.start, line.end)

            # Check if we actually need to calculate if we jumped through a line based on the velocity and the distance to
            if distance_to_line > dist_traveled and (Const.ROBOT_RADIUS - distance_to_line) < Const.EPSILON:
                continue

            extend_intersection = line_seg_intersection(robot_current_center, robot_next_center, line.col_start, line.col_end)
            true_intersection = line_seg_intersection(robot_current_center, robot_next_center, line.start, line.end)
            jumped_through = False
            if extend_intersection is not None:
                jumped_through = distance_point_to_point(robot_current_center, robot_next_center) > distance_point_to_point(
                    robot_current_center, extend_intersection)

            # We need this because otherwise we would stop at the extended line of a
            if extend_intersection is not None and true_intersection is None and np.abs(np.dot((robot_current_center - robot_next_center).T, line.vec)) < Const.EPSILON:
                continue

            if (Const.ROBOT_RADIUS - distance_to_line > Const.EPSILON) or jumped_through:
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
