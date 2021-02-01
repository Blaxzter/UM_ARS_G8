from typing import Callable
import PSO.Constants as Const
from PSO.Team import Team


class PSO:
    def __init__(self, function: Callable[[float, float], float], plot):
        self.team = Team(Const.N_PARTICLES)                           # Object that holds every particle and shares info
        self.environment: Callable[[float, float], float] = function  # Function used for which the min has to be found
        self.plot = plot

    def optimize(self, ax):
        # for i in range(Const.N_ITERATIONS): # ---Not used since the iteration is made through animation frames
        self.team.update(self.environment, self.plot)
        return ax
