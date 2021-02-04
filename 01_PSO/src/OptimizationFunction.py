from enum import Enum

import numpy as np
import math

class OptimizationFunction:
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
        return -20 * np.exp(-0.2 * np.sqrt(0.5 * (pos[0]**2 + pos[1]**2)))
