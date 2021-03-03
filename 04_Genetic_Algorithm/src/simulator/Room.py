from typing import List

import numpy as np

from src.simulator.Line import Line
import src.utils.Constants as Const

default_boundaries = [
    Line(Const.PADDING, Const.PADDING_TOP, Const.WIDTH - Const.PADDING, Const.PADDING_TOP),
    Line(Const.WIDTH - Const.PADDING, Const.PADDING_TOP, Const.WIDTH - Const.PADDING, Const.HEIGHT - Const.PADDING),
    Line(Const.WIDTH - Const.PADDING, Const.HEIGHT - Const.PADDING, Const.PADDING, Const.HEIGHT - Const.PADDING),
    Line(Const.PADDING, Const.HEIGHT - Const.PADDING, Const.PADDING, Const.PADDING_TOP),
]


def box(origin, width, height):
    return [
        Line(origin[0], origin[1], origin[0], origin[1] + height),
        Line(origin[0], origin[1] + height, origin[0] + width, origin[1] + height),
        Line(origin[0] + width, origin[1] + height, origin[0] + width, origin[1]),
        Line(origin[0] + width, origin[1], origin[0], origin[1]),
    ]

rooms = [

    # Room 1
    (
        default_boundaries,  # Map
        np.array([Const.ORIGIN[0] + Const.ROBOT_RADIUS + 10, Const.ORIGIN[1] + Const.ROBOT_RADIUS + 10]).reshape(2, 1)  # Initial Position
    ),

    # Room 2
    (
        default_boundaries + [
            Line(Const.ORIGIN[0], Const.ORIGIN[1], Const.ORIGIN[0] + Const.MAP_WIDTH, Const.ORIGIN[1] + Const.MAP_HEIGHT)
        ],  # Map
        np.array([Const.ORIGIN[0] + Const.MAP_WIDTH - Const.ROBOT_RADIUS - 10, Const.ORIGIN[1] + Const.ROBOT_RADIUS + 10]).reshape(2, 1)  # Initial Position
    ),

    # Room 3 - Box with robot inside
    (
        default_boundaries + box([Const.ORIGIN[0] + Const.MAP_WIDTH * 2 / 5, Const.ORIGIN[1] + Const.MAP_HEIGHT * 2 / 5], 150, 100),  # Map
        np.array([Const.ORIGIN[0] + Const.MAP_WIDTH / 2, Const.ORIGIN[1] + Const.MAP_HEIGHT / 2]).reshape(2, 1)  # Initial Position
    )
]


class Room:
    """
    Author Guillaume Franzoni Darnois
    """

    def __init__(self, room: int):
        self.map: List[Line] = rooms[room][0]
        self.initial_random_pos: np.ndarray = rooms[room][1]
