from typing import Callable, Tuple
from typing import List
import PSO.Constants as Const
from PSO.Position import Position
from PSO.Team import Team


class PSO:
    def __init__(self, function: Callable[[Position], float]):
        self.team = Team(Const.N_PARTICLES)                         # Object that holds every particle and shares info
        self.environment: Callable[[Position], float] = function    # Function used for which the min has to be found

    def optimize(self) -> None:
        for i in range(Const.N_ITERATIONS):
            self.team.update(self.environment)
