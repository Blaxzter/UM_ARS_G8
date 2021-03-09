import json
import os
from os import listdir

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import numpy as np
import time
from matplotlib import pyplot as plt

from genetic.Genome import Genome
from genetic.Population import Population
from simulator.Room import Room

# Frederic Abraham

def old_old_load_file_and_show_graph(file_name):
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

    for generation in data['population']:
        c_data = data['population'][generation]
        genes = [Genome(genes = g['genes']) for g in c_data['individuals']]
        population = Population(genes)
        individual_fitness = [g['fitness'] for g in c_data['individuals']]

        diversity.append(population.compute_diversity())
        best_fitness.append(np.max(individual_fitness))
        avg_fitness.append(np.mean(individual_fitness))

    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle('Genetic Algorithm - Fitness - 1 Room')

    ax1.plot(x, avg_fitness, color="blue", label="AVG Fitness")
    ax1.plot(x, best_fitness, color="green", label="Best Fitness")
    leg1 = interactive_legend(ax1)

    ax2.plot(x, diversity, color = "red", label = 'diversity')
    leg3 = interactive_legend(ax2)

    plt.show()


def old_load_file_and_show_graph(file_name):
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

        if 'room' in c_data:
            room = c_data['room']
        else:
            np.random.seed(c_data['seed'])
            room = np.random.randint(0, len(Room.rooms))

        diversity.append(population.compute_diversity())
        best_fitness.append(np.max(individual_fitness))
        avg_fitness.append(np.mean(individual_fitness))

        room_data[room].append(np.mean(individual_fitness))

    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle('Genetic Algorithm - Fitness - Random Rooms')

    ax1.plot(x, avg_fitness, color="blue", label="AVG Fitness")
    ax1.plot(x, best_fitness, color="green", label="Best Fitness")
    leg1 = interactive_legend(ax1)

    ax3 = ax1.twinx()
    ax3.plot(x, diversity, color = "red", label = 'diversity')
    leg3 = interactive_legend(ax3)

    max_length = np.max([len(ro_data) for ro_data in room_data.values()])

    for key, ro_data in room_data.items():
        ax2.plot(np.arange(len(ro_data)), ro_data, color = colors[key], label=room_names[key])

    leg2 = interactive_legend(ax2)
    plt.show()


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

        for room_idx in range(len(Room.rooms)):
            room_data[room_idx].append(np.mean([individual_fitness[i][str(room_idx)] for i in range(len(individual_fitness))]))

        generall_fitness = [np.mean(list(individual_fitness[i].values())) for i in range(len(individual_fitness))]
        diversity.append(population.compute_diversity())
        best_fitness.append(np.max(generall_fitness))
        avg_fitness.append(np.mean(generall_fitness))

    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle('Genetic Algorithm - Fitness - Random Rooms')


    ax1.plot(x, avg_fitness, color="blue", label="AVG Fitness")
    ax1.plot(x, best_fitness, color="green", label="Best Fitness")
    # ax1.plot(x, diversity, color="red")
    leg1 = interactive_legend(ax1)

    ax3 = ax1.twinx()
    ax3.plot(x, diversity, color="red", label='diversity')
    leg3 = interactive_legend(ax3)

    max_length = np.max([len(ro_data) for ro_data in room_data.values()])

    for key, ro_data in room_data.items():
        ax2.plot(np.arange(len(ro_data)), ro_data, color = colors[key], label=room_names[key])

    leg2 = interactive_legend(ax2)
    plt.show()

