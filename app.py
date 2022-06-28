# Import required libraries
import pickle
import copy
import pathlib
import urllib.request
import dash
import math
import datetime as dt
from dash_core_components.Interval import Interval
from dash_html_components.Br import Br
from dash_html_components.Div import Div
from dash_html_components.Label import Label
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objs as go
import dash_table
import numpy as np
import yaml
from queries import *


app = dash.Dash(
    __name__, meta_tags=[
        {"name": "viewport", "content": "width=device-width"}],
)
app.title = "Kamp Lintfort park"
server = app.server

# ============= data source for tree species and sensors id
df2 = pd.read_csv("tree_location.csv")
fig = px.line(df2, x="sensor_id", y="tree_species", labels={
    "sensor_id": "Sensors Id",
    "tree_species": "Tree Species"},
    title='Trees species and sensors id')


# df3 = get_table("kali", "meas")


# filter based on sm

# sm = df3["variable_type"].isin(["sm"])

# sm = smtemp[smtemp['sensor_id'] == 'lse01_02']

# more options can be specified also
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     print(sm)

# print(sm.head(500))

# print(df3)
# print(df3[sm])

# figure sm


# ========================= filter based on ec

# ec = df3["variable_type"].isin(["ec"])

# # figure ec
# fig_ec = px.line(df3[ec], x="ts", y="val",
#                  color='sensor_id', labels={
#     "ts": "Time",
#     "val": "Soil Conductivity", "sensor_id": "sensors id"}, title="Soil Conductivity")

# # based on Temperature
# temp = df3["variable_type"].isin(["temp"])

# # figure Temperature
# fig_temp = px.line(df3[temp], x="ts", y="val",
#                    color='sensor_id', labels={
#     "ts": "Time",
#     "val": "Temprature", "sensor_id": "sensors id"}, title="Temperature")


# Create app layout
app.layout = html.Div(
    [

        html.Div(
            [

                html.Div(
                    [

                        html.H3(
                            "Kamp Lintfort park",
                            style={"margin-bottom": "0px",
                                   'font-weight': 'bold'},
                        ),
                    ],
                    className="three column",
                    id="title",
                ),

            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.Div(
                    [

                        dcc.RadioItems(
                            id="data_type",
                            options=[
                                {'label': 'All Trees ',
                                    'value': 'all'},
                                {'label': 'Active Sensors', 'value': 'active'},

                            ],
                            value='all',


                            labelStyle={"display": "inline-block"},
                            className="dcc_control",
                        ),
                        html.P("choose the time:",
                               className="control_label"),
                        dcc.Dropdown(
                            id="time",
                            options=[

                                {"label": "Last 15 min", "value": "15min"},
                                {"label": "Last 30 min", "value": "30min"},
                                {"label": "Last 1 hour", "value": "1hr"},
                                {"label": "Last 3 hours", "value": "3hr"},
                                {"label": "Last 6 hours", "value": "6hr"},
                                {"label": "Last 12 hour", "value": "12hr"},
                                {"label": "Last 24 hours", "value": "24hr"},
                                {"label": "Last 2 days", "value": "2d"},
                                {"label": "Last 7 days", "value": "7d"},
                            ],
                            multi=False,
                            value='30min',
                            className="dcc_control",
                        ),
                    ],
                    # ==========================================
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    [html.Div([html.P("Batrry life time (Voltage)", style={"margin-bottom": "0px",
                                                                           'font-weight': 'bold', 'text-align': 'center'},
                                      className="control_label"),
                               html.Div(
                        [

                            html.Div(
                                [html.H6(id="sen1"),
                                 html.P("lse01_01")],
                                id="sen_1",
                                className="mini_container",
                            ),
                            html.Div(
                                [html.H6(id="sen2"),
                                 html.P("lse01_02")],
                                id="sen_2",
                                className="mini_container",
                            ),
                            html.Div(
                                [html.H6(id="sen3"),
                                 html.P("lse01_03")],
                                id="sen_3",
                                className="mini_container",
                            ),
                            html.Div(
                                [html.H6(id="sen4"),
                                 html.P("lse01_04")],
                                id="sen_4",
                                className="mini_container",
                            ),
                            html.Div(
                                [html.H6(id="sen5"), html.P("lse01_05")],
                                id="sen_5",
                                className="mini_container",
                            ),
                        ],
                        id="info-container",
                        className="row container-display",
                    ),
                    ]),
                        #     html.Div(
                        #     [dcc.Graph(id="count_graph", figure=fig)],
                        #     id="countGraphContainer",
                        #     className="pretty_container",
                        # ),
                    ],
                    id="right-column",
                    className="eight columns pretty_container  ",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [html.Div([

                dcc.Graph(id='live-update-graph',
                          config={'displayModeBar': False, 'scrollZoom': True}),
                dcc.Interval(
                    id='interval-component',
                    interval=60*1000,  # in milliseconds
                    n_intervals=0
                )
            ], className="pretty_container twelve columns"),

                #     html.Div(
                #     [dcc.Graph(id="individual_graph", figure=fig)],
                #     className="pretty_container five columns",
                # ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(
                        id="line-graph-sm", config={'displayModeBar': False})],
                    className="pretty_container twelve columns",
                ),

                # html.Div(
                #     [dcc.Graph(id="aggregate_graph")],
                #     className="pretty_container five columns",
                # ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [dcc.Graph(id="line_graph_ec", config={
                       'displayModeBar': False})],
            className="pretty_container twelve columns",
        ),
        html.Div(
            [dcc.Graph(id="line_graph_temp", config={
                       'displayModeBar': False})],
            className="pretty_container twelve columns",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)
