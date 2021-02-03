import math

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from enum import Enum

import Constants as Const
from ParticleSwarmOptimization import PSO
from src.Visualizer import Visualizer

a = 0
b = 100


class OptiFunks(Enum):
    Rosenbrock = 1
    Rastrigin = 2


c_opti_func = OptiFunks.Rastrigin


def rosenberg(x: float, y: float):
    return (a - x) ** 2 + b * (y - x ** 2) ** 2


def rastrigin(pos: np.ndarray):
    return 10 * 2 + np.sum(pos ** 2 - 10 * np.cos(2 * math.pi * pos))


def optimization_function(pos: np.ndarray) -> float:
    if c_opti_func == OptiFunks.Rosenbrock:
        if len(pos) >= 2:
            return rosenberg(pos[0], pos[1])
        else:
            raise Exception("Not enough dimensions")

    if c_opti_func == OptiFunks.Rastrigin:
        return rastrigin(pos)


if __name__ == "__main__":

    # ---Create PSO object to be used in the animation frames
    pso = PSO(optimization_function)
    pso.optimize()
    Visualizer(optimization_function, pso.history)

