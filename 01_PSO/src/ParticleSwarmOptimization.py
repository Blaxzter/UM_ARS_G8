from typing import Callable
import Constants as Const
from Swarm import Swarm

import numpy as np


class PSO:
    def __init__(self, function: Callable[[np.ndarray], float]):
        self.team = Swarm(Const.N_PARTICLES)  # Object that holds every particle and shares info
        self.environment: Callable[[np.ndarray], float] = function  # Function used for which the min has to be found

    def optimize(self):
        for i in range(Const.N_ITERATIONS):
            self.team.update(self.environment)
