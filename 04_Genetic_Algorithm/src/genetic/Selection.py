from typing import List
import numpy as np

from src.utils.Constants import *

from src.genetic.Genome import Genome


def roulette_wheel_selection(individuals: List[Genome], next_population: List):
    fitness = [individual.fitness for individual in individuals]
    weights = fitness / np.sum(fitness)  # Normalize
    # Do roulette wheel selection
    for i in range(int(N_INDIVIDUALS * SELECT_PERCENTAGE)):
        choice = np.random.choice(individuals, p = weights)
        next_population.append(choice)  # Sample


def ranked_based_selection(individuals: List[Genome], next_population: List):
    ranks = [rank for rank in range(len(individuals), 0, -1)]
    weights = ranks / np.sum(ranks)  # Normalize
    # Do roulette wheel selection
    for i in range(int(N_INDIVIDUALS * SELECT_PERCENTAGE)):
        choice = np.random.choice(individuals, p = weights)
        next_population.append(choice)  # Sample