import plotly.graph_objects as go # or plotly.express as px

from src.OptimizationFunction import OptimizationFunction, OptiFunks
from src.ParticleSwarmOptimization import PSO
from src.Visualizer import Visualizer
import dash
import dash_core_components as dcc
import dash_html_components as html

opti = OptimizationFunction(a=1, b=100, selected_function=OptiFunks.Rastrigin)

# ---Create PSO object to be used in the animation frames
pso = PSO(opti.optimization_function)
pso.optimize()
print("Optimization Done")

viz = Visualizer(opti.optimization_function, pso.history,
           dict(
               avg_vel=pso.average_velocity_history,
               avg_alt=pso.average_altitude_history,
               best_alt=pso.best_altitude_history,
           ))

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=viz.fig)
])

app.run_server(debug=True, use_reloader=False)