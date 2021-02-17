import random

import Constants as Const
from src.Robot import Robot
import numpy as np


class Population:

    def __init__(self):
        self.individuals = self.init_individuals()
        self.best_from_previous_generation = None
        self.generation = 1

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
        self.generation += 1

    def evaluation(self):
        for individual in self.individuals:
            individual.compute_fitness()

    def selection(self):
        new_population = []
        for _ in range(Const.number_of_individuals):
            tournament = random.sample(self.individuals, 5)
            best: Robot = max(tournament, key=lambda item: item.fitness)

            new_individual = Robot(Const.start_pos)
            new_individual.genome = best.genome
            new_population.append(new_individual)

        best_overall: Robot = max(self.individuals, key=lambda item: item.fitness)
        elite = Robot(Const.start_pos)
        elite.genome = best_overall.genome
        self.best_from_previous_generation = elite

        self.individuals = new_population

    def crossover_mutation(self):
        new_population = []
        for _ in range(Const.number_of_individuals - Const.elitism_rate):
            parent1 = random.sample(self.individuals, 1)[0]
            parent2 = random.sample(self.individuals, 1)[0]
            child = Robot(Const.start_pos)

            child.genome.genes = parent1.genome.crossover(parent2.genome)
            child.genome.mutation()

            new_population.append(child)

        new_population.append(self.best_from_previous_generation)
        self.individuals = new_population

    @staticmethod
    def init_individuals():
        return [Robot(Const.start_location) for _ in range(Const.number_of_individuals)]
