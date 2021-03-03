import random
from typing import List
from datetime import datetime

import json
import numpy as np

from src.genetic import Crossover, Mutations
from src.genetic.Genome import Genome
from src.genetic.Population import Population
from src.genetic.Selection import ranked_based_selection
from src.simulator.Simulator import Simulator
from src.utils.Constants import *
from src.utils.DataVisualizer import DataManager


class GeneticAlgorithm:
    """
    Author Frederic Abraham
    """

    def __init__(self):
        self.emergency_break = False
        self.display_data = dict(
            avg_fitness = dict(display_name = 'avg fitness',  value = 0, graph = True),
            best_fitness = dict(display_name = 'best fitness',  value = 0, graph = True),
            diversity = dict(display_name = 'diversity',  value = 0, graph = True),
            generation = dict(display_name = 'generation',  value = 0, graph = False),
        )

        self.data_manager: DataManager = DataManager(data_names = [
            display_name['display_name'] for display_name in list(filter(lambda ele: ele['graph'], self.display_data.values()))
        ], parallel = False, visualize=False)

        self.sim = Simulator(display_data = self.display_data, simulation_time = LIFE_STEPS, gui_enabled = DRAW, stop_callback = self.stop)

        self.populations: List[Population] = []
        self.history = {i: [] for i in range(0, N_GENERATION)}

        self.generation = 0
        self.avg_fitness = [-1]
        self.best_fitness = [-1]

    def run(self):

        population = Population()
        for generation in range(1, N_GENERATION + 1):
            if self.emergency_break:
                break

            self.generation = generation

            self.populations.append(population)

            self.evaluation(population)
            self.update_data(generation, population)

            next_population = self.selection()
            self.crossover_mutation(next_population)
            self.generate_new(next_population)

            population = Population(next_population)

        self.data_manager.stop()
        self.store_date()

    def store_date(self):
        data = dict(
            seed = self.sim.seed,
            genomes = {
                i: [
                    dict(
                        fitness = individual.fitness,
                        genes = list(individual.genes)
                    ) for individual in population.individuals
                ] for i, population in enumerate(self.populations)
            }
        )
        with open(f"data/chromosome_{datetime.now().strftime('%Y%m%d-%H%M%S')}_data.json", "w") as write_file:
            json.dump(data, write_file)

    def evaluation(self, population: Population):
        self.robot_evaluation(population)


    def robot_evaluation(self, population):
        self.sim.set_population(population)
        self.sim.start()

    def selection(self) -> List[Genome]:
        next_population = []
        ordered_by_fitness = list(sorted(self.populations[-1].individuals, key=lambda genome: genome.fitness, reverse=True))

        # Select first n as elite
        for i in range(1, int(N_INDIVIDUALS * ELITISM_PERCENTAGE) + 1):
            best_genome = ordered_by_fitness[i]
            next_population.append(best_genome)

        ranked_based_selection(ordered_by_fitness, next_population)

        return next_population

    def crossover_mutation(self, next_population: List):
        for i in range(int(N_INDIVIDUALS * CROSSOVER_MUTATION_PERCENTAGE)):
            parent1 = random.sample(next_population, 1)[0]
            parent2 = random.sample(next_population, 1)[0]
            child = Crossover.two_point_crossover(parent1, parent2)

            child = Mutations.gaussian(child)

            next_population.append(child)

    def generate_new(self, next_population):
        while len(next_population) < N_INDIVIDUALS:
            next_population.append(Genome())

    def stop(self):
        self.emergency_break = True
        self.data_manager.stop()

    def update_data(self, generation, population):
        individuals = population.individuals

        individual_fitness = [x.fitness for x in individuals]

        self.data_manager.update_time_step(generation)
        self.display_data['generation']['value'] = generation
        self.display_data['avg_fitness']['value'] = np.mean(individual_fitness)
        self.display_data['best_fitness']['value'] = np.max(individual_fitness)
        self.display_data['diversity']['value'] = np.mean(np.abs(np.diff(individual_fitness)))

        for data in self.display_data.values():
            if 'graph' in data and data['graph']:
                self.data_manager.update_value(data['display_name'], data['value'])

        self.data_manager.update()

