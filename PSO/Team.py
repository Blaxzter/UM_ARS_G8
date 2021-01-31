from typing import List, Callable
from PSO.Particle import Particle
from PSO.Position import Position


class Team:
    def __init__(self, n_particles: int):
        self.particles: List[Particle] = self.init_particles(n_particles)   # List of particles in the environment
        self.best_location: Position = None                                 # Best location achieved overall
        self.best_altitude: float = -1.                                     # Altitude of the best location
        self.altitude_history: List[float] = []                             # History of all the altitude changes

    def update(self, environment: Callable[[Position], float]) -> None:
        for particle in self.particles:
            particle_altitude = particle.evaluate(environment)

            if particle_altitude < self.best_altitude or self.best_altitude == -1:
                self.best_altitude = particle_altitude
                self.best_location = particle.position
                self.altitude_history.append(self.best_altitude)

        for particle in self.particles:
            particle.update_velocity(self.best_location)
            particle.update_position()

    @staticmethod
    def init_particles(n_particles: int) -> List[Particle]:
        return [Particle() for i in range(n_particles)]
