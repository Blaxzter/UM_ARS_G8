import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots

from src.OptimizationFunction import OptimizationFunction
from src.ParticleSwarmOptimization import PSO
import plotly.graph_objects as go

import Constants as Const

if __name__ == '__main__':

    repeats = 50
    func_name = 'Rastrigin'

    to_be_tested_values = np.linspace(0, 2, 10)

    opti = OptimizationFunction(a=0, b=100)
    selected_function = opti.rastrigin

    data = {to_be_tested_value: dict(
        avg_vel=[],
        avg_alt=[],
        best_alt=[],
    ) for to_be_tested_value in to_be_tested_values}

    for to_be_tested_value in to_be_tested_values:
        Const.C1 = to_be_tested_value
        for repeat in range(repeats):
            # ---Create PSO object to be used in the animation frames
            pso = PSO(selected_function)
            pso.optimize()
            data.get(to_be_tested_value).get('avg_vel').append(pso.average_velocity_history)
            data.get(to_be_tested_value).get('avg_alt').append(pso.average_altitude_history)
            data.get(to_be_tested_value).get('best_alt').append(pso.best_altitude_history)

    fig = make_subplots(rows=2, cols=2, subplot_titles=("Average Velocity", "Average Altitude", "Best Altitude", ""))

    colors = px.colors.qualitative.Plotly

    for i, to_be_tested_value in enumerate(to_be_tested_values):
        fig.add_trace(go.Scatter(x=list(range(Const.N_ITERATIONS)),
                                 y=np.mean(data.get(to_be_tested_value).get('avg_vel'), axis=0),
                                 name=f'C1 = {np.round(to_be_tested_value, decimals=3)}',
                                 line=dict(color=colors[i], width=1)
                                 ),
                      row=1, col=1)

    for i, to_be_tested_value in enumerate(to_be_tested_values):
        fig.add_trace(go.Scatter(x=list(range(Const.N_ITERATIONS)),
                                 y=np.mean(data.get(to_be_tested_value).get('avg_alt'), axis=0),
                                 name=f'C1 = {to_be_tested_value}',
                                 showlegend=False,
                                 line=dict(color=colors[i], width=1)
                                 ),
                      row=1, col=2)

    for i, to_be_tested_value in enumerate(to_be_tested_values):
        fig.add_trace(go.Scatter(x=list(range(Const.N_ITERATIONS)),
                                 y=np.mean(data.get(to_be_tested_value).get('best_alt'), axis=0),
                                 name=f'C1 = {to_be_tested_value}',
                                 showlegend=False,
                                 line=dict(color=colors[i], width=1)
                                 ),
                      row=2, col=1)

    fig.update_layout(
        title_text=f"Testing of multiple cognitive velocity parameter for {func_name} avg over {repeats} tries"
    )
    fig.show()
    fig.write_html(f"{func_name}Analysis.html", include_plotlyjs='cdn', include_mathjax=False, auto_play=False)
