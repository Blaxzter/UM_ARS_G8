import numpy as np
import matplotlib.pyplot as plt

from PSO.ParticleSwarmOptimization import PSO
from PSO.Position import Position


def function(position: Position) -> float:
    return np.sqrt(
        position.x ** 2 +
        position.y ** 2
    )


my_pso = PSO(function)
history = my_pso.optimize()

plt.plot([i for i in range(len(history))], [i[1] for i in history])
plt.show()
