import time
from multiprocessing import Manager, Process
from typing import List

import seaborn as sns
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


class LiveGraph:
    """
    Class to visualize data live in an matplot env
    @author Frederic Abraham
    """

    def __init__(self, timestep, line_dict, pull_rate=100):

        self.pull_rate = pull_rate
        self.time_step = timestep
        self.line_dict = line_dict

        self.fig = plt.figure()
        self.ax = plt.axes()

        self.xs = []
        self.data = {key: [] for key in self.line_dict.keys()}

        self.colors = plt.get_cmap('plasma')(np.linspace(0, 0.8, len(self.data)))

        plt.title("A Sine Curve")
        plt.xlabel("x")
        plt.ylabel("sin(x)")
        sns.set_theme()
        for i, key in enumerate(line_dict.keys()):
            plt.plot([], [], color=self.colors[i], label=f'{key}')
        plt.legend()

        self.p = Process(target=self.start_animate)
        self.p.start()

    def do_line_graphs(self, timestep, line_dict):
        self.xs.append(timestep.value)
        for key in line_dict.keys():
            self.data[key].append(line_dict[key])

        # Draw x and y lists
        for i, key in enumerate(line_dict.keys()):
            plt.plot(self.xs, self.data[key], color=self.colors[i], label=f'{key}')

        plt.draw()

    def animate(self, i, timestep, line_dict):
        try:
            # print(f'i: {i}   t: {timestep}     lines: {line_dict}')
            self.do_line_graphs(timestep, line_dict)
            plt.draw()
        except Exception:
            self.p.kill()
            plt.close(self.fig)

    def start_animate(self):
        try:
            ani = animation.FuncAnimation(self.fig, self.animate,
                                          fargs=(self.time_step, self.line_dict), interval=self.pull_rate)
            plt.show()
        except Exception:
            self.p.kill()
            plt.close(self.fig)

    def stop(self):
        self.p.kill()
        plt.close(self.fig)


class DataManager:
    """
    Class to interact with the Data visualizer
    @author Frederic Abraham
    """

    def __init__(self, data_names: List, pull_rate: int):
        self.manager = Manager()
        self.time_step = self.manager.Value("timestep", 0)
        self.line_dict = self.manager.dict({data_name: 0 for data_name in data_names})
        self.live_graph = LiveGraph(self.time_step, self.line_dict, pull_rate)

    def update_time_step(self, new_time_step):
        self.time_step.value = new_time_step

    def update_value(self, key, value):
        self.line_dict[key] = value

    def stop(self):
        self.live_graph.stop()


if __name__ == '__main__':
    data_manager = DataManager(data_names=[
        'avg fitness',
        'max fitness',
        'käse brot'
    ], pull_rate=100)

    for i in range(0, 200):
        data_manager.update_time_step(i)
        data_manager.update_value('avg fitness', np.sin(i / 10))
        data_manager.update_value('max fitness', np.cos(i / 10))
        # data_manager.update_value('käse brot', np.tan(i / 10))
        time.sleep(0.4)

    data_manager.stop()
