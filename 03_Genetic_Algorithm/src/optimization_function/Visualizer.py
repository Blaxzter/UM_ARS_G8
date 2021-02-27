from typing import Dict, Callable, List

from colour import Color
from plotly.subplots import make_subplots

import Constants as Const
import plotly.graph_objects as go
import numpy as np
import plotly.express as px

colors = px.colors.qualitative.Plotly


class Visualizer:
    """
    Author = Frederic Abraham
    """

    def __init__(self, opti_func: Callable[[np.ndarray], float], data: Dict = None, title: str = None,
                 line_data: Dict = None):

        # Read data from a csv
        X, Y, Z = self.create_map_variables(opti_func)

        layout = self.create_layout(title if title is not None else "PSO Visualization")

        fig = make_subplots(rows=1, cols=2,
                            specs=[[{"type": "surface"}, {"type": "scatter"}]])

        fig = fig.add_trace(
            go.Surface(x=X, y=Y, z=Z, colorscale='Blues', showscale=False),
            row=1, col=1
        )

        fig.update_traces(contours_z=dict(show=True, usecolormap=True, highlightcolor="limegreen", project_z=True),
                          row=1, col=1)

        fig = fig.add_trace(
            go.Scatter3d(
                x=[data.get(0)[i].get("pos")[0][0] for i in range(len(data.get(0)))],
                y=[data.get(0)[i].get("pos")[1][0] for i in range(len(data.get(0)))],
                z=[data.get(0)[i].get("alt") for i in range(len(data.get(0)))],
                hovertext=[f'team {data.get(0)[i].get("swarm")}' for i in range(len(data.get(0)))],
                hoverinfo="text",
                mode="markers",
                name=f'Particle',
                marker=dict(
                    color=[Color(colors[particle_info.get("swarm")], luminance=0.3).get_hex() if particle_info.get(
                        "best") else colors[particle_info.get("swarm")] for particle_info in data.get(0)],
                    size=10)
            ),
            row=1, col=1
        )

        fig = fig.add_trace(
            go.Scatter3d(
                x=[data.get(0)[i].get("pos")[0][0] for i in range(len(data.get(0)))],
                y=[data.get(0)[i].get("pos")[1][0] for i in range(len(data.get(0)))],
                z=[-2.5 for _ in range(len(data.get(0)))],
                hovertext=[f'team {data.get(0)[i].get("swarm")}' for i in range(len(data.get(0)))],
                hoverinfo="text",
                mode="markers",
                showlegend=False,
                marker=dict(
                    color=[
                        Color(colors[particle_info.get("swarm")], luminance=0.3).get_hex()
                        if particle_info.get("best") else colors[particle_info.get("swarm")]
                        for particle_info in data.get(0)],
                    size=5)
            ),
            row=1, col=1
        )

        # Add each line chart to the figure
        style = ['solid', 'dash', 'dot']
        counter = 0
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
            counter += 1

        sliders_dict = self.create_slider(data)

        frames = [
            go.Frame(
                data=self.get_current_data_frame(k, data, line_data),
                name=str(k),
                traces=list(range(1, len(fig.data)))
            )
            for k in range(len(data))
        ]

        fig.frames = frames
        layout["sliders"] = [sliders_dict]

        fig.update_layout(layout)
        fig.update_layout(coloraxis_showscale=False)
        self.fig = fig
        # fig.show()
        # fig.write_html("index.html", include_plotlyjs='cdn', include_mathjax=False, auto_play=False)

    def create_slider(self, data):
        sliders_dict = {
            "active": 0,
            "yanchor": "top",
            "xanchor": "left",
            "currentvalue": {
                "font": {"size": 20},
                "prefix": "Generation:",
                "visible": True,
                "xanchor": "right"
            },
            "transition": dict(duration=5, easing='linear'),
            "pad": {"b": 10, "t": 50},
            "len": 0.9,
            "x": 0.1,
            "y": 0,
            "steps": [
                {"args": [
                    [k],
                    {"frame": dict(duration=5, redraw=True),
                     "mode": "immediate",
                     "transition": dict(duration=0, easing='linear')}
                ],
                    "label": k,
                    "method": "animate"} for k in range(len(data))
            ]
        }
        return sliders_dict

    def show_fig(self):
        self.fig.show()

    def write_fig(self, write_title: str):
        self.fig.write_html(f'{write_title}.html', include_plotlyjs='cdn', include_mathjax=False, auto_play=False)

    def get_current_data_frame(self, gen, data, line_data):
        ret_list = [
            go.Scatter3d(
                x=[data.get(gen)[i].get("pos")[0][0] for i in range(len(data.get(gen)))],
                y=[data.get(gen)[i].get("pos")[1][0] for i in range(len(data.get(gen)))],
                z=[data.get(gen)[i].get("alt") for i in range(len(data.get(gen)))],
                hovertext=[f'team {data.get(gen)[i].get("swarm")}' for i in range(len(data.get(0)))],
                hoverinfo="text",
                mode="markers",
                marker=dict(
                    color=[Color(colors[particle_info.get("swarm")], luminance=0.3).get_hex() if particle_info.get(
                        "best") else colors[particle_info.get("swarm")] for particle_info in data.get(gen)],
                    size=10)),
            go.Scatter3d(
                x=[data.get(gen)[i].get("pos")[0][0] for i in range(len(data.get(gen)))],
                y=[data.get(gen)[i].get("pos")[1][0] for i in range(len(data.get(gen)))],
                z=[-2.5 for _ in range(len(data.get(gen)))],
                hovertext=[f'team {data.get(gen)[i].get("swarm")}' for i in range(len(data.get(0)))],
                hoverinfo="text",
                mode="markers",
                marker=dict(
                    color=[Color(colors[particle_info.get("swarm")], luminance=0.3).get_hex() if particle_info.get(
                        "best") else colors[particle_info.get("swarm")] for particle_info in data.get(gen)],
                    size=5))
        ]

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

    def create_layout(self, title):
        layout = go.Layout(
            title_text=title,
            updatemenus=[dict(type="buttons",
                              buttons=[
                                  dict(label="Play",
                                       method="animate",
                                       args=[None, dict(frame=dict(duration=5, redraw=False),
                                                        fromcurrent=True,
                                                        transition=dict(duration=0, easing='linear')
                                                        )]
                                       ),
                                  dict(label="Pause",
                                       method="animate",
                                       args=[[None],
                                             dict(frame=dict(duration=0, redraw=False),
                                                  mode='immediate',
                                                  transition=dict(duration=0)
                                                  )],
                                       )
                              ],
                              direction="left",
                              pad={"r": 10, "t": 87},
                              showactive=False,
                              x=0.1,
                              xanchor="right",
                              y=0,
                              yanchor="top"
                              )]
        )
        return layout

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
