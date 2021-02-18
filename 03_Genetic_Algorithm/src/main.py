from Simulator import Simulator
import seaborn as sns
from matplotlib import pyplot as plt

if __name__ == '__main__':
    sim = Simulator()
    sim.start()
    sns.set_theme()
    plt.plot(
        [i for i in range(len(sim.population.avg_fitness))],
        sim.population.avg_fitness,
    )
    plt.plot(
        [i for i in range(len(sim.population.best_fitness))],
        sim.population.best_fitness,
    )
    plt.show()

