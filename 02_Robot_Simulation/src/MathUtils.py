import numpy as np


def rotate(vec: np.ndarray, deg: float):
    rotation_matrix = np.matrix([[np.cos(deg), np.sin(deg)],
                                 [-np.sin(deg), np.cos(deg)]])
    return rotation_matrix * vec