# ===============================callback ec


@ app.callback(
    Output("line_graph_ec", "figure"),
    [Input('time', 'value'), Input('interval-component', 'n_intervals')]

)
def update_time(t, n):

    if t == "15min":
        df5 = get_15min("kali", "meas")
        sm = df5[df5['variable_type'] == 'ec']
        fig_sm1 = px.line(sm, x="timezone", y="val", color="sensor_id", labels={
            "timezone": "Local Time",
            "val": "Soil conductivity (µS/cm)", "sensor_id": "sensors id"})

    if t == "30min":

        df5 = get_30min("kali", "meas")
        sm = df5[df5['variable_type'] == 'ec']
        fig_sm1 = px.line(sm, x="timezone", y="val", color="sensor_id", labels={
            "timezone": "Local Time",
            "val": "Soil conductivity (µS/cm)", "sensor_id": "sensors id"})

    if t == "1hr":
        df5 = get_1hr("kali", "meas")
        sm = df5[df5['variable_type'] == 'ec']
        fig_sm1 = px.line(sm, x="timezone", y="val", color="sensor_id", labels={
            "timezone": "Local Time",
            "val": "Soil conductivity (µS/cm)", "sensor_id": "sensors id"})

    if t == "3hr":
        df5 = get_3hr("kali", "meas")
        sm = df5[df5['variable_type'] == 'ec']
        fig_sm1 = px.line(sm, x="timezone", y="val", color="sensor_id", labels={
            "timezone": "Local Time",
            "val": "Soil conductivity (µS/cm)", "sensor_id": "sensors id"})
    if t == "6hr":
        df5 = get_6hr("kali", "meas")
        sm = df5[df5['variable_type'] == 'ec']
        fig_sm1 = px.line(sm, x="timezone", y="val", color="sensor_id", labels={
            "timezone": "Local Time",
            "val": "Soil conductivity (µS/cm)", "sensor_id": "sensors id"})
    if t == "12hr":
        df5 = get_12hr("kali", "meas")
        sm = df5[df5['variable_type'] == 'ec']
        fig_sm1 = px.line(sm, x="timezone", y="val", color="sensor_id", labels={
            "timezone": "Local Time",
            "val": "Soil conductivity (µS/cm)", "sensor_id": "sensors id"})

    if t == "24hr":
        df5 = get_24hr("kali", "meas")
        sm = df5[df5['variable_type'] == 'ec']
        fig_sm1 = px.line(sm, x="timezone", y="val", color="sensor_id", labels={
            "timezone": "Local Time",
            "val": "Soil conductivity (µS/cm)", "sensor_id": "sensors id"})

    if t == "2d":
        df5 = get_2d("kali", "meas")
        sm = df5[df5['variable_type'] == 'ec']
        fig_sm1 = px.line(sm, x="timezone", y="val", color="sensor_id", labels={
            "timezone": "Local Time",
            "val": "Soil conductivity (µS/cm)", "sensor_id": "sensors id"})

    if t == "7d":
        df5 = get_7d("kali", "meas")
        sm = df5[df5['variable_type'] == 'ec']
        fig_sm1 = px.line(sm, x="timezone", y="val", color="sensor_id", labels={
            "timezone": "Local Time",
            "val": "Soil conductivity (µS/cm)", "sensor_id": "sensors id"})
    fig_sm1.update_layout(
        title="Soil conductivity",

        font=dict(
            family="Arial",
            size=16,
            color="black"
        )
    )
    return fig_sm1

