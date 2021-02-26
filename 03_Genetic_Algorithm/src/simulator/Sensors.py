from typing import List

import pygame
from pygame import gfxdraw

from src.simulator.Environment import Environment
from src.utils.MathUtils import *
from src.utils.Constants import DRAW

# Mostly done by Teo


class Sensors:
    def __init__(self):
        self.sensors: List[LineString] = []  # Collection of all the sensor in a Robot
        if DRAW:
            self.font_sensors = pygame.font.SysFont(None, 28)  #

    def update(self, environment: Environment, sensor_orientation: float, robot_center: np.ndarray) -> None:
        self.sensors.clear()
        robot_center_x, robot_center_y = get_x_y(robot_center)

        for _ in range(Const.NUMBER_OF_SENSORS):
            # Recalculate new sensor orientation with 360 /  degrees offset from the previous one
            n_vec_orient = self.get_orientation_vector(sensor_orientation)
            pos_on_edge = robot_center + n_vec_orient * Const.ROBOT_RADIUS
            sensor_start_x = pos_on_edge[0, 0]
            sensor_start_y = pos_on_edge[1, 0]

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

            end_point_x = sensor_intersection[0, 0]
            end_point_y = sensor_intersection[1, 0]
            if distance_closest_intersection > Const.SENSOR_MAX_LENGTH:
                end_pos = robot_center + n_vec_orient * (Const.SENSOR_MAX_LENGTH + Const.ROBOT_RADIUS)
                end_point_x = end_pos[0, 0]
                end_point_y = end_pos[1, 0]

            # Append sensor segment to the list of sensor to be drawn after the update
            self.sensors.append(
                LineString([
                    [sensor_start_x, sensor_start_y],
                    [end_point_x, end_point_y]
                ])
            )
            # Update degrees for next sensor
            sensor_orientation = sensor_orientation + np.deg2rad(360 / Const.NUMBER_OF_SENSORS)

    def draw(self, screen) -> None:
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
                self.font_sensors.render(
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
    def get_orientation_vector(degree: float) -> (float, float):
        default_vec = np.array([1, 0]).reshape((2, 1))
        rotated = rotate(default_vec, degree)
        return rotated
