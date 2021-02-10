import math
from typing import Tuple

import numpy as np

from Line import Line


def rotate(vec: np.ndarray, deg: float):
    rotation_matrix = np.matrix([[np.cos(deg), np.sin(deg)],
                                 [-np.sin(deg), np.cos(deg)]])
    return rotation_matrix * vec


def distance_point_to_point(p1, p2):
    return math.dist(p1, p2)


def distance_point_to_line(point: np.ndarray, line: Line) -> float:
    return np.abs(
        (line.end[0] - line.start[0]) * (line.start[1] - point[1]) -
        (line.start[0] - point[0]) * (line.end[1] - line.start[1])
    ) / np.sqrt(
        (line.end[0] - line.start[0]) ** 2 +
        (line.end[1] - line.start[1]) ** 2
    )


def det(a, b):
    return a[0] * b[1] - a[1] * b[0]


def angle_between_lines(m1, m2):
    if m1 == np.inf:
        return np.arctan(np.deg2rad(90) - m2)
    elif m2 == np.inf:
        return np.arctan(np.deg2rad(90) - m1)
    else:
        return np.arctan(np.abs((m1 - m2) / (1 + m1 * m2)))


def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    div = det(xdiff, ydiff)
    if div == 0:
        return None

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


def line_angle(line: Line) -> int:
    if (line.start[0] - line.end[0]) != 0:
        angle = int(
            np.rad2deg(
                np.arctan(
                    (line.start[1] - line.end[1]) / (line.start[0] - line.end[0])
                )
            )
        )
    else:
        angle = 90
    return angle


def line_param(p1: np.ndarray, p2: np.ndarray):
    return np.array(
        [(p1[1] - p2[1]), (p1[0] - p2[0]), (p1[0] * p2[1] - p2[0] * p1[1])])  # return [A, B, C] of Ax + By + # C = 0


def perpendicular_angles(angle_1: int, angle_2: int) -> bool:
    return np.abs(angle_1 - angle_2) == 90 or np.abs(angle_1 - angle_2) == 270


def parallel_angles(angle_1: int, angle_2: int) -> bool:
    return np.abs(angle_1 - angle_2) == 0 or np.abs(angle_1 - angle_2) == 180
