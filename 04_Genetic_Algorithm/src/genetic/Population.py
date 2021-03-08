from typing import List

import numpy as np

import utils.Constants as Const
from genetic.Genome import Genome


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
        self.individuals = list(sorted(self.individuals, key = lambda genome: genome.get_fitness(), reverse = True))[:show_best]
        pass

    def compute_diversity(self):
        if len(self.individuals) < 2:
            return 0
        diversity = 0
        comparisons = 0
        for i in range(len(self.individuals)):
            for j in range(len(self.individuals)):
                if i != j:
                    gene1 = np.array(self.individuals[i].genes)
                    gene2 = np.array(self.individuals[j].genes)

                    diversity += np.linalg.norm(gene1 - gene2)
                    comparisons += 1
        return diversity
