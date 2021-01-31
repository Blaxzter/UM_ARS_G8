from typing import Callable, Tuple
from typing import List
import PSO.Constants as Const
from PSO.Position import Position
from PSO.Team import Team


class PSO:
    def __init__(self, function: Callable[[Position], float]):
        self.team = Team(Const.N_PARTICLES)
        self.environment: Callable[[Position], float] = function

    def iteration(self) -> Tuple[Position, float]:
        for particle in self.team.particles:
            particle_altitude = particle.evaluate(self.environment)

            if particle_altitude < self.team.best_altitude or self.team.best_altitude == -1:
                self.team.best_altitude = particle_altitude
                self.team.best_location = particle.position

        for particle in self.team.particles:
            particle.update_velocity(self.team.best_location)
            particle.update_position()

        return self.team.best_location, self.team.best_altitude

    def optimize(self) -> List[Tuple[Position, float]]:
        optimization_history: List = []

        for i in range(Const.N_ITERATIONS):
            position, altitude = self.iteration()
            optimization_history.append((position, altitude))

        return optimization_history
