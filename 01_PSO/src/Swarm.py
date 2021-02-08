"""
Author Guillaume Franzoni Darnois
"""

import math
from typing import List, Callable, Tuple

import numpy as np
import Constants as Const

from Particle import Particle


class Swarm:
    def __init__(self, n_particles: int, environment: Callable[[np.ndarray], float]):
        self.environment: Callable[[np.ndarray], float] = environment
        self.particles: List[Particle] = self.init_particles(n_particles, self.environment)  # List of particles in the environment
        self.best_location: np.ndarray = None  # Best location achieved overall
        self.best_altitude: float = math.nan  # Altitude of the best location
        self.altitude_history: List[float] = []  # History of all the altitude changes

    def update(self) -> Tuple[float, float]:
        tot_altitude = 0
        tot_velocity = 0
        best_particle = None
        for particle in self.particles:
            particle_altitude = particle.evaluate()
            tot_altitude += particle_altitude

            if math.isnan(self.best_altitude) or particle_altitude < self.best_altitude:
                best_particle = particle
                self.best_altitude = particle_altitude
                self.best_location = particle.position

        # Set the best new particle
        if best_particle is not None:
            for particle in self.particles:
                particle.found_the_best = False
            best_particle.found_the_best = True
            self.best_altitude = best_particle.altitude

        self.altitude_history.append(self.best_altitude)

        for particle in self.particles:
            particle.update_velocity(self.best_location)
            particle.update_position()
            tot_velocity += np.linalg.norm(particle.velocity_history[-1])

        return np.round(tot_altitude / float(len(self.particles)), decimals=Const.precision), np.round(
            tot_velocity / float(len(self.particles)), decimals=Const.precision)

    @staticmethod
    def init_particles(n_particles: int, environment: Callable[[np.ndarray], float]) -> List[Particle]:
        return [Particle(environment) for i in range(n_particles)]
