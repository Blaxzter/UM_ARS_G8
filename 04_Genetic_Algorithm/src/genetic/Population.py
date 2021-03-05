from typing import List

import src.utils.Constants as Const
from src.genetic.Genome import Genome


def distance(individual_1, individual_2):
    return sum([abs(individual_1.genes[i] - individual_2.genes[i])/abs(Const.GENOME_BOUNDS * 2) for i in range(Const.GENOME_LENGTH)])/Const.GENOME_LENGTH



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

    def compute_diversity(self):
        diversity = 0
        comparisons = 0
        for i in range(len(self.individuals)):
            for j in range(len(self.individuals)):
                if i != j:
                    diversity += distance(self.individuals[i], self.individuals[j])
                    comparisons += 1
        return 100 * diversity/comparisons


