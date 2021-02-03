from typing import Callable, List
import Constants as Const
from Swarm import Swarm

import numpy as np


class PSO:
    def __init__(self, function: Callable[[np.ndarray], float]):
        self.team = Swarm(Const.N_PARTICLES)  # Object that holds every particle and shares info
        self.environment: Callable[[np.ndarray], float] = function  # Function used for which the min has to be found
        self.best_altitude_history: List[float] = []
        self.average_altitude_history: List[float] = []
        self.average_velocity_history: List[float] = []
        self.history = {i: [] for i in range(0, Const.N_ITERATIONS)}

    def optimize(self):
        for i in range(Const.N_ITERATIONS):
            avg_history, avg_velocity = self.team.update(self.environment)
            self.average_altitude_history.append(avg_history)
            self.average_velocity_history.append(avg_velocity * 100)  # times 100 to have the percentage
            self.best_altitude_history.append(self.team.altitude_history[-1])
            for particle in self.team.particles:
                self.history.get(i).append(
                    dict(
                        id=particle.id,
                        alt=particle.altitude_history[-1],
                        best=particle.altitude_history[-1] == self.team.altitude_history[-1],
                        pos=particle.position.vec
                    )
                )
