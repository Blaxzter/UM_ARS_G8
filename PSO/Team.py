from typing import Tuple, List
from PSO.Particle import Particle
from PSO.Position import Position


class Team:
    def __init__(self, n_particles: int):
        self.particles: List[Particle] = self.init_particles(n_particles)
        self.best_location: Position = None
        self.best_altitude: float = -1.

    @staticmethod
    def init_particles(n_particles: int) -> List[Particle]:
        return [Particle() for i in range(n_particles)]
