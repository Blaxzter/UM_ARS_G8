import numpy as np
import matplotlib.pyplot as plt

from PSO.ParticleSwarmOptimization import PSO
from PSO.Position import Position


def function(position: Position):
    return -( (12 * np.cos((position.x**2 + position.y**2)/4)) / (3 + position.x**2 + position.y**2))


my_pso = PSO(function)
history = my_pso.optimize()
print([i[1] for i in history])
plt.plot([i for i in range(len(history))], [i[1] for i in history])
plt.show()
