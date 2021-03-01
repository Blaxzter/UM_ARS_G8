from typing import List

from src.simulator.Line import Line
from src.utils.Constants import *


class Room:
    """
    Author Guillaume Franzoni Darnois
    """
    def __init__(self, room: int):
        self.map: List[Line] = rooms[room][0]
        self.initial_random_pos: np.ndarray = rooms[room][1]
        self.dust: np.ndarray = self.generate_dust()

    @staticmethod
    def generate_dust() -> np.ndarray:
        n = int(MAP_WIDTH * MAP_HEIGHT / ROBOT_RADIUS)
        xy_min = ORIGIN
        xy_max = [MAP_WIDTH, MAP_HEIGHT]
        return np.random.uniform(low=xy_min, high=xy_max, size=(n, 2))


default_boundaries = [
    Line(PADDING, PADDING_TOP, WIDTH - PADDING, PADDING_TOP),
    Line(WIDTH - PADDING, PADDING_TOP, WIDTH - PADDING, HEIGHT - PADDING),
    Line(WIDTH - PADDING, HEIGHT - PADDING, PADDING, HEIGHT - PADDING),
    Line(PADDING, HEIGHT - PADDING, PADDING, PADDING_TOP),
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
    )
]
