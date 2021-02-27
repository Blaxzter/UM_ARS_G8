from enum import Enum

import numpy as np
import math

ackley_height = 20

class OptimizationFunction:
    """
    Author Frederic Abraham
    """

    def __init__(self, a: float = 0, b: float = 100):
        self.a = a
        self.b = b

    def rosenbrock(self, pos: np.ndarray):
        return np.sum(
            [self.b * (pos[i + 1] - pos[i] ** 2) ** 2 + (self.a - pos[i]) ** 2 for i in range(0, len(pos) - 1)]
        )

    def rastrigin(self, pos: np.ndarray):
        return 10 * len(pos) + np.sum(pos ** 2 - 10 * np.cos(2 * math.pi * pos))

    def square(self, pos: np.ndarray):
        return np.sum(pos ** 2)

    def ackley(self, pos: np.ndarray):
        return -20 * np.exp(-0.2 * np.sqrt(0.5 * (pos[0] ** 2 + pos[1] ** 2)))[0]

    def reverse_ackley(self, pos: np.ndarray):
        return self.ackley(pos) * -1

    def ackley2(self, pos: np.ndarray):
        """
        Src: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.differential_evolution.html
        """
        arg1 = -0.2 * np.sqrt(0.5 * (pos[0] ** 2 + pos[1] ** 2))
        arg2 = 0.5 * (np.cos(2. * np.pi * pos[0]) + np.cos(2. * np.pi * pos[1]))
        ackley_value = -20. * np.exp(arg1) - np.exp(arg2) + 20. + np.e
        return ackley_value[0]

    def reverse_ackley2(self, pos: np.ndarray):
        return self.ackley2(pos) * -1
