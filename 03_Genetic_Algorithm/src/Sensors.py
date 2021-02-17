from typing import List

from pygame import gfxdraw
from shapely.geometry import LineString

from src.MathUtils import *

class Sensors:
    def __init__(self):
        self.sensors: List[LineString] = []

    def get_orientation_vector(self, pos, degree):
        default_vec = np.array([Const.robot_radius, 0]).reshape((2, 1))
        rotated = rotate(default_vec, degree)
        vec = pos + rotated
        return vec[0, 0], vec[1, 0]

    def update(self, environment, sensor_orientation, robot_center):
        self.sensors.clear()
        robot_center_x, robot_center_y = get_x_y(robot_center)

        for _ in range(Const.number_of_sensors):
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

                if intersection is not None:
                    intersection_x, intersection_y = get_x_y(intersection)
                    temp_distance = distance_point_to_point(
                        [sensor_start_x, sensor_start_y],
                        [intersection_x, intersection_y]
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
            sensor_orientation = sensor_orientation + np.deg2rad(360 / Const.number_of_sensors)

    def draw(self, screen):
        for sensor in self.sensors:
            gfxdraw.line(
                screen,
                int(np.round(sensor.coords.xy[0][0])),
                int(np.round(sensor.coords.xy[1][0])),
                int(np.round(sensor.coords.xy[0][1])),
                int(np.round(sensor.coords.xy[1][1])),
                Const.colors['red']
            )
            screen.blit(
                Const.font_sensor.render(
                    f'{np.round(sensor.length if sensor.length > 0 else 0.0, decimals=1)}',
                    True,
                    Const.colors["white"]
                ),
                (
                    int(np.round(sensor.coords.xy[0][1])),
                    int(np.round(sensor.coords.xy[1][1]))
                )
            )