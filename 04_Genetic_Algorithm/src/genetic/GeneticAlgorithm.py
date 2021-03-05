import random
from typing import List
from datetime import datetime

import json
import numpy as np

from src.genetic import Crossover, Mutations
from src.genetic.Genome import Genome
from src.genetic.Population import Population
from src.genetic.Selection import ranked_based_selection, tournament_selection
from src.simulator.Simulator import Simulator
import src.utils.Constants as Const
from src.utils.DataVisualizer import DataManager
from types import ModuleType


class GeneticAlgorithm:
    """
    Author Frederic Abraham
    """

    def __init__(self, load=None, generation = None, show_best = None):
        self.loaded = False
        self.show_best = show_best

        if load:
            self.loaded = True
            f = open(load, )
            self.sim_data = json.load(f)
            self.load_constants()
            if show_best is not None:
                Const.N_INDIVIDUALS = show_best

        self.c_seed = 0
        self.emergency_break = False
        self.data_manager: DataManager = DataManager(
            dict(
                avg_fitness=dict(display_name='avg fitness', value=0, graph=True),
                best_fitness=dict(display_name='best fitness', value=0, graph=True),
                diversity=dict(display_name='diversity', value=0, graph=True),
                generation=dict(display_name='generation', value=0, graph=False),
                seed=dict(display_name='seed', value=0, graph=False),
            ), parallel=False, visualize=True)

        self.sim = Simulator(
            display_data=self.data_manager.display_data,
            simulation_time=Const.LIFE_STEPS,
            gui_enabled=Const.DRAW,
            stop_callback=self.stop
        )

        self.populations: List[Population] = []

        self.history = {i: [] for i in range(0, Const.N_GENERATION)}

        self.start_generation = 0
        if load and generation is not None:
            if generation == -1:
                self.start_generation = len(self.sim_data['population']) - 1
            else:
                self.start_generation = generation

        self.generation = self.start_generation + 1
        self.avg_fitness = [-1]
        self.best_fitness = [-1]

    def run(self):

        if self.loaded:
            loaded_data = self.sim_data['population'][str(self.start_generation)]
            genes = [Genome(genes=g['genes']) for g in loaded_data['individuals']]
            population = Population(genes)
            if self.show_best is not None:
                population.get_top(self.show_best)
            self.c_seed = loaded_data['seed']
        else:
            self.c_seed = np.random.randint(2147483647)
            population = Population()

        for generation in range(self.generation, Const.N_GENERATION + 1):
            if self.emergency_break:
                break

            self.generation = generation
            self.populations.append(population)
            self.evaluation(population)
            self.update_data(generation, population)

            if self.loaded:

                if self.generation > len(self.sim_data['population']) - 1:
                    break

                loaded_data = self.sim_data['population'][str(generation)]
                population = Population([Genome(genes=g['genes']) for g in loaded_data['individuals']])
                if self.show_best is not None:
                    population.get_top(self.show_best)
                self.c_seed = loaded_data['seed']
            else:
                next_population = self.selection()
                self.crossover_mutation(next_population)
                self.generate_new(next_population)
                population = Population(next_population)

                # Next seed for next simulation
                self.c_seed = np.random.randint(2147483647)

        self.data_manager.stop()
        if not self.loaded:
            self.store_date()

    def store_date(self):
        data = dict(
            constants=[
                dict(name=name, value=value) if not isinstance(value, ModuleType) else None for name, value in vars(Const).items() if not name.startswith('_')
            ],
            population= {
                i: dict(
                    seed = self.data_manager.get_data('seed')[i],
                    individuals = [
                        dict(
                            fitness=individual.fitness,
                            genes=list(individual.genes)
                        ) for individual in population.individuals
                    ]
                ) for i, population in enumerate(self.populations)
            }
        )
        with open(f"data/chromosome_{datetime.now().strftime('%Y%m%d-%H%M%S')}_data.json", "w") as write_file:
            json.dump(data, write_file)

    def evaluation(self, population: Population):
        self.sim.set_population(population, self.c_seed)
        self.sim.start() # start simulation for current population

    def selection(self) -> List[Genome]:
        next_population = []
        ordered_by_fitness = list(
            sorted(self.populations[-1].individuals, key=lambda genome: genome.fitness, reverse=True))

        # Select first n as elite
        # It was : range(1, int(Const.N_INDIVIDUALS * Const.ELITISM_PERCENTAGE) + 1): and it was not selecting the [0]th element
        # which is the best individual after sorting
        for i in range(0, int(Const.N_INDIVIDUALS * Const.ELITISM_PERCENTAGE) + 1):
            best_genome = ordered_by_fitness[i]
            next_population.append(best_genome)

        tournament_selection(ordered_by_fitness, next_population)

        return next_population

    def crossover_mutation(self, next_population: List):
        for i in range(int(Const.N_INDIVIDUALS * Const.CROSSOVER_MUTATION_PERCENTAGE)):
            parent1 = random.sample(next_population, 1)[0]
            parent2 = random.sample(next_population, 1)[0]
            child = Crossover.two_point_crossover(parent1, parent2)

            child = Mutations.gaussian(child)

            next_population.append(child)

    def generate_new(self, next_population):
        while len(next_population) < Const.N_INDIVIDUALS:
            next_population.append(Genome())

    def stop(self):
        self.emergency_break = True
        self.data_manager.stop()

    def update_data(self, generation, population):
        individuals = population.individuals

        individual_fitness = [x.fitness for x in individuals]

        self.data_manager.update_time_step(generation)

        self.data_manager.update_value('generation', generation)

        avg_fitness = np.mean(individual_fitness)
        self.data_manager.update_value('avg_fitness', avg_fitness)

        best_fitness = np.max(individual_fitness)
        self.data_manager.update_value('best_fitness', best_fitness)

        diversity = np.mean(np.abs(np.diff(np.array(np.meshgrid(individual_fitness, individual_fitness)).T.reshape(-1, 2))))
        self.data_manager.update_value('diversity', diversity)

        self.data_manager.update_value('seed', self.c_seed)

        print(f'generation: {generation} avg_fitness: {avg_fitness} best_fitness: {best_fitness} diversity: {diversity}')

        self.data_manager.update()

    def load_constants(self):
        if 'constants' not in self.sim_data:
            return
        for const in self.sim_data['constants']:
            if const is not None:
                c_name, c_value = const['name'], const['value']

                if c_name == 'ORIGIN':
                    Const.ORIGIN = c_value
                elif c_name == 'MAP_WIDTH':
                    Const.MAP_WIDTH = c_value
                elif c_name == 'MAP_HEIGHT':
                    Const.MAP_HEIGHT = c_value
                elif c_name == 'FPS':
                    Const.FPS = c_value
                elif c_name == 'HIDDEN_SIZE':
                    Const.HIDDEN_SIZE = c_value
                elif c_name == 'INPUT_SIZE':
                    Const.INPUT_SIZE = c_value
                elif c_name == 'OUTPUT_SIZE':
                    Const.OUTPUT_SIZE = c_value
                elif c_name == 'INPUT_WEIGHTS_SIZE':
                    Const.INPUT_WEIGHTS_SIZE = c_value
                elif c_name == 'HIDDEN_WEIGHTS_SIZE':
                    Const.HIDDEN_WEIGHTS_SIZE = c_value
                elif c_name == 'LIFE_STEPS':
                    Const.LIFE_STEPS = c_value
                elif c_name == 'LIFE_UPDATE':
                    Const.LIFE_UPDATE = c_value
                elif c_name == 'N_INDIVIDUALS':
                    Const.N_INDIVIDUALS = c_value
                elif c_name == 'CROSSOVER_MUTATION_PERCENTAGE':
                    Const.CROSSOVER_MUTATION_PERCENTAGE = c_value
                elif c_name == 'SELECT_PERCENTAGE':
                    Const.SELECT_PERCENTAGE = c_value
                elif c_name == 'ELITISM_PERCENTAGE':
                    Const.ELITISM_PERCENTAGE = c_value
                elif c_name == 'MUTATION_PROBABILITY':
                    Const.MUTATION_PROBABILITY = c_value
                elif c_name == 'GENOME_LENGTH':
                    Const.GENOME_LENGTH = c_value
                elif c_name == 'GENOME_BOUNDS':
                    Const.GENOME_BOUNDS = c_value
                elif c_name == 'INIT_SIZE':
                    Const.INIT_SIZE = c_value
                elif c_name == 'N_GENERATION':
                    Const.N_GENERATION = c_value
                elif c_name == 'DENSITY':
                    Const.GRAPH_WINDOW = c_value
                elif c_name == 'DENSITY':
                    Const.DUST_HORIZONTAL = c_value
