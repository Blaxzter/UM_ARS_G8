import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.animation import FuncAnimation
import math

from PSO import Constants as Const
from PSO.ParticleSwarmOptimization import PSO

a = 0
b = 100



def function(x: float, y: float) -> float:
    # return (a - x) ** 2 + b * (y - x ** 2) ** 2                                                       # Rosenbrock
    return 10 * 2 + (x**2 - 10 * np.cos(2 * math.pi * x)) + (y**2 - 10 * np.cos(2 * math.pi * y))       # Rastrigin


# ---Create fig and subplot
fig, ax = plt.subplots()
fig.set_tight_layout(True)
ax.set_xlim([Const.MIN_POS, Const.MAX_POS])
ax.set_ylim([Const.MIN_POS, Const.MAX_POS])

# --Setup and plot function contour
x_y_range = np.arange(Const.MIN_POS, Const.MAX_POS, 0.01)
X, Y = np.meshgrid(x_y_range, x_y_range)
Z = function(X, Y)
ax.contour(X, Y, Z)

# ---Scatter empty sets
scatter = ax.scatter([], [], marker='x')

# ---Create PSO object to be used in the animation frames
pso = PSO(function, scatter)

# ---Update scatter plot to display initial positions of the particles
scatter.set_offsets(
    [[particle.position.x, particle.position.y] for particle in pso.team.particles]
)

# ---Setup animation and show the first graph
animation = FuncAnimation(fig, pso.optimize, repeat=False, frames=np.arange(0, Const.N_ITERATIONS), interval=100)
plt.show()

# ---Plot particles history and show it
for particle in pso.team.particles:
    plt.plot([i for i in range(len(particle.altitude_history))], [i for i in particle.altitude_history])
plt.show()

print(pso.team.particles[-1].position.x, pso.team.particles[-1].position.x) # Final Position of the particles
