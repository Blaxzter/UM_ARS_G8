import math
import numpy as np

from typing import List

from src.utils.Constants import GENOME_LENGTH, SEARCH_SPACE


class Genome:
    def __init__(self, genes: List = None):
        if genes is None:
            self.genes: np.ndarray = self.init_genome()
        else:
            self.genes = genes
        self.fitness: float = math.nan

    def set_fitness(self, fitness):
        self.fitness = fitness

    @staticmethod
    def init_genome():
        return np.random.randint(low = -SEARCH_SPACE, high = SEARCH_SPACE, size = GENOME_LENGTH)  # np.random.rand(GENOME_LENGTH) * 0.1

    def get_fitness(self):
        return self.fitness
