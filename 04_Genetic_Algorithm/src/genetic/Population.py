from typing import List

import src.utils.Constants as Const
from src.genetic.Genome import Genome


class Population:
    """
    Author Frederic Abraham
    """

    def __init__(self, individuals: List = None):
        if individuals is None:
            self.individuals: List[Genome] = [Genome() for _ in range(Const.N_INDIVIDUALS)]
        else:
            self.individuals: List[Genome] = individuals

    def get_top(self, show_best):
        self.individuals = list(sorted(self.individuals, key = lambda genome: genome.fitness, reverse = True))[:show_best]
        pass
