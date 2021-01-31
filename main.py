import numpy as np
import matplotlib.pyplot as plt

from PSO.ParticleSwarmOptimization import PSO
from PSO.Position import Position


def function(position: Position):
    return -( (12 * np.cos((position.x**2 + position.y**2)/4)) / (3 + position.x**2 + position.y**2))


my_pso = PSO(function)
my_pso.optimize()

for particle in my_pso.team.particles:
    plt.plot([i for i in range(len(particle.altitude_history))], [i for i in particle.altitude_history])

plt.show()
