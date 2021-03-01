import math
import numpy as np

from typing import List

from src.utils.Constants import VALUES_PER_AXIS, DIMENSION, MAX_POS, MIN_POS


class Genome:
    """
    Author Frederic Abraham & Guillaume Franzoni Darnois
    """
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
        # return list(np.repeat(np.random.uniform(low = MAX_POS - (MAX_POS / 3), high = MAX_POS, size = (DIMENSION, 1)), VALUES_PER_AXIS))  # np.random.rand(GENOME_LENGTH) * 0.1
        return list(np.repeat(np.random.uniform(low = MIN_POS, high = MAX_POS, size = (DIMENSION, 1)), VALUES_PER_AXIS))  # np.random.rand(GENOME_LENGTH) * 0.1

    def get_fitness(self):
        return self.fitness
