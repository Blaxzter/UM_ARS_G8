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


def trapezoid(origin, width, height):
    return [
        Line(origin[0] + 5 / 100 * Const.MAP_WIDTH, origin[1], origin[0], origin[1] + height),
        Line(origin[0], origin[1] + height, origin[0] + width, origin[1] + height),
        Line(origin[0] + width, origin[1] + height, origin[0] + width - 5 / 100 * Const.MAP_WIDTH, origin[1]),
        Line(origin[0] + width - 5 / 100 * Const.MAP_WIDTH, origin[1], origin[0] + 5 / 100 * Const.MAP_WIDTH,
             origin[1]),
    ]


class Room:
    """
    Author Guillaume Franzoni Darnois & Theodoros Giannilias
    """

    rooms = [

        # Room 1
        (
            default_boundaries,  # Map
            [
                [Const.ORIGIN[0] + Const.ROBOT_RADIUS + 10, Const.ORIGIN[1] + Const.ROBOT_RADIUS + 10],
                # Top left corner
                [Const.ORIGIN[0] + Const.MAP_WIDTH - Const.ROBOT_RADIUS - 10,
                 Const.ORIGIN[1] + Const.ROBOT_RADIUS + 10],  # top right
                [Const.ORIGIN[0] + Const.MAP_WIDTH - Const.ROBOT_RADIUS - 10,
                 Const.ORIGIN[1] + Const.MAP_HEIGHT - Const.ROBOT_RADIUS - 10],  # Bottom right
                [Const.ORIGIN[0] + Const.ROBOT_RADIUS + 10,
                 Const.ORIGIN[1] + Const.MAP_HEIGHT - Const.ROBOT_RADIUS - 10],  # Bottom Left

                [Const.ORIGIN[0] + Const.MAP_WIDTH / 2, Const.ORIGIN[1] + Const.MAP_HEIGHT / 2]  # Middle
            ]
        ),

        # Room 2
        (
            default_boundaries + [
                Line(Const.ORIGIN[0], Const.ORIGIN[1], Const.ORIGIN[0] + Const.MAP_WIDTH, Const.ORIGIN[1] + Const.MAP_HEIGHT)
            ],  # Map
            [
                [Const.ORIGIN[0] + Const.MAP_WIDTH - Const.ROBOT_RADIUS - 10, Const.ORIGIN[1] + Const.ROBOT_RADIUS + 10]
            ]
        ),

        # Room 3 - Box with robot inside
        (
            default_boundaries + box(
                [Const.ORIGIN[0] + Const.MAP_WIDTH * 2 / 5, Const.ORIGIN[1] + Const.MAP_HEIGHT * 2 / 5], 150, 100),
            # Map
            [
                [Const.ORIGIN[0] + Const.MAP_WIDTH / 2, Const.ORIGIN[1] + Const.MAP_HEIGHT / 2]
            ]
        ),

        # Room 4 - Trapezoid with trapezoid inside
        (
            trapezoid([Const.ORIGIN[0], Const.ORIGIN[1]], Const.MAP_WIDTH, Const.MAP_HEIGHT) +
            trapezoid([Const.ORIGIN[0] + Const.MAP_WIDTH/4, Const.ORIGIN[1] + Const.MAP_HEIGHT/4], Const.MAP_WIDTH/2, Const.MAP_HEIGHT/2),
            # Map
            [
                [Const.ORIGIN[0] + Const.MAP_WIDTH / 2, Const.ORIGIN[1] + Const.MAP_HEIGHT / 2]
            ]
        ),

        # Room 5 - Maze Map 1
        (
            default_boundaries + [
                Line(200, 400, 200, 200), Line(700, 200, 200, 200), Line(30, 200, 200, 200), Line(600, 400, 600, 200)
            ],
            # Map
            [
                # Top right corner
                [Const.ORIGIN[0] + Const.MAP_WIDTH / 2, Const.ORIGIN[1] + Const.MAP_HEIGHT / 6],
                # Center
                [Const.ORIGIN[0] + Const.MAP_WIDTH / 2, Const.ORIGIN[1] + Const.MAP_HEIGHT / 2]

            ]
        ),

        # Room 6 Propeller
        (
            default_boundaries + [
                Line(Const.ORIGIN[0], Const.ORIGIN[1] , (Const.ORIGIN[0] + Const.MAP_WIDTH) / 2, (Const.ORIGIN[1] + Const.MAP_HEIGHT) / 1.8),
                Line(Const.ORIGIN[0] + Const.MAP_WIDTH, Const.ORIGIN[1], Const.ORIGIN[0]+370, (Const.ORIGIN[1] + Const.MAP_HEIGHT) / 1.8),
                Line(Const.MAP_WIDTH / 1.95, Const.ORIGIN[1] * 2.7, Const.MAP_WIDTH / 1.95,  Const.ORIGIN[1] + Const.MAP_HEIGHT)

            ],
            # Map
            [
                # Top left corner
                [Const.ORIGIN[0] + Const.ROBOT_RADIUS + 10, Const.ORIGIN[1] + Const.ROBOT_RADIUS + 40],
                # Top right corner
                [Const.ORIGIN[0] + Const.MAP_WIDTH - Const.ROBOT_RADIUS - 10,Const.ORIGIN[1] + Const.ROBOT_RADIUS + 40],
                # Bottom right corner
                [Const.ORIGIN[0] + Const.MAP_WIDTH - Const.ROBOT_RADIUS - 10, Const.ORIGIN[1] + Const.MAP_HEIGHT - Const.ROBOT_RADIUS - 10],
                # Bottom left corner
                [Const.ORIGIN[0] + Const.ROBOT_RADIUS + 10, Const.ORIGIN[1] + Const.MAP_HEIGHT - Const.ROBOT_RADIUS - 10],
                # Inside the 2 borders
                [Const.ORIGIN[0] + Const.MAP_WIDTH / 2, Const.ORIGIN[1] + Const.MAP_HEIGHT / 3]
            ]
        )
    ]

    def __init__(self, room: int):
        self.map: List[Line] = self.rooms[room][0]
        self.initial_random_positions = self.rooms[room][1]

    def get_initial_position(self):
        pos_index = np.random.randint(len(self.initial_random_positions))
        return np.array(self.initial_random_positions[pos_index]).reshape((2, 1))
