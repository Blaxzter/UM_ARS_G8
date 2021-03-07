import math
import numpy as np

from typing import List

import utils.Constants as Const
from simulator.Room import Room


class Genome:
    """
    Author Frederic Abraham & Guillaume Franzoni Darnois
    """

    def __init__(self, genes: List = None, fitness=math.nan):
        if genes is None:
            self.genes: np.ndarray = self.init_genome()
        else:
            self.genes = genes
        self.fitness = {i: 0 for i in range(len(Room.rooms))}

    def set_fitness(self, fitness, room):
        self.fitness[room] = fitness

    @staticmethod
    def init_genome():
        return np.random.rand(Const.GENOME_LENGTH) * Const.INIT_SIZE - (Const.INIT_SIZE / 2)

    def get_fitness(self):
        return np.mean(list(self.fitness.values()))

    def get_fitness_by_key(self, key):
        return self.fitness[key]
