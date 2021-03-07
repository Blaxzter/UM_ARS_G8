import numpy as np

from genetic import Genome

# todo write some other mutation operators
import utils.Constants as Const

"""
Author Guillaume Franzoni Darnois & Theodoros Giannilias
"""


def mutation(genome: Genome):
    for i in range(len(genome.genes)):
        if np.random.uniform(low = 0, high = 1) < Const.MUTATION_PROBABILITY:
            genome.genes[i] = np.random.uniform(low = -Const.GENOME_BOUNDS, high = Const.GENOME_BOUNDS)
    return genome


# Flip values mutation operation
def bit_flip_mutation(genome: Genome):
    for i in range(len(genome.genes)):
        if np.random.uniform(low = 0, high = 1) < Const.MUTATION_PROBABILITY:
            genome.genes[i] = -1 * genome.genes[i]
    return genome


# Swap randomly mutation operation
def swap_mutation(genome: Genome):
    for i in range(len(genome.genes)):
        if np.random.uniform(low = 0, high = 1) < Const.MUTATION_PROBABILITY:
            temp = genome.genes[i]
            index = np.random.randint(low = 0, high = len(genome.genes))
            genome.genes[i] = genome.genes[index]
            genome.genes[index] = temp
    return genome


def mutationInt(genome: Genome):
    for i in range(len(genome.genes)):
        if np.random.uniform(low = 0, high = 1) < Const.MUTATION_PROBABILITY:
            genome.genes[i] = np.random.randint(low = -Const.GENOME_BOUNDS, high = Const.GENOME_BOUNDS)
    return genome


def boundary(genome: Genome):
    for i in range(len(genome.genes)):
        if np.random.uniform(low = 0, high = 1) < Const.MUTATION_PROBABILITY:
            genome.genes[i] = Const.GENOME_BOUNDS * (1 if np.random.uniform(low = 0, high = 1) < 0.5 else -1)
    return genome


def gaussian(genome: Genome):
    for i in range(len(genome.genes)):
        if np.random.uniform(low = 0, high = 1) < Const.MUTATION_PROBABILITY:
            genome.genes[i] = np.clip([np.random.normal(scale = 0.5)], -Const.GENOME_BOUNDS, Const.GENOME_BOUNDS)[0]
    return genome
