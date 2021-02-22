from typing import List

import pygame
from pygame import gfxdraw

from src.Environment import Environment
from src.MathUtils import *


class Sensors:
    def __init__(self):
        self.sensors: List[LineString] = []  # Collection of all the sensor in a Robot

    def update(self, environment: Environment, sensor_orientation: float, robot_center: np.ndarray) -> None:
        self.sensors.clear()
        robot_center_x, robot_center_y = get_x_y(robot_center)

        for _ in range(Const.NUMBER_OF_SENSORS):
            # Recalculate new sensor orientation with 360 /  degrees offset from the previous one
            sensor_start_x, sensor_start_y = self.get_orientation_vector(robot_center, sensor_orientation)

            # For every boundary in the map calculate the intersection if there is one and it's the best
            sensor_intersection = None
            distance_closest_intersection = np.inf

            for line in environment.environment:
                intersection = intersection_semiline_segment(
                    line,
                    (robot_center_x, robot_center_y),
                    (sensor_start_x, sensor_start_y)
                )

                if intersection.size != 0:
                    intersection_x, intersection_y = get_x_y(intersection)
                    temp_distance = distance_point_to_point(
                        (sensor_start_x, sensor_start_y),
                        (intersection_x, intersection_y)
                    )
                    if temp_distance < distance_closest_intersection:
                        distance_closest_intersection = temp_distance
                        sensor_intersection = intersection
                else:
                    continue

            # Append sensor segment to the list of sensor to be drawn after the update
            self.sensors.append(
                LineString([
                    [sensor_start_x, sensor_start_y],
                    [sensor_intersection[0, 0], sensor_intersection[1, 0]]
                ])
            )
            # Update degrees for next sensor
            sensor_orientation = sensor_orientation + np.deg2rad(360 / Const.NUMBER_OF_SENSORS)

    def draw(self, screen: pygame.display) -> None:
        for sensor in self.sensors:
            gfxdraw.line(
                screen,
                int(np.round(sensor.coords.xy[0][0])),
                int(np.round(sensor.coords.xy[1][0])),
                int(np.round(sensor.coords.xy[0][1])),
                int(np.round(sensor.coords.xy[1][1])),
                Const.COLORS['red']
            )
            screen.blit(
                Const.FONT_SENSORS.render(
                    f'{np.round(sensor.length if sensor.length > 0 else 0.0, decimals=1)}',
                    True,
                    Const.COLORS["white"]
                ),
                (
                    int(np.round(sensor.coords.xy[0][1])),
                    int(np.round(sensor.coords.xy[1][1]))
                )
            )

    @staticmethod
    def get_orientation_vector(pos: np.ndarray, degree: float) -> (float, float):
        default_vec = np.array([Const.ROBOT_RADIUS, 0]).reshape((2, 1))
        rotated = rotate(default_vec, degree)
        vec = pos + rotated
        return vec[0, 0], vec[1, 0]
