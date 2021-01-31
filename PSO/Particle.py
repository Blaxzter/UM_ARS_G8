from typing import Callable
from PSO.Position import Position
from PSO.Velocity import Velocity
import numpy as np



class Particle:
    MAX_POS = 1000
    MIN_POS = 0
    MAX_VEL = 1
    MIN_VEL = 0.1
    W = 0.5
    C1 = 1
    C2 = 1

    def __init__(self):
        self.position: Position = Position(                 # Current Particle position
            np.random.uniform(self.MIN_POS, self.MAX_POS),
            np.random.uniform(self.MIN_POS, self.MAX_POS)
        )
        self.velocity: Velocity = Velocity(              # Current Particle velocity
            np.random.uniform(self.MIN_VEL, self.MAX_VEL),
            np.random.uniform(self.MIN_VEL, self.MAX_VEL)
        )
        self.personal_best_location: Position = None        # All time best location reached
        self.personal_best_altitude: float = -1.            # Altitude of the best location so far

    def evaluate(self, function: Callable[[Position], float]) -> float:
        current_altitude: float = function(self.position)

        if current_altitude < self.personal_best_altitude or (self.personal_best_altitude == -1):
            self.personal_best_altitude = current_altitude
            self.personal_best_location = self.position

        return current_altitude

    def update_velocity(self, team_best: Position) -> None:

        current_velocity_x = self.W * self.velocity.x
        current_velocity_y = self.W * self.velocity.y

        cognitive_velocity_x = self.C1 * (self.personal_best_location.x - self.position.x)
        cognitive_velocity_y = self.C1 * (self.personal_best_location.y - self.position.y)

        social_velocity_x = self.C2 * (team_best.x - self.position.x)
        social_velocity_y = self.C2 * (team_best.y - self.position.y)

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

        if self.position.x > self.MAX_POS:
            self.position.x = self.MAX_POS
        if self.position.y > self.MAX_POS:
            self.position.y = self.MAX_POS

        if self.position.x < self.MIN_POS:
            self.position.x = self.MIN_POS
        if self.position.y < self.MIN_POS:
            self.position.y = self.MIN_POS
