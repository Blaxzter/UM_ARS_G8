import random

import Constants as Const
from src.Robot import Robot
import numpy as np


class Population:

    def __init__(self):
        self.individuals = self.init_individuals()

    def update(self, environment, frame):
        for individual in self.individuals:
            individual.apply_genome(frame)
            individual.update(environment)

    def draw(self, screen):
        for individual in self.individuals:
            individual.draw(screen)

    def generation_cycle(self):
        self.evaluation()
        self.selection()
        self.crossover_mutation()

    def evaluation(self):
        for individual in self.individuals:
            individual.compute_fitness()

    def selection(self):
        new_population = []
        for _ in range(Const.number_of_individuals):
            tournament = random.sample(self.individuals, 3)
            best: Robot = max(tournament, key=lambda item: item.fitness)
            new_individual = Robot(Const.start_pos)
            new_individual.genome = best.genome
            new_population.append(new_individual)
        self.individuals = new_population

    def crossover_mutation(self):
        for individual in self.individuals:
            paired_with = random.sample(self.individuals, 1)[0]
            while paired_with.genome == individual.genome:
                paired_with = random.sample(self.individuals, 1)[0]
            individual.genome.crossover(paired_with.genome)
            individual.genome.mutation()

    @staticmethod
    def init_individuals():
        return [Robot(Const.start_location) for _ in range(Const.number_of_individuals)]
