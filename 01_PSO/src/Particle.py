import math
from typing import Callable, List
from Position import Position
from Velocity import Velocity
import Constants as Const

import numpy as np


class Particle:
    index = 0

    def __init__(self):
        self.id = Particle.index
        Particle.index = Particle.index + 1
        self.position: Position = Position(  # Current Particle position
            np.random.uniform(low=Const.MIN_POS, high=Const.MAX_POS, size=(Const.DIMENSION,))
        )
        self.velocity: Velocity = Velocity(  # Current Particle velocity
            np.random.uniform(low=Const.MIN_VEL, high=Const.MAX_VEL, size=(Const.DIMENSION,))
        )
        self.personal_best_location: Position = None    # All time best location reached
        self.personal_best_altitude: float = math.nan   # Altitude of the best location so far
        self.altitude_history: List[float] = []         # History of all the altitudes reached by the particle

        self.position_history: List[np.ndarray] = []
        self.velocity_history: List[np.ndarray] = []

    def evaluate(self, function: Callable[[np.ndarray], float]) -> float:
        current_altitude: float = function(self.position.vec)
        self.altitude_history.append(current_altitude)

        if math.isnan(self.personal_best_altitude) or current_altitude < self.personal_best_altitude:
            self.personal_best_altitude = current_altitude
            self.personal_best_location = self.position

        return current_altitude

    def update_velocity(self, team_best: Position) -> None:

        current_velocity = Const.W * self.velocity.vec

        random_cognitive = np.random.random()
        random_social = np.random.random()

        cognitive_velocity = Const.C1 * random_cognitive * (self.personal_best_location.vec - self.position.vec)
        social_velocity = Const.C2 * random_social * (team_best.vec - self.position.vec)

        velocity = current_velocity + cognitive_velocity + social_velocity
        self.velocity.vec = np.clip(velocity, Const.MIN_VEL, Const.MAX_VEL) * Const.SPEED

        # Store velocity for graphs
        self.velocity_history.append(self.velocity.vec)

    def update_position(self) -> None:
        # Should this be square? GUI: ??
        self.position.vec = np.clip(self.velocity.vec + self.position.vec, Const.MIN_POS, Const.MAX_POS)

        # Store position for graph
        self.position_history.append(self.position.vec)
