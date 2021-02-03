from typing import Dict, Callable, List

from plotly.subplots import make_subplots

import Constants as Const
import plotly.graph_objects as go
import numpy as np


class Visualizer:
    def __init__(self, opti_func: Callable[[np.ndarray], float], data: Dict = None, line_data: Dict = None):

        # Read data from a csv

        X, Y, Z = self.create_map_variables(opti_func)

        layout = self.create_layout()

        fig = make_subplots(rows=1, cols=2,
                            specs=[[{"type": "surface"}, {"type": "scatter"}]])

        fig = fig.add_trace(
            go.Surface(x=X, y=Y, z=Z, colorscale='Blues'),
            row=1, col=1
        )

        fig.update_traces(contours_z=dict(show=True, usecolormap=True, highlightcolor="limegreen", project_z=True),
                          row=1, col=1)

        # Add each line chart to the figure
        for key in line_data.keys():
            fig.add_trace(
                go.Scatter(
                    x=[0],
                    y=[line_data.get(key)[0]],
                    mode='lines',
                    name=str(key)
                ),
                row=1, col=2
            )

        frames = [
            go.Frame(
                data=self.get_current_data_frame(k, opti_func, data, line_data, X, Y, Z),
                name=f'genration: {k}'
            )
            for k in range(len(data))
        ]

        fig.frames = frames

        fig.update_layout(layout)

        fig.write_html("pso.html")

    def get_current_data_frame(self, gen, opti_func, data, line_data, X, Y, Z):
        ret_list = [
            go.Surface(x=X, y=Y, z=Z, colorscale='Blues'),
            go.Scatter3d(
                x=[data.get(gen)[i][0] for i in range(len(data.get(gen)))],
                y=[data.get(gen)[i][1] for i in range(len(data.get(gen)))],
                z=[opti_func(data.get(gen)[i]) for i in range(len(data.get(gen)))],
                mode="markers",
                marker=dict(size=10, color='red'))]

        for key in line_data.keys():
            ret_list.append(
                go.Scatter(
                    x=list(range(gen)),
                    y=line_data.get(key)[:gen],
                    mode='lines',
                    name=str(key)
                )
            )
        return ret_list

    def create_layout(self):
        layout = go.Layout(
            title_text='Chasing global Minima',
            updatemenus=[dict(type="buttons",
                              buttons=[
                                  dict(label="Play",
                                       method="animate",
                                       args=[None, dict(frame=dict(duration=5, redraw=True),
                                                        fromcurrent=True,
                                                        mode='immediate',
                                                        )]),
                                  dict(label="Pause",
                                       method="animate",
                                       args=[None,
                                             {"frame": {"duration": 0, "redraw": False},
                                              "mode": "immediate",
                                              "transition": {"duration": 0}}],
                                       )
                              ]
                              )
                         ]
        )
        return layout

    def create_map_variables(self, opti_func):
        x_y_range = np.linspace(Const.MIN_POS, Const.MAX_POS, Const.grid_granularity)
        X, Y = np.meshgrid(x_y_range, x_y_range)
        Z = np.zeros(shape=(len(x_y_range), len(x_y_range)))
        for x in range(0, len(x_y_range)):
            for y in range(0, len(x_y_range)):
                Z[x, y] = opti_func(np.array([X[x, y], Y[x, y]]))
        return X, Y, Z
