import math
from typing import Callable, List

import Constants as Const

import numpy as np


class Particle:
    index = 0

    def __init__(self, function: Callable[[np.ndarray], float]):
        self.id = Particle.index
        Particle.index = Particle.index + 1
        self.W = Const.W_S
        self.position: np.ndarray = np.random.uniform(low=Const.MIN_POS, high=Const.MAX_POS, size=(Const.DIMENSION, 1))
        self.velocity: np.ndarray = np.random.uniform(low=Const.MIN_VEL, high=Const.MAX_VEL, size=(Const.DIMENSION, 1))

        self.function = function
        self.personal_best_location: np.ndarray = None          # All time best location reached
        self.personal_best_altitude: float = math.nan           # Altitude of the best location so far
        self.altitude = math.nan
        self.altitude_history: List[float] = []                 # History of all the altitudes reached by the particle
        self.found_the_best = False

        self.position_history: List[np.ndarray] = [self.position]
        self.velocity_history: List[np.ndarray] = [self.velocity]

    def evaluate(self) -> float:
        current_altitude: float = self.function(self.position)
        self.altitude = current_altitude
        self.altitude_history.append(current_altitude)

        if math.isnan(self.personal_best_altitude) or current_altitude < self.personal_best_altitude:
            self.personal_best_altitude = current_altitude
            self.personal_best_location = self.position

        return current_altitude

    def update_velocity(self, team_best: np.ndarray) -> None:
        current_velocity = self.W * self.velocity
        self.W -= (Const.W_S - Const.W_E) / Const.N_ITERATIONS

        random_cognitive = np.random.random() / 0.5
        random_social = np.random.random() / 0.5

        cognitive_velocity = Const.C1 * random_cognitive * (self.personal_best_location - self.position)
        social_velocity = Const.C2 * random_social * (team_best - self.position)

        velocity = current_velocity + cognitive_velocity + social_velocity
        self.velocity = np.clip(velocity, Const.MIN_VEL, Const.MAX_VEL)

        # Store velocity for graphs
        self.velocity_history.append(self.velocity)

    def update_position(self) -> None:
        new_pos = self.position + self.velocity * Const.SPEED

        if Const.BOUNCE_BACK:
            for coordinate in new_pos:
                if coordinate > Const.MAX_POS or coordinate < Const.MIN_POS:
                    self.velocity = np.rot90(self.velocity, k=2)
                    new_pos = self.position + self.velocity * Const.SPEED

        self.position = np.clip(new_pos, Const.MIN_POS, Const.MAX_POS)

        # Store position for graph
        self.position_history.append(self.position)
