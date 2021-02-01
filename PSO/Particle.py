from typing import Callable, List
from PSO.Position import Position
from PSO.Velocity import Velocity
import PSO.Constants as Const
import numpy as np



class Particle:
    def __init__(self):
        self.position: Position = Position(                 # Current Particle position
            np.random.uniform(Const.MIN_POS, Const.MAX_POS),
            np.random.uniform(Const.MIN_POS, Const.MAX_POS)
        )
        self.velocity: Velocity = Velocity(                 # Current Particle velocity
            np.random.uniform(Const.MIN_VEL, Const.MAX_VEL),
            np.random.uniform(Const.MIN_VEL, Const.MAX_VEL)
        )
        self.personal_best_location: Position = None        # All time best location reached
        self.personal_best_altitude: float = -1.            # Altitude of the best location so far
        self.altitude_history: List[float] = []             # History of all the altitudes reached by the particle

    def evaluate(self, function: Callable[[float, float], float]) -> float:
        current_altitude: float = function(self.position.x, self.position.y)
        self.altitude_history.append(current_altitude)

        if current_altitude < self.personal_best_altitude or (self.personal_best_altitude == -1):
            self.personal_best_altitude = current_altitude
            self.personal_best_location = self.position

        return current_altitude

    def update_velocity(self, team_best: Position) -> None:

        current_velocity_x = Const.W * self.velocity.x
        current_velocity_y = Const.W * self.velocity.y

        cognitive_velocity_x = Const.C1 * np.random.random() * (self.personal_best_location.x - self.position.x)
        cognitive_velocity_y = Const.C1 * np.random.random() * (self.personal_best_location.y - self.position.y)

        social_velocity_x = Const.C2 * np.random.random() * (team_best.x - self.position.x)
        social_velocity_y = Const.C2 * np.random.random() * (team_best.y - self.position.y)

        self.velocity.x = (
            current_velocity_x +
            cognitive_velocity_x +
            social_velocity_x
        )
        self.velocity.y = (
                current_velocity_y +
                cognitive_velocity_y +
                social_velocity_y
        )

    def update_position(self) -> None:
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y

        if self.position.x > Const.MAX_POS:
            self.position.x = Const.MAX_POS
        if self.position.y > Const.MAX_POS:
            self.position.y = Const.MAX_POS

        if self.position.x < Const.MIN_POS:
            self.position.x = Const.MIN_POS
        if self.position.y < Const.MIN_POS:
            self.position.y = Const.MIN_POS