# ======================================== callback temp


@ app.callback(
    Output("line_graph_temp", "figure"),
    [Input('time', 'value'), Input('interval-component', 'n_intervals')]
)
def update_time(t, n):

    if t == "15min":
        df5 = get_15min("kali", "meas")
        sm = df5[df5['variable_type'] == 'temp']
        fig_sm1 = px.line(sm, x="timezone", y="val", color="sensor_id", labels={
            "timezone": "Local Time",
            "val": "Temperature (°C)", "sensor_id": "sensors id"})

    if t == "30min":

        df5 = get_30min("kali", "meas")
        sm = df5[df5['variable_type'] == 'temp']
        fig_sm1 = px.line(sm, x="timezone", y="val", color="sensor_id", labels={
            "timezone": "Local Time",
            "val": "Temperature (°C)", "sensor_id": "sensors id"})

    if t == "1hr":
        df5 = get_1hr("kali", "meas")
        sm = df5[df5['variable_type'] == 'temp']
        fig_sm1 = px.line(sm, x="timezone", y="val", color="sensor_id", labels={
            "timezone": "Local Time",
            "val": "Temperature (°C)", "sensor_id": "sensors id"})

    if t == "3hr":
        df5 = get_3hr("kali", "meas")
        sm = df5[df5['variable_type'] == 'temp']
        fig_sm1 = px.line(sm, x="timezone", y="val", color="sensor_id", labels={
            "timezone": "Local Time",
            "val": "Temperature (°C)", "sensor_id": "sensors id"})
    if t == "6hr":
        df5 = get_6hr("kali", "meas")
        sm = df5[df5['variable_type'] == 'temp']
        fig_sm1 = px.line(sm, x="timezone", y="val", color="sensor_id", labels={
            "timezone": "Local Time",
            "val": "Temperature (°C)", "sensor_id": "sensors id"})
    if t == "12hr":
        df5 = get_12hr("kali", "meas")
        sm = df5[df5['variable_type'] == 'temp']
        fig_sm1 = px.line(sm, x="timezone", y="val", color="sensor_id", labels={
            "timezone": "Local Time",
            "val": "Temperature (°C)", "sensor_id": "sensors id"})

    if t == "24hr":
        df5 = get_24hr("kali", "meas")
        sm = df5[df5['variable_type'] == 'temp']
        fig_sm1 = px.line(sm, x="timezone", y="val", color="sensor_id", labels={
            "timezone": "Local Time",
            "val": "Temperature (°C)", "sensor_id": "sensors id"})

    if t == "2d":
        df5 = get_2d("kali", "meas")
        sm = df5[df5['variable_type'] == 'temp']
        fig_sm1 = px.line(sm, x="timezone", y="val", color="sensor_id", labels={
            "timezone": "Local Time",
            "val": "Temperature (°C)", "sensor_id": "sensors id"})

    if t == "7d":
        df5 = get_7d("kali", "meas")
        sm = df5[df5['variable_type'] == 'temp']
        fig_sm1 = px.line(sm, x="timezone", y="val", color="sensor_id", labels={
            "timezone": "Local Time",
            "val": "Temperature (°C)", "sensor_id": "sensors id"})
    fig_sm1.update_layout(
        title="Temperature",
        font=dict(
            family="Arial",
            size=16,
            color="black"
        )
    )
    return fig_sm1

    # ===============call back sm


