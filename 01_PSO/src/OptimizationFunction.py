from enum import Enum

import numpy as np
import math


class OptiFunks(Enum):
    Rosenbrock = 1
    Rastrigin = 2


class OptimizationFunction:
    def __init__(self, a: float = 0, b: float = 100, selected_function: OptiFunks = None):
        if selected_function is None:
            self.c_opti_func = OptiFunks.Rastrigin
        else:
            self.c_opti_func = selected_function

        self.a = a
        self.b = b

    def rosenbrock(self, pos: np.ndarray):
        return np.sum(
            [self.b * (pos[i + 1] - pos[i] ** 2) ** 2 + (self.a - pos[i]) ** 2 for i in range(0, len(pos) - 1)]
        )

    def rastrigin(self, pos: np.ndarray):
        return 10 * len(pos) + np.sum(pos ** 2 - 10 * np.cos(2 * math.pi * pos))

    def optimization_function(self, pos: np.ndarray) -> float:
        if self.c_opti_func == OptiFunks.Rosenbrock:
            return self.rosenbrock(pos)

        if self.c_opti_func == OptiFunks.Rastrigin:
            return self.rastrigin(pos)
