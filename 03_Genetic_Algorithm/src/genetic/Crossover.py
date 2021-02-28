from random import randint
import random as rd
import src.utils.Constants as const
from src.genetic.Genome import Genome

# TODO write some different cross over operators

#  Normally we have to return at least 2 offsprings
def one_point_crossover(genome_1: Genome, genome_2: Genome) -> Genome:
    first_point = randint(0, const.GENOME_LENGTH)
    new_genes = []
    for i in range(const.GENOME_LENGTH):
        if first_point < i:
            new_genes.append(genome_1.genes[i])
        else:
            new_genes.append(genome_2.genes[i])
    return Genome(new_genes)

#  Two-Point Crossover Operation
def two_point_crossover(genome_1: Genome, genome_2: Genome) -> Genome:
    first_point = randint(0, const.GENOME_LENGTH)
    # Normally both have to be a random number but it makes sense to start them that way since after the 1st point then the second starts
    second_point = randint(first_point, const.GENOME_LENGTH)
    new_genes = []
    selection = rd.choices([0, 1], weights=[5, 5], k=1)
    if selection[0] == 0:
        for i in range(const.GENOME_LENGTH):
            if i < first_point or i > second_point:
                new_genes.append(genome_1.genes[i])
            else:
                new_genes.append(genome_2.genes[i])
    else:
        for i in range(const.GENOME_LENGTH):
            if i < first_point or i > second_point:
                new_genes.append(genome_2.genes[i])
            else:
                new_genes.append(genome_1.genes[i])
    return Genome(new_genes)

# Multi-Point Crossover Operation
def multi_point_crossover(genome_1: Genome, genome_2: Genome) -> Genome:
    num_of_points = randint(0, const.GENOME_LENGTH)
    selection = rd.choices([0, 1], weights=[5, 5], k=1)
    new_genes = []
    multi_points = []
    for i in range(num_of_points):
        multi_points.append(randint(0, const.GENOME_LENGTH))
    # remove duplicate variables from the list
    multi_points = list(dict.fromkeys(multi_points))
    multi_points.sort()
    counter = 0
    if selection[0] == 0:
        for i in range(const.GENOME_LENGTH):
            if i >= multi_points[counter]:
                counter += 1
            if counter % 2 == 0:
                new_genes.append(genome_1.genes[i])
            else:
                new_genes.append(genome_2.genes[i])
    else:
        for i in range(const.GENOME_LENGTH):
            if i >= multi_points[counter]:
                counter += 1
            if counter % 2 == 0:
                new_genes.append(genome_1.genes[i])
            else:
                new_genes.append(genome_2.genes[i])
    return Genome(new_genes)

# Uniform Crossover Operation
def uniform_crossover(genome_1: Genome, genome_2: Genome) -> Genome:
    new_genes = []
    for i in range(const.GENOME_LENGTH):
        selection = rd.choices([0, 1], weights=[5, 5], k=1)
        if selection[0] == 0:
            new_genes.append(genome_1.genes)
        else:
            new_genes.append(genome_2.genes)
    return Genome(new_genes)

# Linear Crossover Operation:
def linear_crossover(genome_1: Genome, genome_2: Genome) -> Genome:
    a: float = rd.uniform(0, 1)
    new_genes = (genome_1.genes * a + (1 - a) * genome_2.genes)
    for i in range(len(new_genes)):
        new_genes[i] = round(new_genes[i], 0)

    return Genome(new_genes)

# TODO mask_uniform_crossover, linear_crossover, multi-point_crossover
# Testing main just for my part :

#def main():
#    genome1 = Genome()
#    genome2 = Genome()
#    print(multi_point_crossover(genome1, genome2))

#if __name__ == "__main__":
#    main()
