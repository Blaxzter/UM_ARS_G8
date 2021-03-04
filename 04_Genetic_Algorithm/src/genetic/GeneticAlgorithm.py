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
import src.utils.Constants as Const
from src.utils.DataVisualizer import DataManager
from types import ModuleType


class GeneticAlgorithm:
    """
    Author Frederic Abraham
    """

    def __init__(self, load=None, generation=None):
        self.loaded = False
        seed = None
        if load:
            self.loaded = True
            f = open(load, )
            self.sim_data = json.load(f)
            seed = self.sim_data['seed']
            self.load_constants()

        self.emergency_break = False
        self.display_data = dict(
            avg_fitness=dict(display_name='avg fitness', value=0, graph=True),
            best_fitness=dict(display_name='best fitness', value=0, graph=True),
            diversity=dict(display_name='diversity', value=0, graph=True),
            generation=dict(display_name='generation', value=0, graph=False),
        )

        self.data_manager: DataManager = DataManager(data_names=[
            display_name['display_name'] for display_name in
            list(filter(lambda ele: ele['graph'], self.display_data.values()))
        ], parallel=True, visualize=True)

        self.sim = Simulator(display_data=self.display_data, simulation_time=Const.LIFE_STEPS, gui_enabled=Const.DRAW,
                             stop_callback=self.stop, seed=seed)

        self.populations: List[Population] = []
        self.history = {i: [] for i in range(0, Const.N_GENERATION)}

        self.generation = 0
        self.avg_fitness = [-1]
        self.best_fitness = [-1]

    def run(self):

        if self.loaded:
            genes = [Genome(genes=g['genes']) for g in self.sim_data['genomes'][str(self.generation)]]
            population = Population(genes)
        else:
            population = Population()
        for generation in range(1, Const.N_GENERATION + 1):
            if self.emergency_break:
                break

            self.generation = generation
            self.populations.append(population)
            self.evaluation(population)
            self.update_data(generation, population)

            if self.loaded:
                population = Population([Genome(genes=g['genes']) for g in self.sim_data['genomes'][str(generation)]])
                if generation + 1 > len(self.sim_data['genomes']) - 1:
                    break
            else:
                next_population = self.selection()
                self.crossover_mutation(next_population)
                self.generate_new(next_population)
                population = Population(next_population)

        self.data_manager.stop()
        if not self.loaded:
            self.store_date()

    def store_date(self):
        data = dict(
            seed=self.sim.seed,

            constants=[
                dict(name=name, value=value) if not isinstance(value, ModuleType) else None for name, value in vars(Const).items() if not name.startswith('_')
            ],
            genomes={
                i: [
                    dict(
                        fitness=individual.fitness,
                        genes=list(individual.genes)
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
        ordered_by_fitness = list(
            sorted(self.populations[-1].individuals, key=lambda genome: genome.fitness, reverse=True))

        # Select first n as elite
        for i in range(1, int(Const.N_INDIVIDUALS * Const.ELITISM_PERCENTAGE) + 1):
            best_genome = ordered_by_fitness[i]
            next_population.append(best_genome)

        ranked_based_selection(ordered_by_fitness, next_population)

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
        self.display_data['generation']['value'] = generation
        avg_fitness = np.mean(individual_fitness)
        self.display_data['avg_fitness']['value'] = avg_fitness
        best_fitness = np.max(individual_fitness)
        self.display_data['best_fitness']['value'] = best_fitness
        diversity = np.mean(np.abs(np.diff(individual_fitness)))
        self.display_data['diversity']['value'] = diversity

        print(f'generation: {generation} avg_fitness: {avg_fitness} best_fitness: {best_fitness} diversity: {diversity}')

        for data in self.display_data.values():
            if 'graph' in data and data['graph']:
                self.data_manager.update_value(data['display_name'], data['value'])

        self.data_manager.update()

    def load_constants(self):
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
                elif c_name == 'GRAPH_WINDOW':
                    Const.GRAPH_WINDOW = c_value
                elif c_name == 'DUST_HORIZONTAL':
                    Const.DUST_HORIZONTAL = c_value
                elif c_name == 'DUST_VERTICAL':
                    Const.DUST_VERTICAL = c_value