def avg_data(folder):

    runs = listdir(folder)

    data_list = []

    for run in runs[:2]:
        f = open(f'{folder}/{run}', )
        data = json.load(f)
        pop_data = dict(data['population'])
        data_list.append(pop_data)

    colors = plt.get_cmap('plasma')(np.linspace(0, 0.8, len(Room.rooms)))
    x = np.arange(len(pop_data))

    sum_avg_fitness = []
    up_std_error_avg_fitness = []
    down_std_error_avg_fitness = []

    sum_best_fitness = []
    up_std_error_best_fitness = []
    down_std_error_best_fitness = []

    sum_diversity = []
    up_std_error_diversity = []
    down_std_error_diversity = []

    sum_room_data = {
        i: [] for i in range(len(Room.rooms))
    }
    room_names = ['Empty', 'Triangle', 'Room', 'Small Box', 'Bigger Box', 'Trapezoid', 'Labyrinth', 'Propeller', 'Slope']

    for gen in range(100):
        avg_fitness = []
        best_fitness = []
        diversity = []
        room_data = {
            i: [] for i in range(len(Room.rooms))
        }
        for data_entry in data_list:
            c_data = data_entry[str(gen)]
            genes = [Genome(genes = g['genes']) for g in c_data['individuals']]
            population = Population(genes)
            individual_fitness = [g['fitness'] for g in c_data['individuals']]

            for room_idx in range(len(Room.rooms)):
                room_data[room_idx].append(np.mean([individual_fitness[i][str(room_idx)] for i in range(len(individual_fitness))]))

            generall_fitness = [np.mean(list(individual_fitness[i].values())) for i in range(len(individual_fitness))]
            diversity.append(population.compute_diversity())
            best_fitness.append(np.max(generall_fitness))
            avg_fitness.append(np.mean(generall_fitness))

        avg_of_avg_fitness = np.mean(avg_fitness)
        sum_avg_fitness.append(avg_of_avg_fitness)

        differences = []
        for c_avg_fitness in avg_fitness:
            differences.append(avg_of_avg_fitness - c_avg_fitness)
        up_std_error_avg_fitness.append(np.max(avg_fitness) - avg_of_avg_fitness)
        down_std_error_avg_fitness.append(avg_of_avg_fitness - np.min(avg_fitness))


        avg_of_best_fitness = np.mean(best_fitness)
        sum_best_fitness.append(avg_of_best_fitness)

        differences = []
        for c_best_fitness in avg_fitness:
            differences.append(avg_of_best_fitness - c_best_fitness)

        up_std_error_best_fitness.append(np.max(best_fitness) - avg_of_best_fitness)
        down_std_error_best_fitness.append(avg_of_best_fitness - np.min(best_fitness))


        avg_diversity = np.mean(diversity)
        sum_diversity.append(avg_diversity)
        differences = []
        for c_diversity in diversity:
            differences.append(avg_diversity - c_diversity)

        up_std_error_diversity.append(np.max(diversity) - avg_diversity)
        down_std_error_diversity.append(avg_diversity - np.min(diversity))

        for room_idx in range(len(Room.rooms)):
            sum_room_data[room_idx].append(np.mean(room_data[room_idx]))

    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle('Genetic Algorithm - Fitness - Avg Rooms')

    # ax1.errorbar(x, sum_avg_fitness, [down_std_error_avg_fitness, up_std_error_avg_fitness], color="blue", marker = '^', label='avg_fitness')
    # # ax1.plot(x, sum_avg_fitness, color="blue")
    # ax1.errorbar(x, sum_best_fitness, [down_std_error_best_fitness, up_std_error_best_fitness], color = "green", marker = 'x', label='best_fitness')
    # # ax1.plot(x, sum_best_fitness, color="green")
    # leg1 = interactive_legend(ax1)

    ax3 = ax1.twinx()
    ax3.errorbar(x, sum_diversity, [down_std_error_diversity, up_std_error_diversity], color = "red", marker = '^', label = 'diversity')
    # ax3.plot(x, sum_diversity, color="red", label='diversity')
    leg3 = interactive_legend(ax3)


    for key, ro_data in sum_room_data.items():
        ax2.plot(np.arange(len(ro_data)), ro_data, color = colors[key], label=room_names[key])

    leg2 = interactive_legend(ax2)
    plt.show()

# Taken from here:
# https://stackoverflow.com/questions/31410043/hiding-lines-after-showing-a-pyplot-figure

def interactive_legend(ax=None):
    if ax is None:
        ax = plt.gca()
    if ax.legend_ is None:
        ax.legend()

    return InteractiveLegend(ax.get_legend())

class InteractiveLegend(object):
    def __init__(self, legend):
        self.legend = legend
        self.fig = legend.axes.figure

        self.lookup_artist, self.lookup_handle = self._build_lookups(legend)
        self._setup_connections()

        self.update()

    def _setup_connections(self):
        for artist in self.legend.texts + self.legend.legendHandles:
            artist.set_picker(10) # 10 points tolerance

        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)

    def _build_lookups(self, legend):
        labels = [t.get_text() for t in legend.texts]
        handles = legend.legendHandles
        label2handle = dict(zip(labels, handles))
        handle2text = dict(zip(handles, legend.texts))

        lookup_artist = {}
        lookup_handle = {}
        for artist in legend.axes.get_children():
            if artist.get_label() in labels:
                handle = label2handle[artist.get_label()]
                lookup_handle[artist] = handle
                lookup_artist[handle] = artist
                lookup_artist[handle2text[handle]] = artist

        lookup_handle.update(zip(handles, handles))
        lookup_handle.update(zip(legend.texts, handles))

        return lookup_artist, lookup_handle

    def on_pick(self, event):
        handle = event.artist
        if handle in self.lookup_artist:

            artist = self.lookup_artist[handle]
            artist.set_visible(not artist.get_visible())
            self.update()

    def on_click(self, event):
        if event.button == 3:
            visible = False
        elif event.button == 2:
            visible = True
        else:
            return

        for artist in self.lookup_artist.values():
            artist.set_visible(visible)
        self.update()

    def update(self):
        for artist in self.lookup_artist.values():
            handle = self.lookup_handle[artist]
            if artist.get_visible():
                handle.set_visible(True)
            else:
                handle.set_visible(False)
        self.fig.canvas.draw()

    def show(self):
        plt.show()

if __name__ == '__main__':
    avg_data('../data/avg_run_save')
    # load_file_and_show_graph('../data/154_Avg_over_8_rooms.json')
    # old_load_file_and_show_graph('../data/chromosome_20210306-120009_data.json')
    # # old_old_load_file_and_show_graph('../data/chromosome_20210305-185238_data.json')
    # old_old_load_file_and_show_graph('../data/chromosome_20210306-120009_data.json')
