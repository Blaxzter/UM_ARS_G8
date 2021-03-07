from typing import List
import numpy as np
import random

import utils.Constants as Const

from genetic.Genome import Genome


def roulette_wheel_selection(individuals: List[Genome], next_population: List):
    fitness = [individual.fitness for individual in individuals]
    weights = fitness / np.sum(fitness)  # Normalize
    # Do roulette wheel selection
    for i in range(int(Const.N_INDIVIDUALS * Const.SELECT_PERCENTAGE)):
        choice = np.random.choice(individuals, p = weights)
        next_population.append(choice)  # Sample


def ranked_based_selection(individuals: List[Genome], next_population: List):
    ranks = [rank for rank in range(len(individuals), 0, -1)]
    weights = ranks / np.sum(ranks)  # Normalize
    # Do roulette wheel selection
    for i in range(int(Const.N_INDIVIDUALS * Const.SELECT_PERCENTAGE)):
        choice = np.random.choice(individuals, p = weights)
        next_population.append(choice)  # Sample


def tournament_selection(individuals: List[Genome], next_population: List):
    """
    Author Villen doctor evil aka frederic abraham
    """
    for i in range(int(Const.N_INDIVIDUALS * Const.SELECT_PERCENTAGE)):
        tournament = random.sample(individuals, Const.TOURNAMENT_SELECTION)
        best: Genome = max(tournament, key = lambda item: item.get_fitness())
        next_population.append(best)
