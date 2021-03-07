import json
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import numpy as np
import time
from matplotlib import pyplot as plt

from genetic.Genome import Genome
from genetic.Population import Population
from simulator.Room import Room


def load_file_and_show_graph(file_name):
    f = open(file_name, )
    data = json.load(f)
    pop_data = dict(data['population'])
    colors = plt.get_cmap('plasma')(np.linspace(0, 0.8, len(Room.rooms)))
    x = np.arange(len(pop_data))

    avg_fitness = []
    best_fitness = []
    diversity = []
    room_data = {
        i: [] for i in range(len(Room.rooms))
    }
    room_names = ['Empty', 'Triangle', 'Room', 'Small Box', 'Bigger Box', 'Trapezoid', 'Labyrinth', 'Propeller', 'Slope']

    for generation in data['population']:
        c_data = data['population'][generation]
        genes = [Genome(genes = g['genes']) for g in c_data['individuals']]
        population = Population(genes)
        individual_fitness = [g['fitness'] for g in c_data['individuals']]

        room = c_data['room']

        diversity.append(population.compute_diversity())
        best_fitness.append(np.max(individual_fitness))
        avg_fitness.append(np.mean(individual_fitness))

        room_data[room].append(np.mean(individual_fitness))

    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle('Horizontally stacked subplots')

    ax1.plot(x, avg_fitness, color="blue")
    ax1.plot(x, best_fitness, color="green")
    ax1.plot(x, diversity, color="red")

    max_length = np.max([len(ro_data) for ro_data in room_data.values()])

    for key, ro_data in room_data.items():
        ax2.plot(np.arange(len(ro_data)), ro_data, color = colors[key], label=room_names[key])

    plt.legend()
    plt.show()

if __name__ == '__main__':
    load_file_and_show_graph('../data/chromosome_20210307-163218_data.json')
