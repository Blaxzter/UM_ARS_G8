from typing import List

from src.simulator.Line import Line
from src.utils.Constants import *

default_boundaries = [
    Line(PADDING, PADDING_TOP, WIDTH - PADDING, PADDING_TOP),
    Line(WIDTH - PADDING, PADDING_TOP, WIDTH - PADDING, HEIGHT - PADDING),
    Line(WIDTH - PADDING, HEIGHT - PADDING, PADDING, HEIGHT - PADDING),
    Line(PADDING, HEIGHT - PADDING, PADDING, PADDING_TOP),
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
        np.array([ORIGIN[0] + ROBOT_RADIUS + 10, ORIGIN[1] + ROBOT_RADIUS + 10]).reshape(2, 1)  # Initial Position
    ),

    # Room 2
    (
        default_boundaries + [
            Line(ORIGIN[0], ORIGIN[1], ORIGIN[0] + MAP_WIDTH, ORIGIN[1] + MAP_HEIGHT)
        ],  # Map
        np.array([ORIGIN[0] + MAP_WIDTH - ROBOT_RADIUS - 10, ORIGIN[1] + ROBOT_RADIUS + 10]).reshape(2, 1)  # Initial Position
    ),

    # Room 3 - Box with robot inside
    (
        default_boundaries + box([ORIGIN[0] + MAP_WIDTH * 2 / 5, ORIGIN[1] + MAP_HEIGHT * 2 / 5], 150, 100),  # Map
        np.array([ORIGIN[0] + MAP_WIDTH / 2, ORIGIN[1] + MAP_HEIGHT / 2]).reshape(2, 1)  # Initial Position
    )
]


class Room:
    """
    Author Guillaume Franzoni Darnois
    """

    def __init__(self, room: int):
        self.map: List[Line] = rooms[room][0]
        self.initial_random_pos: np.ndarray = rooms[room][1]
