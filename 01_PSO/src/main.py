from ParticleSwarmOptimization import PSO
from OptimizationFunction import OptimizationFunction
from src.Visualizer import Visualizer
import Constants as Const


if __name__ == "__main__":

    opti = OptimizationFunction(a=0, b=100)
    selected_function = opti.rastrigin

    # ---Create PSO object to be used in the animation frames
    pso = PSO(selected_function)
    pso.optimize()
    #
    # for swarm in pso.swarms:
    #     for i in range(Const.N_ITERATIONS):
    #         print(str(pso.swarms.index(swarm)) + " " + str(i) + " " + str(list(filter(lambda data: data.get("best") and data.get('swarm') == pso.swarms.index(swarm), pso.history.get(i)))[0].get('id')))

    print("Optimization Done")

    viz = Visualizer(selected_function, pso.history,
               dict(
                   avg_vel=pso.average_velocity_history,
                   avg_alt=pso.average_altitude_history,
                   best_alt=pso.best_altitude_history,
               ))
    print("Viz Done")
    viz.show_fig()
    # viz.write_fig()