import numpy as np

from src.genetic import Genome

# todo write some other mutation operators
from src.utils.Constants import SEARCH_SPACE


def mutation(genome: Genome):
    for i in range(len(genome.genes)):
        if np.random.uniform(low = 0, high = 1) < 0.08:
            genome.genes[i] = np.random.uniform(low = -SEARCH_SPACE, high = SEARCH_SPACE)
    return genome

def mutationInt(genome: Genome):
    for i in range(len(genome.genes)):
        if np.random.uniform(low = 0, high = 1) < 0.08:
            genome.genes[i] = np.random.randint(low = -SEARCH_SPACE, high = SEARCH_SPACE)
    return genome