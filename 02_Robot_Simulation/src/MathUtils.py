import math
import numpy as np
from shapely.geometry import LineString
import Constants as Const


def rotate(vec: np.ndarray, rad: float):
    rotation_matrix = np.matrix([[np.cos(rad), np.sin(rad)],
                                 [-np.sin(rad), np.cos(rad)]])
    return np.asarray(rotation_matrix * vec)


def rotate_deg(vec: np.ndarray, rad: float):
    deg = np.deg2rad(rad)
    rotation_matrix = np.matrix([[np.cos(deg), np.sin(deg)],
                                 [-np.sin(deg), np.cos(deg)]])
    return rotation_matrix * vec


def distance_point_to_point(p1, p2):
    return math.dist(p1, p2)


def distance_point_to_line(point: np.ndarray, line_start: np.ndarray, line_end: np.ndarray) -> float:
    distance = np.abs((line_end[0] - line_start[0]) * (line_start[1] - point[1]) - (line_start[0] - point[0]) * (
            line_end[1] - line_start[1])) / np.sqrt(
        (line_end[0] - line_start[0]) ** 2 + (line_end[1] - line_start[1]) ** 2)
    return distance[0]


def get_orientation_vector(orientation, position):
    default_vec = np.array([Const.robot_radius, 0]).reshape((2, 1))
    rotated = rotate(default_vec, orientation)
    vec = position + rotated
    return np.array([vec[0, 0], vec[1, 0]]).reshape((2, 1))


def det(a, b):
    return a[0] * b[1] - a[1] * b[0]


def angle_between_lines(m1, m2):
    if m1 == np.inf:
        return np.arctan(abs(1 / m2))
    elif m2 == np.inf:
        return np.arctan(abs(1 / m1))
    else:
        return np.arctan(abs((m1 - m2) / (1 + m1 * m2)))


def side_of_point(line_start: np.ndarray, line_end: np.ndarray, point: np.ndarray):
    ab = line_end - line_start
    ap = point - line_start
    cross_product = ab[0] * ap[1] - ap[0] * ab[1]
    return cross_product > 0


def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)


def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u.T, v2_u), -1.0, 1.0))[0, 0]


def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    div = det(xdiff, ydiff)
    if div == 0:
        return None

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return np.array([x[0], y[0]]).reshape((2, 1))


def line_seg_intersection(a1, a2, b1, b2):
    line1 = LineString([a1, a2])
    line2 = LineString([b1, b2])
    intersection = line1.intersection(line2)
    if intersection.is_empty:
        return None
    return np.array(intersection).reshape((2, 1))


def math_line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0] * p2[1] - p2[0] * p1[1])
    return A, B, -C


# from: https://gist.github.com/nim65s/5e9902cd67f094ce65b0
def distance_point_to_line_seg(p: np.ndarray, s: np.ndarray, e: np.ndarray):
    if all(s == p) or all(e == p):
        return 0
    if np.arccos(np.dot(((p - s) / np.linalg.norm(p - s)).T, (e - s) / np.linalg.norm(e - s))).item() > np.pi / 2:
        return np.linalg.norm(p - s)
    if np.arccos(np.dot(((p - e) / np.linalg.norm(p - e)).T, (s - e) / np.linalg.norm(s - e))).item() > np.pi / 2:
        return np.linalg.norm(p - e)
    return np.linalg.norm(np.cross(s - e, s - p, axis=0)) / np.linalg.norm(e - s)

# from: https://gist.github.com/nim65s/5e9902cd67f094ce65b0
def outside_of_line(p: np.ndarray, s: np.ndarray, e: np.ndarray):
    if all(s == p) or all(e == p):
        return None, None
    if np.arccos(np.dot(((p - s) / np.linalg.norm(p - s)).T, (e - s) / np.linalg.norm(e - s))).item() > np.pi / 2:
        return s, e
    if np.arccos(np.dot(((p - e) / np.linalg.norm(p - e)).T, (s - e) / np.linalg.norm(s - e))).item() > np.pi / 2:
        return e, s
    return None, None



# def line_angle(line: Line) -> int:
#     if (line.start[0] - line.end[0]) != 0:
#         angle = int(
#             np.rad2deg(
#                 np.arctan(
#                     (line.start[1] - line.end[1]) / (line.start[0] - line.end[0])
#                 )
#             )
#         )
#     else:
#         angle = 90
#     return angle


def line_param(p1: np.ndarray, p2: np.ndarray):
    return np.array(
        [(p1[1] - p2[1]), (p1[0] - p2[0]), (p1[0] * p2[1] - p2[0] * p1[1])])  # return [A, B, C] of Ax + By + # C = 0


def perpendicular_angles(angle_1: int, angle_2: int) -> bool:
    return np.abs(angle_1 - angle_2) == 90 or np.abs(angle_1 - angle_2) == 270


def parallel_angles(angle_1: int, angle_2: int) -> bool:
    return np.abs(angle_1 - angle_2) == 0 or np.abs(angle_1 - angle_2) == 180
