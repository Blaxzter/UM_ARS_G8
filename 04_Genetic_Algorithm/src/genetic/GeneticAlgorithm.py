import random
from typing import List
from datetime import datetime

import json
import numpy as np

from genetic import Crossover, Mutations
from genetic.Genome import Genome
from genetic.Population import Population
from genetic.Selection import ranked_based_selection, tournament_selection
from simulator.Room import Room
from simulator.Simulator import Simulator
import utils.Constants as Const
from utils.DataVisualizer import DataManager
from types import ModuleType


class GeneticAlgorithm:
    """
    Author Frederic Abraham
    """

    def __init__(self, load = None, generation = None, show_best = None, room: List = None, file_name = None):
        self.loaded = False
        self.show_best = show_best
        self.file_name = file_name

        self.start_generation = 0

        first_room = None

        if load:
            self.room = room
            self.room_idx = 0

            self.loaded = True
            f = open(load, )
            self.sim_data = json.load(f)
            self.load_constants()
            if show_best is not None:
                Const.N_INDIVIDUALS = show_best

            if generation is not None:
                if generation == -1:
                    self.start_generation = len(self.sim_data['population']) - 1
                else:
                    self.start_generation = generation

        self.c_seed = 0
        self.emergency_break = False
        value_dict = dict(
            avg_fitness = dict(display_name = 'avg fitness', value = 0, graph = True, disp = True),
            best_fitness = dict(display_name = 'best fitness', value = 0, graph = True, disp = True),
            diversity = dict(display_name = 'diversity', value = 0, graph = False, disp = True),
            generation = dict(display_name = 'generation', value = 0, graph = False, disp = True),
            seed = dict(display_name = 'seed', value = 0, graph = False, disp = True),
            room = dict(display_name = 'room', value = 0, graph = False, disp = False),
        )
        for room_name in Room.room_names:
            value_dict[room_name] = dict(display_name = f'room: {room_name}', value = 0, graph = True, disp = False)

        self.data_manager: DataManager = DataManager(
            value_dict, parallel = True, visualize = False)

        self.sim = Simulator(
            display_data = self.data_manager.display_data,
            simulation_time = Const.LIFE_STEPS,
            gui_enabled = Const.DRAW,
            stop_callback = self.stop,
            room = first_room,
        )

        self.populations: List[Population] = []

        self.generation = self.start_generation + 1
        self.avg_fitness = [-1]
        self.best_fitness = [-1]

        if self.file_name is not None:
            self.name = f'data/avg_run/{self.file_name}'
        else:
            self.name = f"data/chromosome_{datetime.now().strftime('%Y%m%d-%H%M%S')}_data.json"

    def run(self):
        if self.loaded:
            self.viz_loaded_data()
        else:
            self.train_genetic_algorithm()

    def viz_loaded_data(self):
        population = self.load_generation(self.start_generation)

        while self.generation < Const.N_GENERATION + 1:
            if self.emergency_break:
                break

            self.visualize_population(population)
            self.update_data(self.generation, population)

            if self.generation >= len(self.sim_data['population']) - 1:
                break

            self.generation += 1
            population = self.load_generation(self.generation)

        self.data_manager.stop()

    def load_generation(self, generation):
        loaded_data = self.sim_data['population'][str(generation)]
        genes = [Genome(genes = g['genes'], fitness = g['fitness']) for g in loaded_data['individuals']]
        population = Population(genes)
        if self.show_best is not None:
            population.get_top(self.show_best)
        self.c_seed = loaded_data['seed']
        return population

    def train_genetic_algorithm(self):
        self.c_seed = np.random.randint(2147483647)
        population = Population()

        while self.generation < Const.N_GENERATION + 1:
            if self.emergency_break:
                break

            self.populations.append(population)
            self.evaluation(population)
            self.update_data(self.generation, population)

            next_population = self.selection()
            self.crossover_mutation(next_population)
            self.generate_new(next_population)
            population = Population(next_population)

            self.store_date()

            # Next seed for next simulation
            self.c_seed = np.random.randint(2147483647)

            # Counter for the next generation
            self.generation += 1

    def store_date(self):
        data = dict(
            constants = [
                dict(name = name, value = value) if not isinstance(value, ModuleType) else None for name, value in vars(Const).items() if not name.startswith('_')
            ],
            population = {
                i: dict(
                    seed = self.data_manager.get_data('seed')[i],
                    individuals = [
                        dict(
                            fitness = individual.fitness,
                            genes = list(individual.genes)
                        ) for individual in population.individuals
                    ]
                ) for i, population in enumerate(self.populations)
            }
        )

        with open(self.name, "w") as write_file:
            json.dump(data, write_file)

    def evaluation(self, population: Population):
        for room in range(len(Room.rooms)):
            self.sim.set_population(population, self.c_seed, self.show_best is not None, room)
            self.sim.start()  # start simulation for current population
            print(f'Done room: {room}')

    def visualize_population(self, population: Population):
        for room in self.room:
            self.sim.set_population(population, self.c_seed, self.show_best is not None, room)
            self.sim.start()  # start simulation for current population

    def selection(self) -> List[Genome]:
        next_population = []
        ordered_by_fitness = list(
            sorted(self.populations[-1].individuals, key = lambda genome: genome.get_fitness(), reverse = True))

        # Select first n as elite
        for i in range(round(Const.N_INDIVIDUALS * Const.ELITISM_PERCENTAGE + Const.EPSILON)):
            best_genome = ordered_by_fitness[i]
            next_population.append(best_genome)

        ranked_based_selection(ordered_by_fitness, next_population)

        return next_population

    def crossover_mutation(self, next_population: List):
        for i in range(int(Const.N_INDIVIDUALS * Const.CROSSOVER_MUTATION_PERCENTAGE)):
            parent1 = random.sample(next_population, 1)[0]
            parent2 = random.sample(next_population, 1)[0]
            child = Crossover.two_point_crossover(parent1, parent2)

            child = Mutations.mutation(child)

            next_population.append(child)

    def generate_new(self, next_population):
        while len(next_population) < Const.N_INDIVIDUALS:
            next_population.append(Genome())

    def stop(self):
        self.emergency_break = True
        self.data_manager.stop()

    def update_data(self, generation, population):
        individuals = population.individuals

        individual_fitness = [x.get_fitness() for x in individuals]

        self.data_manager.update_time_step(generation)

        self.data_manager.update_value('generation', generation)

        avg_fitness = np.mean(individual_fitness)
        self.data_manager.update_value('avg_fitness', avg_fitness)

        best_fitness = np.max(individual_fitness)
        self.data_manager.update_value('best_fitness', best_fitness)

        diversity = population.compute_diversity()
        self.data_manager.update_value('diversity', diversity)

        self.data_manager.update_value('seed', self.c_seed)
        self.data_manager.update_value('room', self.sim.environment.room_idx)

        avg_room_fitness = dict()

        for i, room_name in enumerate(Room.room_names):
            # value_dict[room_name] = dict(display_name = 'room', value = 0, graph = False, disp = False),
            room_fitness = np.mean([x.get_fitness_by_key(i) for x in individuals])
            self.data_manager.update_value(room_name, room_fitness)
            avg_room_fitness[room_name] = room_fitness

        print(f'generation: {generation} avg_fitness: {avg_fitness} best_fitness: {best_fitness} diversity: {diversity} rooms: {avg_room_fitness}')

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
                # elif c_name == 'LIFE_STEPS':
                #     Const.LIFE_STEPS = c_value
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
