import math
from typing import List

import numpy as np
from shapely.geometry import LineString
import Constants as Const
from src.Line import Line


def rotate(vec: np.ndarray, rad: float) -> np.ndarray:
    rotation_matrix = np.matrix([[np.cos(rad), np.sin(rad)],
                                 [-np.sin(rad), np.cos(rad)]])
    return np.asarray(rotation_matrix * vec)


def rotate_deg(vec: np.ndarray, rad: float) -> np.ndarray:
    deg = np.deg2rad(rad)
    rotation_matrix = np.matrix([[np.cos(deg), np.sin(deg)],
                                 [-np.sin(deg), np.cos(deg)]])
    return rotation_matrix * vec


def distance_point_to_point(p1: (float, float), p2: (float, float)) -> float:
    return math.dist(p1, p2)


def distance_point_to_line(point: np.ndarray, line_start: np.ndarray, line_end: np.ndarray) -> float:
    distance = np.abs((line_end[0] - line_start[0]) * (line_start[1] - point[1]) - (line_start[0] - point[0]) * (
            line_end[1] - line_start[1])) / np.sqrt(
        (line_end[0] - line_start[0]) ** 2 + (line_end[1] - line_start[1]) ** 2)
    return distance[0]


def get_orientation_vector(orientation: float, position: np.ndarray) -> np.ndarray:
    default_vec = np.array([Const.ROBOT_RADIUS, 0]).reshape((2, 1))
    rotated = rotate(default_vec, orientation)
    vec = position + rotated
    return np.array([vec[0, 0], vec[1, 0]]).reshape((2, 1))


def det(a: (float, float), b: (float, float)) -> float:
    return a[0] * b[1] - a[1] * b[0]


def angle_between_lines(m1: float, m2: float) -> float:
    if m1 == np.inf:
        return np.arctan(abs(1 / m2))
    elif m2 == np.inf:
        return np.arctan(abs(1 / m1))
    else:
        return np.arctan(abs((m1 - m2) / (1 + m1 * m2)))


def side_of_point(line_start: np.ndarray, line_end: np.ndarray, point: np.ndarray) -> bool:
    ab = line_end - line_start
    ap = point - line_start
    cross_product = ab[0] * ap[1] - ap[0] * ab[1]
    return cross_product > 0


def unit_vector(vector: np.ndarray) -> np.ndarray:
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)


def angle_between(v1: np.ndarray, v2: np.ndarray) -> float:
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u.T, v2_u), -1.0, 1.0))[0, 0]


def line_intersection(line1: np.ndarray, line2: np.ndarray) -> np.ndarray:
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    div = det(xdiff, ydiff)
    if div == 0:
        return None

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return np.array([x[0], y[0]]).reshape((2, 1))


def line_seg_intersection(a1: float, a2: float, b1: float, b2: float) -> np.ndarray:
    line1 = LineString([a1, a2])
    line2 = LineString([b1, b2])
    intersection = line1.intersection(line2)
    if intersection.is_empty:
        return None
    return np.array(intersection).reshape((2, 1))


def math_line(p1: (float, float), p2: (float, float)):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0] * p2[1] - p2[0] * p1[1])
    return A, B, -C


# from: https://gist.github.com/nim65s/5e9902cd67f094ce65b0
def distance_point_to_line_seg(p: np.ndarray, s: np.ndarray, e: np.ndarray) -> float:
    if all(s == p) or all(e == p):
        return 0.
    if np.arccos(np.dot(((p - s) / np.linalg.norm(p - s)).T, (e - s) / np.linalg.norm(e - s))).item() > np.pi / 2:
        return np.linalg.norm(p - s)
    if np.arccos(np.dot(((p - e) / np.linalg.norm(p - e)).T, (s - e) / np.linalg.norm(s - e))).item() > np.pi / 2:
        return np.linalg.norm(p - e)
    return np.linalg.norm(np.cross(s - e, s - p, axis=0)) / np.linalg.norm(e - s)


# from: https://gist.github.com/nim65s/5e9902cd67f094ce65b0
def outside_of_line(p: np.ndarray, s: np.ndarray, e: np.ndarray) -> (np.ndarray, np.ndarray):
    if all(s == p) or all(e == p):
        return None, None
    if np.arccos(np.dot(((p - s) / np.linalg.norm(p - s)).T, (e - s) / np.linalg.norm(e - s))).item() > np.pi / 2:
        return s, e
    if np.arccos(np.dot(((p - e) / np.linalg.norm(p - e)).T, (s - e) / np.linalg.norm(s - e))).item() > np.pi / 2:
        return e, s
    return None, None


def line_param(p1: np.ndarray, p2: np.ndarray) -> np.ndarray:
    return np.array(
        [(p1[1] - p2[1]), (p1[0] - p2[0]), (p1[0] * p2[1] - p2[0] * p1[1])])  # return [A, B, C] of Ax + By + # C = 0


def perpendicular_angles(angle_1: int, angle_2: int) -> bool:
    return np.abs(angle_1 - angle_2) == 90 or np.abs(angle_1 - angle_2) == 270


def parallel_angles(angle_1: int, angle_2: int) -> bool:
    return np.abs(angle_1 - angle_2) == 0 or np.abs(angle_1 - angle_2) == 180


def intersection_semiline_segment(segment: Line, line_start: (float, float), direction_point: (float, float)) -> np.ndarray:
    x1 = segment.start_x
    y1 = segment.start_y
    x2 = segment.end_x
    y2 = segment.end_y
    x0 = line_start[0]
    y0 = line_start[1]
    xd = direction_point[0] - line_start[0]
    yd = direction_point[1] - line_start[1]

    denominator = xd * (y2 - y1) - yd * (x2 - x1)
    if denominator == 0:
        return np.array([])

    t = ((x1 - x0) * yd - (y1 - y0) * xd) / denominator
    tao = (x0 * (y1 - y2) + x1 * (y2 - y0) + x2 * (y0 - y1)) / denominator

    if 0 <= t <= 1 and tao >= 0:
        intersection_x = x0 + tao * xd
        intersection_y = y0 + tao * yd
        return np.array([intersection_x, intersection_y]).reshape(2, 1)
    else:
        return np.array([])


def get_x_y(vec: np.ndarray) -> (float, float):
    if vec is None or vec[0] is None:
        print("test")
    return vec[0, 0], vec[1, 0]
