from typing import Dict, Callable

from plotly import graph_objects as go

import Constants as Const
import plotly.graph_objects as go
import numpy as np
import plotly.express as px

colors = px.colors.qualitative.Plotly


class VizTest:
    """
    Author = Frederic Abraham
    """

    def __init__(self, opti_func: Callable[[np.ndarray], float], data: Dict = None, title: str = None,
                 line_data: Dict = None):

        # Read data from a csv
        X, Y, Z = self.create_map_variables(opti_func)

        layout1 = go.Layout(
            scene=dict(
                xaxis=dict(nticks=4, range=[-10, 10], ),
                yaxis=dict(nticks=4, range=[-10, 10], ),
                zaxis=dict(nticks=4, range=[0, 200], ), ),
                updatemenus=[dict(type="buttons",
                                  buttons=[
                                      dict(label="Play",
                                           method="animate",
                                           args=[None, dict(frame=dict(duration=20, redraw=False),
                                                            transition=dict(duration=10, easing='linear')
                                                            )]
                                           )
                                  ])]
        )
        layout = layout1

        fig = go.Figure(
            layout=layout,
            data=go.Scatter(
                x=[data.get(0)[i].get("pos")[0][0] for i in range(len(data.get(0)))],
                y=[data.get(0)[i].get("pos")[1][0] for i in range(len(data.get(0)))],
                # z=[data.get(0)[i].get("alt") for i in range(len(data.get(0)))],
                mode="markers",
            )
        )

        # fig = fig.add_trace(
        #     go.Surface(x=X, y=Y, z=Z, colorscale='Blues', showscale=False)
        # )

        # fig.update_traces(contours_z=dict(show=True, usecolormap=True, highlightcolor="limegreen", project_z=True))

        frames = [
            go.Frame(
                data=[
                    go.Scatter(
                        x=[data.get(gen)[i].get("pos")[0][0] for i in range(len(data.get(gen)))],
                        y=[data.get(gen)[i].get("pos")[1][0] for i in range(len(data.get(gen)))],
                        # z=[data.get(gen)[i].get("alt") for i in range(len(data.get(gen)))],
                        mode="markers",
                    )
                ]
            )
            for gen in range(len(data))
        ]

        fig.frames = frames

        fig.update_layout(coloraxis_showscale=False)
        self.fig = fig
        # fig.show()
        # fig.write_html("index.html", include_plotlyjs='cdn', include_mathjax=False, auto_play=False)

    def show_fig(self):
        self.fig.show()

    def write_fig(self, write_title: str):
        self.fig.write_html(f'{write_title}.html', include_plotlyjs='cdn', include_mathjax=False, auto_play=False)

    @staticmethod
    def create_map_variables(opti_func):
        x_y_range = np.linspace(Const.MIN_POS, Const.MAX_POS, Const.grid_granularity)
        x_y_range = np.round(x_y_range, decimals=Const.precision)
        X, Y = np.meshgrid(x_y_range, x_y_range)
        Z = np.zeros(shape=(len(x_y_range), len(x_y_range)))
        for x in range(0, len(x_y_range)):
            for y in range(0, len(x_y_range)):
                Z[x, y] = opti_func(np.array([X[x, y], Y[x, y]])[np.newaxis, :].T)
        return X, Y, Z
