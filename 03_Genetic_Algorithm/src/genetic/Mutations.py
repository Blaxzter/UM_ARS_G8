import numpy as np

from src.genetic import Genome

# todo write some other mutation operators

def mutation(genome: Genome):
    for i in range(len(genome.genes)):
        if np.random.uniform(low = 0, high = 1) < 0.08:
            genome.genes[i] += np.random.uniform(low = 0, high = 1)
    return genome