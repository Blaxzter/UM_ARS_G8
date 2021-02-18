import random

import Constants as Const
from src.Robot import Robot
import numpy as np


class Population:

    def __init__(self):
        self.individuals = self.init_individuals()
        self.best_from_previous_generation = []
        self.generation = 0
        self.avg_fitness = [-1]
        self.best_fitness = [-1]

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
        if self.generation % 50 == 0:
            Const.individuals_life_steps += Const.life_update
            for individual in self.individuals:
                individual.genome.extend_genome()

    def evaluation(self):
        for individual in self.individuals:
            individual.compute_fitness()

        self.avg_fitness.append(np.sum([x.fitness for x in self.individuals]) / len(self.individuals))
        self.best_fitness.append(np.max([x.fitness for x in self.individuals]))

    def selection(self):
        self.best_from_previous_generation.clear()
        ordered_by_fitness = sorted(self.individuals, key=lambda robot: robot.fitness, reverse=True)[:Const.elitism_rate]
        for best in ordered_by_fitness:
            elite = Robot(Const.start_pos)
            elite.genome = best.genome
            self.best_from_previous_generation.append(elite)

    def crossover_mutation(self):
        new_population = []
        for _ in range(Const.number_of_individuals - Const.elitism_rate):
            parent1 = random.sample(self.best_from_previous_generation, 1)[0]
            parent2 = random.sample(self.best_from_previous_generation, 1)[0]
            child = Robot(Const.start_pos)

            child.genome.genes = parent1.genome.crossover(parent2.genome)
            child.genome.mutation()

            new_population.append(child)

        new_population.extend(self.best_from_previous_generation)
        self.individuals = new_population

    @staticmethod
    def init_individuals():
        return [Robot(Const.start_location) for _ in range(Const.number_of_individuals)]
