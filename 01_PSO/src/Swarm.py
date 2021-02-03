from typing import List, Callable, Tuple

import numpy as np
import Constants as Const

from Particle import Particle
from Position import Position


class Swarm:
    def __init__(self, n_particles: int):
        self.particles: List[Particle] = self.init_particles(n_particles)  # List of particles in the environment
        self.best_location: Position = None  # Best location achieved overall
        self.best_altitude: float = -1.  # Altitude of the best location
        self.altitude_history: List[float] = []  # History of all the altitude changes

    def update(self, environment: Callable[[np.ndarray], float]) -> Tuple[float, float]:
        tot_altitude = 0
        tot_velocity = 0
        for particle in self.particles:
            particle_altitude = particle.evaluate(environment)
            tot_altitude += particle_altitude

            if particle_altitude < self.best_altitude or self.best_altitude == -1:
                self.best_altitude = particle_altitude
                self.best_location = particle.position
                self.altitude_history.append(self.best_altitude)

        for particle in self.particles:
            particle.update_velocity(self.best_location)
            particle.update_position()
            tot_velocity += np.linalg.norm(particle.velocity_history[-1])

        return np.round(tot_altitude / float(len(self.particles)), decimals=Const.precision), np.round(tot_velocity / float(len(self.particles)), decimals=Const.precision)

    @staticmethod
    def init_particles(n_particles: int) -> List[Particle]:
        return [Particle() for i in range(n_particles)]
