from typing import Callable, List
import Constants as Const
from Swarm import Swarm

import numpy as np


class PSO:
    def __init__(self, function: Callable[[np.ndarray], float]):
        self.swarms: List[Swarm] = self.init_swarms(Const.N_SWARMS, function)  # Object that holds every particle and shares info
        self.environment: Callable[[np.ndarray], float] = function             # Function used for which the min has to be found
        self.best_altitude_history: List[float] = []
        self.average_altitude_history: List[float] = []
        self.average_velocity_history: List[float] = []
        self.history = {i: [] for i in range(0, Const.N_ITERATIONS)}

    def optimize(self):
        for i in range(Const.N_ITERATIONS):
            total_average_altitude: float = 0
            total_average_velocity: float = 0
            best_altitude: float = np.inf

            for swarm in self.swarms:
                avg_history, avg_velocity = swarm.update()
                total_average_velocity += avg_velocity
                total_average_altitude += avg_history
                if swarm.altitude_history[-1] < best_altitude:
                    best_altitude = swarm.best_altitude

                self.create_particle_data(i, swarm)

            self.average_altitude_history.append(total_average_altitude / len(self.swarms))
            self.average_velocity_history.append(total_average_velocity * 100 / len(self.swarms))
            self.best_altitude_history.append(best_altitude)

    def create_particle_data(self, i, swarm: Swarm):
        for particle in swarm.particles:
            self.history.get(i).append(
                dict(
                    id=particle.id,
                    alt=particle.altitude_history[-1],
                    best=particle.found_the_best,
                    pos=particle.position,
                    vel=particle.velocity,
                    swarm=self.swarms.index(swarm)
                )
            )

    @staticmethod
    def init_swarms(number_swarms: int, function: Callable[[np.ndarray], float]):
        return [Swarm(Const.N_PARTICLES, function) for _ in range(number_swarms)]
