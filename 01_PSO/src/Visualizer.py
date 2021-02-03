from typing import Dict, Callable

import Constants as Const
import plotly.graph_objects as go
import numpy as np


class Visualizer:
    def __init__(self, opti_func: Callable[[np.ndarray], float], data: Dict = None):

        # Read data from a csv

        x_y_range = np.linspace(Const.MIN_POS, Const.MAX_POS, Const.grid_granularity)
        X, Y = np.meshgrid(x_y_range, x_y_range)

        Z = np.zeros(shape=(len(x_y_range), len(x_y_range)))
        for x in range(0, len(x_y_range)):
            for y in range(0, len(x_y_range)):
                Z[x, y] = opti_func(np.array([X[x, y], Y[x, y]]))

        layout = go.Layout(
            xaxis=dict(range=[Const.MIN_POS, Const.MAX_POS], autorange=False, zeroline=False),
            yaxis=dict(range=[Const.MIN_POS, Const.MAX_POS], autorange=False, zeroline=False),
            title_text='Chasing global Minima',
            updatemenus=[dict(type="buttons",
                              buttons=[
                                  dict(label="Play",
                                       method="animate",
                                       args=[None, dict(frame=dict(duration=5, redraw=True),
                                                        fromcurrent=True,
                                                        mode='next',
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

        frames = None
        if data is not None:
            frames = [
                go.Frame(
                    data=[
                        go.Scatter3d(
                            x=[data.get(k)[i][0] for i in range(len(data.get(k)))],
                            y=[data.get(k)[i][1] for i in range(len(data.get(k)))],
                            z=[opti_func(data.get(k)[i]) for i in range(len(data.get(k)))],
                            mode="markers",
                            marker=dict(size=10, color='red'))
                    ],
                    name=f'genration: {k}'
                )
                for k in range(len(data))
            ]

        fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale='Blues'),
                              go.Surface(x=X, y=Y, z=Z, colorscale='Blues')], layout=layout, frames=frames)

        fig.update_traces(contours_z=dict(show=True, usecolormap=True, highlightcolor="limegreen", project_z=True))

        camera = dict(
            up=dict(x=0, y=0, z=1),
            center=dict(x=0, y=0, z=0),
            eye=dict(x=1.25, y=1.25, z=1.25)
        )

        fig.update_layout(scene_camera=camera)

        fig.show()
