from typing import List, Tuple, Dict

import numpy as np

from Line import Line
from src.Constants import padding, width, height, robot_radius, padding_top, epsilon
from src.MathUtils import line_intersection, distance_point_to_point, distance_point_to_line

class Environment:
    def __init__(self):
        self.environment = [
            Line(width / 2,         padding_top + 50,   width / 2,          height / 2  + 50),
            Line(padding,           padding_top,        width - padding,    padding_top),
            Line(width - padding,   padding_top,        width - padding,    height - padding),
            Line(width - padding,   height - padding,   padding,            height - padding),
            Line(padding,           height - padding,   padding,            padding_top),
            Line(69, 69, 169, 196),
        ]

    def draw(self, screen):
        for line in self.environment:
            line.draw(screen)

    def collides(self, robot_current_center: np.ndarray, robot_next_center: np.ndarray) -> List:
        collisions = []
        for line in self.environment:
            distance_to_line = distance_point_to_line(robot_next_center, line)

            relevant_intersection = False
            intersection_outside_line = False
            intersection = line_intersection([robot_current_center, robot_next_center], [line.start, line.end])

            if intersection is not None:
                point_on_line = line.is_on(intersection)
                if point_on_line:
                    intersection_outside_line = True
                    occurs_before_next = distance_point_to_point(robot_current_center, robot_next_center) > distance_point_to_point(robot_current_center, intersection)
                    if occurs_before_next:
                        relevant_intersection = True

            if relevant_intersection or (robot_radius - distance_to_line > epsilon and intersection_outside_line):
                collisions.append({
                    'line': line,
                    'intersect': intersection,
                    'distance': distance_point_to_point(intersection, robot_current_center)
                })
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
    collisions = e.collides(np.array([50, 150]), np.array([70, 150]))
    print(len(collisions))
