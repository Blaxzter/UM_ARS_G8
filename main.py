import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.animation import FuncAnimation

from PSO import Constants as Const
from PSO.ParticleSwarmOptimization import PSO


def function(x: float, y: float) -> float:
    # return -((12 * np.cos((x ** 2 + y ** 2) / 4)) / (3 + x ** 2 + y ** 2))    # func1
    return -np.sin(np.sqrt(x ** 2 + y ** 2))                                    # func2


# ---Create fig and subplot
fig, ax = plt.subplots()
fig.set_tight_layout(True)
ax.set_xlim([Const.MIN_POS, Const.MAX_POS])
ax.set_ylim([Const.MIN_POS, Const.MAX_POS])

# --Setup and plot function contour
x_y_range = np.linspace(Const.MIN_POS, Const.MAX_POS, 300)
X, Y = np.meshgrid(x_y_range, x_y_range)
Z = function(X, Y)
ax.contour(X, Y, Z, cmap=cm.coolwarm)

# ---Scatter empty sets
scatter = ax.scatter([], [])

# ---Create PSO object to be used in the animation frames
pso = PSO(function, scatter)

# ---Update scatter plot to display initial positions of the particles
scatter.set_offsets(
    [[particle.position.x, particle.position.y] for particle in pso.team.particles]
)

# ---Setup animation and show the first graph
animation = FuncAnimation(fig, pso.optimize, repeat=False, frames=np.arange(0, Const.N_ITERATIONS), interval=50)
plt.show()

# ---Plot particles history and show it
for particle in pso.team.particles:
    plt.plot([i for i in range(len(particle.altitude_history))], [i for i in particle.altitude_history])
plt.show()
