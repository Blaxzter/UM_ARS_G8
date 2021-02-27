import sys
import threading
from multiprocessing import Manager, Process
from typing import List

import numpy as np
import time
from matplotlib import pyplot as plt

def run(done, iteration, line_dict):
    """
    Display the simulation using matplotlib, optionally using blit for speed
    """

    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)

    colors = plt.get_cmap('plasma')(np.linspace(0, 0.8, len(line_dict)))
    data = {key: [] for key in line_dict.keys()}

    lines = {key: ax.plot([], [], color=colors[i], label=f'{key}')[0] for i, key in enumerate(data)}
    old_value = iteration.value
    x = []

    while done.value:
        # print(done.value)
        if old_value < iteration.value:
            # print(old_value, iteration.value)
            for key in line_dict.keys():
                data[key].append(line_dict[key])
                x = np.arange(len(data[key]))
            old_value = iteration.value

            for i, key in enumerate(data.keys()):
                ax.plot(x, data[key], color=colors[i], label=f'{key}')

            fig.canvas.draw()

            fig.canvas.flush_events()
            time.sleep(0.1)

    plt.close(fig)


class DataManager:
    """
    Class to interact with the Data visualizer
    @author Frederic Abraham
    """

    def __init__(self, data_names: List, pull_rate: int):
        self.manager = Manager()
        self.done = self.manager.Value("done", True)
        self.time_step = self.manager.Value("timestep", 0)
        self.line_dict = self.manager.dict({data_name: 0 for data_name in data_names})
        self.p = Process(target=run, args = (self.done, self.time_step, self.line_dict, ))
        self.p.start()

    def update_time_step(self, new_time_step):
        self.time_step.value = new_time_step

    def update_value(self, key, value):
        self.line_dict[key] = value

    def stop(self):
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