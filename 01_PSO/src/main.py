from ParticleSwarmOptimization import PSO
from OptimizationFunction import OptimizationFunction, OptiFunks
from src.Visualizer import Visualizer

if __name__ == "__main__":

    opti = OptimizationFunction(a=1, b=100, selected_function=OptiFunks.Rosenbrock)

    # ---Create PSO object to be used in the animation frames
    pso = PSO(opti.optimization_function)
    pso.optimize()
    Visualizer(opti.optimization_function, pso.history,
               dict(
                   avg_vel=pso.average_velocity_history,
                   avg_alt=pso.average_altitude_history,
                   best_alt=pso.best_altitude_history,
               ))
