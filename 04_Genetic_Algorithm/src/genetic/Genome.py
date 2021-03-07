import math
import numpy as np

from typing import List

import utils.Constants as Const


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
        return np.random.rand(Const.GENOME_LENGTH) * Const.INIT_SIZE - (Const.INIT_SIZE / 2)

    def get_fitness(self):
        return self.fitness
