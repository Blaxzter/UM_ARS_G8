import math

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from enum import Enum

import Constants as Const
from ParticleSwarmOptimization import PSO

a = 0
b = 100


class OptiFunks(Enum):
    Rosenbrock = 1
    Rastrigin = 2


c_opti_func = OptiFunks.Rastrigin


def rosenbrock(x: float, y: float):
    return (a - x) ** 2 + b * (y - x ** 2) ** 2


def rastrigin(pos: np.ndarray):
    return 10 * 2 + np.sum(pos ** 2 - 10 * np.cos(2 * math.pi * pos))


def optimization_function(pos: np.ndarray) -> float:
    if c_opti_func == OptiFunks.Rosenbrock:
        if len(pos) >= 2:
            return rosenbrock(pos[0], pos[1])
        else:
            raise Exception("Not enough dimensions")

    if c_opti_func == OptiFunks.Rastrigin:
        return rastrigin(pos)


if __name__ == "__main__":
    # ---Create fig and subplot
    fig, ax = plt.subplots()
    fig.set_tight_layout(True)
    ax.set_xlim([Const.MIN_POS, Const.MAX_POS])
    ax.set_ylim([Const.MIN_POS, Const.MAX_POS])

    # --Setup and plot function contour
    x_y_range = np.linspace(Const.MIN_POS, Const.MAX_POS, Const.grid_granularity)
    X, Y = np.meshgrid(x_y_range, x_y_range)

    Z = np.zeros(shape=(len(x_y_range), len(x_y_range)))
    for _x in range(0, len(x_y_range)):
        for _y in range(0, len(x_y_range)):
            Z[_x, _y] = optimization_function(np.array([X[_x, _y], Y[_x, _y]]))

    contour = ax.contourf(X, Y, Z, 100)
    plt.colorbar(contour, ax=ax)

    # ---Create PSO object to be used in the animation frames
    pso = PSO(optimization_function)
    pso.optimize()

    ax.scatter([0], [0], color='w')  # Global Min - Rosenbrock & Rastrigin


    # ---Scatter empty sets
    scatter = ax.scatter([], [], marker='x', color='r')


    def my_animation(frame_data):
        next_offset = []

        for particle in pso.team.particles:
            next_offset.append(particle.position_history[frame_data])

        scatter.set_offsets(next_offset)


    # ---Setup animation and show the first graph
    animation = FuncAnimation(fig, my_animation, repeat=False, frames=np.arange(0, Const.N_ITERATIONS), interval=5)
    plt.show()

    # ---Plot particles history and show it
    for particle in pso.team.particles:
        plt.plot([i for i in range(len(particle.altitude_history))], [i for i in particle.altitude_history])
    plt.show()

    # ---Plot particles history and show it
    for particle in pso.team.particles:
        plt.plot([i for i in range(len(particle.velocity_history))], [i for i in particle.velocity_history])
    plt.show()

    # ---Plot swarm history and show it
    plt.plot([i for i in range(len(pso.best_altitude_history))], [i for i in pso.best_altitude_history], linewidth=3)

    # ---Plot swarm history and show it
    plt.plot([i for i in range(len(pso.average_altitude_history))], [i for i in pso.average_altitude_history], linewidth=3)

    # ---Plot swarm history and show it
    plt.plot([i for i in range(len(pso.average_velocity_history))], [i for i in pso.average_velocity_history], linewidth=3)
    plt.show()
