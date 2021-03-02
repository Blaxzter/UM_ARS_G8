import numpy as np

from src.genetic import Genome

# todo write some other mutation operators
from src.utils.Constants import MUTATION_PROBABILITY, GENOME_BOUNDS

"""
Author Guillaume Franzoni Darnois
"""

def mutation(genome: Genome):
    for i in range(len(genome.genes)):
        if np.random.uniform(low = 0, high = 1) < MUTATION_PROBABILITY:
            genome.genes[i] = np.random.uniform(low = -GENOME_BOUNDS, high = GENOME_BOUNDS)
    return genome


def mutationInt(genome: Genome):
    for i in range(len(genome.genes)):
        if np.random.uniform(low = 0, high = 1) < MUTATION_PROBABILITY:
            genome.genes[i] = np.random.randint(low = -GENOME_BOUNDS, high = GENOME_BOUNDS)
    return genome


def boundary(genome: Genome):
    for i in range(len(genome.genes)):
        if np.random.uniform(low=0, high=1) < 0.08:
            genome.genes[i] = GENOME_BOUNDS * (1 if np.random.uniform(low=0, high=1) < 0.5 else -1)
    return genome

def gaussian(genome: Genome):
    for i in range(len(genome.genes)):
        if np.random.uniform(low=0, high=1) < 0.08:
            genome.genes[i] = np.random.normal(scale=GENOME_BOUNDS//2)
    return genome