@ app.callback(
    Output("line-graph-sm", "figure"),
    [Input('time', 'value'), Input('interval-component', 'n_intervals')]


)
def update_time(t, n):

    if t == "15min":
        df5 = get_15min("kali", "meas")
        sm = df5[df5['variable_type'] == 'sm']
        fig_sm1 = px.line(sm, x="timezone", y="val", color="sensor_id", labels={
            "timezone": "Local Time",
            "val": "Soil Moistures (%H)", "sensor_id": "sensors id"})

    if t == "30min":

        df5 = get_30min("kali", "meas")
        sm = df5[df5['variable_type'] == 'sm']
        fig_sm1 = px.line(sm, x="timezone", y="val", color="sensor_id", labels={
            "timezone": "Local Time",
            "val": "Soil Moistures (%H)", "sensor_id": "sensors id"})

    if t == "1hr":
        df5 = get_1hr("kali", "meas")
        sm = df5[df5['variable_type'] == 'sm']
        fig_sm1 = px.line(sm, x="timezone", y="val", color="sensor_id", labels={
            "timezone": "Local Time",
            "val": "Soil Moistures (%H)", "sensor_id": "sensors id"})

    if t == "3hr":
        df5 = get_3hr("kali", "meas")
        sm = df5[df5['variable_type'] == 'sm']
        fig_sm1 = px.line(sm, x="timezone", y="val", color="sensor_id", labels={
            "timezone": "Local Time",
            "val": "Soil Moistures (%H)", "sensor_id": "sensors id"})
    if t == "6hr":
        df5 = get_6hr("kali", "meas")
        sm = df5[df5['variable_type'] == 'sm']
        fig_sm1 = px.line(sm, x="timezone", y="val", color="sensor_id", labels={
            "timezone": "Local Time",
            "val": "Soil Moistures (%H)", "sensor_id": "sensors id"})
    if t == "12hr":
        df5 = get_12hr("kali", "meas")
        sm = df5[df5['variable_type'] == 'sm']
        fig_sm1 = px.line(sm, x="timezone", y="val", color="sensor_id", labels={
            "timezone": "Local Time",
            "val": "Soil Moistures (%H)", "sensor_id": "sensors id"})

    if t == "24hr":
        df5 = get_24hr("kali", "meas")
        sm = df5[df5['variable_type'] == 'sm']
        fig_sm1 = px.line(sm, x="timezone", y="val", color="sensor_id", labels={
            "timezone": "Local Time",
            "val": "Soil Moistures (%H)", "sensor_id": "sensors id"})

    if t == "2d":
        df5 = get_2d("kali", "meas")
        sm = df5[df5['variable_type'] == 'sm']
        fig_sm1 = px.line(sm, x="timezone", y="val", color="sensor_id", labels={
            "timezone": "Local Time",
            "val": "Soil Moistures(%H)", "sensor_id": "sensors id"})

    if t == "7d":
        df5 = get_7d("kali", "meas")
        sm = df5[df5['variable_type'] == 'sm']
        fig_sm1 = px.line(sm, x="timezone", y="val", color="sensor_id", labels={
            "timezone": "Local Time",
            "val": "Soil Moistures (%H)", "sensor_id": "sensors id"})
    fig_sm1.update_layout(
        title="Soil Moisture",
        font=dict(
            family="Arial",
            size=16,
            color="black"
        )
    )
    return fig_sm1


# ===============================update batrrty life time
@ app.callback(
    [
        Output("sen1", "children"),
        Output("sen2", "children"),
        Output("sen3", "children"),
        Output("sen4", "children"),
        Output("sen5", "children"),

    ],
    [Input('interval-component', 'n_intervals')],
)
def update_bat(n):
    df4 = get_battry("kali", "meas")
    return df4['val'][0], df4['val'][1], df4['val'][2], df4['val'][3], df4['val'][4]

# ======================update map


@ app.callback(Output('live-update-graph', 'figure'), [Input('interval-component', 'n_intervals'), Input('data_type', 'value')])
def update_graph_live(n, x):

    if x == "all":
        fig = px.scatter_mapbox(df2, title="All Trees in Kamp-Lintfort Park", lat="latitude", lon="longitude", hover_name="tree_number", hover_data=["tree_species"],
                                zoom=15, height=500, size_max=5,)
        fig.update_layout(mapbox_style="open-street-map", title_x=0.5,
                          title_y=0.95, font_size=16,)
        fig.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})

    if x == "active":
        df6 = get_location("kali", "location")
        fig = px.scatter_mapbox(df6, title="All active sensors in Kamp-Lintfort Park", lat="latitude", lon="longitude", hover_name="tree_number", hover_data=[
                                "sensor_id", "sm", "ec", "temp"], size='sm', color='sensor_id', labels={
            "sensor_id": "sensors Id", "sm": "Soil Moistures (%H)", "ec": "soil conductivity (µS/cm)", "temp": "Temperature (°C)"}, color_continuous_scale=px.colors.sequential.YlOrRd, zoom=15, height=500, size_max=5,)
        fig.update_layout(mapbox_style="open-street-map",  title_x=0.5,
                          title_y=0.95, font_size=16)
        fig.update_layout(margin={
                          "r": 0, "t": 50, "l": 0, "b": 0})

    return fig


# Main
if __name__ == "__main__":
    app.run_server(debug=True)
