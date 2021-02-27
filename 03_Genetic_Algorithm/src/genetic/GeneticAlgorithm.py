import random
from typing import List

import numpy as np

from src.genetic import Crossover, Mutations
from src.genetic.Decoder import optimization_decoder
from src.genetic.Population import Population
from src.optimization_function.OptimizationFunction import OptimizationFunction
from src.simulator.Simulator import Simulator
from src.utils.Constants import N_GENERATION, ELITISM_PERCENTAGE, SELECT_PERCENTAGE, N_INDIVIDUALS, DRAW, OPTI_FUNC
from src.utils.DataVisualizer import DataManager


class GeneticAlgorithm:

    def __init__(self, robot: bool = False):
        self.emergency_break = False
        self.display_data = dict(
            avg_fitness = dict(display_name = 'avg fitness',  value = 0, graph = True),
            best_fitness = dict(display_name = 'best fitness',  value = 0, graph = True),
            generation = dict(display_name = 'generation',  value = 0, graph = False),
        )

        self.data_manager: DataManager = DataManager(data_names = [
            display_name['display_name'] for display_name in list(filter(lambda ele: ele['graph'], self.display_data.values()))
        ], parallel = False)

        self.robot = robot
        if self.robot:
            self.sim = Simulator(display_data = self.display_data, simulation_time = 50, gui_enabled = DRAW, stop_callback = self.stop)

        self.populations: List[Population] = []

        self.generation = 0
        self.avg_fitness = [-1]
        self.best_fitness = [-1]

    def run(self):

        population = Population()
        for generation in range(1, N_GENERATION):
            if self.emergency_break:
                break

            self.generation = generation

            self.populations.append(population)

            self.evaluation(population)
            self.update_data(generation, population)

            next_population = self.selection()
            # next_avg = np.average([indi.fitness for indi in next_population])
            # current_avg = np.average([indi.fitness for indi in population.individuals])
            # print(f'Next: {next_avg}, Current: {current_avg} Smaller: {next_avg < current_avg}')
            self.crossover_mutation(next_population)

            population = Population(next_population)

        self.data_manager.stop()

    def evaluation(self, population: Population):
        if self.robot:
            self.robot_evaluation(population)
        else:
            self.optimisation_evaluation(population)

    def robot_evaluation(self, population):
        self.sim.set_population(population)
        self.sim.start()

    def optimisation_evaluation(self, population):
        individuals = population.individuals
        for individual in individuals:
            coordinates = optimization_decoder(individual)
            func = OPTI_FUNC(coordinates)
            individual.set_fitness(0.00000001 if func == 0 else func)

    def selection(self) -> List:
        next_population = []
        ordered_by_fitness = list(sorted(self.populations[-1].individuals, key=lambda genome: genome.fitness, reverse=True))
        fitness = [individual.fitness for individual in ordered_by_fitness]

        # Select first n as elite
        for i in range(0, int(N_INDIVIDUALS * ELITISM_PERCENTAGE)):
            best_genome = ordered_by_fitness[-i]
            next_population.append(best_genome)

        weights = np.reciprocal(fitness)  # Invert all weights
        weights = weights / np.sum(weights)  # Normalize
        # Do roulette wheel selection
        for i in range(int(N_INDIVIDUALS * SELECT_PERCENTAGE)):
            choice = np.random.choice(ordered_by_fitness, p = weights)
            next_population.append(choice)  # Sample

        return next_population

    def crossover_mutation(self, next_population: List):
        while len(next_population) < N_INDIVIDUALS:
            parent1 = random.sample(next_population, 1)[0]
            parent2 = random.sample(next_population, 1)[0]
            child = Crossover.one_point_crossover(parent1, parent2)

            child = Mutations.mutationInt(child)

            next_population.append(child)

    def stop(self):
        self.emergency_break = True
        self.data_manager.stop()

    def update_data(self, generation, population):
        individuals = population.individuals

        self.data_manager.update_time_step(generation)
        self.display_data['generation']['value'] = generation
        self.display_data['avg_fitness']['value'] = np.sum([x.fitness for x in individuals]) / len(individuals)
        self.display_data['best_fitness']['value'] = np.min([x.fitness for x in individuals])

        for data in self.display_data.values():
            if 'graph' in data and data['graph']:
                self.data_manager.update_value(data['display_name'], data['value'])

        self.data_manager.update()