from multiprocessing import Manager, Process
from typing import List

import numpy as np
import time
from matplotlib import pyplot as plt

from src.utils.Constants import GRAPH_WINDOW


def animate(x, data, colors):
    plt.cla()

    for i, key in enumerate(data.keys()):
        y = data[key]
        viz_x = x

        if GRAPH_WINDOW != -1:
            y = data[key][-GRAPH_WINDOW:]
            viz_x = x[-GRAPH_WINDOW:]

        plt.plot(viz_x, y, color = colors[i], label = f'{key}')
    plt.pause(0.00001)

    plt.legend(loc='upper left')
    plt.tight_layout()


def run(done, iteration, line_dict):
    """
    Display the simulation using matplotlib, optionally using blit for speed
    """

    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)

    colors = plt.get_cmap('plasma')(np.linspace(0, 0.8, len(line_dict)))
    data = {key: [] for key in line_dict.keys()}
    for i, key in enumerate(data):
        ax.plot([], [], color=colors[i], label=f'{key}')
    plt.legend()
    old_value = iteration.value
    x = []

    while done.value:
        # print(done.value)
        if old_value < iteration.value:
            # print(old_value, iteration.value)
            ax.cla()
            for i, key in enumerate(line_dict.keys()):

                data[key].append(line_dict[key])
                y = data[key]
                x = np.arange(len(data[key]))

                if GRAPH_WINDOW != -1:
                    y = data[key][-GRAPH_WINDOW:]
                    x = x[-GRAPH_WINDOW:]

                # print(key, x)
                # print(key, y)
                ax.plot(x, y, color = colors[i], label = f'{key}')

            old_value = iteration.value

            fig.canvas.draw()
            # plt.legend()
            # plt.cla()
            time.sleep(0.001)

    plt.close(fig)


class DataManager:
    """
    Class to interact with the Data visualizer
    @author Frederic Abraham
    """

    def __init__(self, data_names: List, parallel: bool = False, visualize: bool = True):

        self.parallel = parallel
        self.visualize = visualize
        if parallel:
            if self.visualize:
                self.manager = Manager()
                self.done = self.manager.Value("done", True)
                self.time_step = self.manager.Value("timestep", 0)
                self.line_dict = self.manager.dict({data_name: 0 for data_name in data_names})

                self.p = Process(target = run, args = (self.done, self.time_step, self.line_dict,))
                self.p.start()
        else:
            if self.visualize:
                plt.tight_layout()
                plt.ion()
                plt.show()
            self.time_steps = []
            self.data = {data_name: [] for data_name in data_names}
            self.colors = plt.get_cmap('plasma')(np.linspace(0, 0.8, len(self.data)))

    def update_time_step(self, new_time_step):
        if self.parallel:
            self.time_step.value = new_time_step
        else:
            self.time_steps.append(new_time_step)

    def update_value(self, key, value):
        if self.parallel:
            self.line_dict[key] = value
        else:
            self.data[key].append(value)

    def get_data(self, key):
        return self.data[key]

    def update(self):
        if not self.parallel and self.visualize:
            animate(self.time_steps, self.data, self.colors)

    def stop(self):
        if self.parallel:
            self.done.value = False
            self.p.join()
            self.p.close()


if __name__ == '__main__':
    data_manager = DataManager(data_names=[
        'avg fitness',
        'max fitness'
    ], pull_rate=100)

    for i in range(0, 50):
        print(i)
        data_manager.update_time_step(i)
        data_manager.update_value('avg fitness', np.sin(i / 10))
        data_manager.update_value('max fitness', np.cos(i / 10))
        time.sleep(0.1)

    data_manager.stop()