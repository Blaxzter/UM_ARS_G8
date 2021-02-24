from random import randint

from src.genetic.Genome import Genome

# TODO write some different cross over operators

def one_point_crossover(genome_1: Genome, genome_2: Genome) -> Genome:
    first_point = randint(0, len(genome_1.genes))
    new_genes = []
    for i in range(len(genome_1.genes)):
        if first_point < i:
            new_genes.append(genome_1.genes[i])
        else:
            new_genes.append(genome_2.genes[i])

    return Genome(new_genes)
