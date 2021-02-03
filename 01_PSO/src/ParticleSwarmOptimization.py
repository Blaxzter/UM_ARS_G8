from typing import Callable, List
import Constants as Const
from Swarm import Swarm

import numpy as np


class PSO:
    def __init__(self, function: Callable[[np.ndarray], float]):
        self.team = Swarm(Const.N_PARTICLES)  # Object that holds every particle and shares info
        self.environment: Callable[[np.ndarray], float] = function  # Function used for which the min has to be found
        self.altitude_history: List[float] = []
        self.avg_history: List[float] = []
        self.history = {i: [] for i in range(0, Const.N_ITERATIONS)}

    def optimize(self):
        for i in range(Const.N_ITERATIONS):
            avg_altitude = self.team.update(self.environment)
            self.avg_history.append(avg_altitude)
            self.altitude_history.append(self.team.altitude_history[-1])
            for particle in self.team.particles:
                self.history.get(i).append(particle.position.vec)
