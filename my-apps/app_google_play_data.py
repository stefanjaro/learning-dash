# import libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

#import data
df = pd.read_csv("googleplaystore.csv")

# set external stylesheets and initiate app instance
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# configure app layout
app.layout = html.Div(children=[
    html.Div(children=[
        html.H1("Google Play Store Data Visualization", style={"text-align": "center"})
    ]),
    
    # dropdown for app category
    html.Div([
        html.Label("App Category"),
        dcc.Dropdown(
            id="app-category",
            options=[{"label": i, "value": i} for i in df.Category.unique()]
        )], 
        style={
            "width": "30%", 
            "display": "inline-block",
            "margin": {"l": 50, "t": 50, "b": 50, "r": 50}}),

    # dropdown for number of app installs
    html.Div([
        html.Label("App Installs"),
        dcc.Dropdown(
            id="app-installs",
            options=[{"label": i, "value": i} for i in df.Installs.unique()]
        )], 
        style={
            "width": "30%",
            "display": "inline-block",
            "margin": {"l": 50, "t": 50, "b": 50, "r": 50}
            }),

    # dropdown for type of app
    html.Div([
        html.Label("App Type"),
        dcc.Dropdown(
            id="app-type",
            options=[{"label": i, "value": i} for i in df.Type.unique()]
        )], 
        style={
            "width": "30%", 
            "display": "inline-block", 
            "margin": {"l": 50, "t": 50, "b": 50, "r": 50}
            }),

    # graph to display filtered data
    html.Div([
        dcc.Graph(id="filtered-graph")
    ], style={"width": "100%", "display": "inline-block"})
])

@app.callback(
    Output("filtered-graph", "figure"),
    [Input("app-category", "value"),
     Input("app-installs", "value"),
     Input("app-type", "value")]
)
def update_graph(app_category, app_installs, app_type):
    # filter dataset
    filtered_df = df[(df["Category"] == app_category) & 
                     (df["Installs"] == app_installs) & 
                     (df["Type"] == app_type)]

    # return scatter of reviews against ratings
    return {
        "data": [
            go.Scatter(
                x=filtered_df["Reviews"],
                y=filtered_df["Rating"],
                text=filtered_df["App"],
                mode="markers",
                opacity=0.7,
                marker={
                    "size": 15,
                    "line": {"width": 0.5, "color": "white"}
                },
            )
        ],

        "layout": go.Layout(
            xaxis={"type": "linear", "title": "# of Reviews"},
            yaxis={"type": "linear", "title": "# of Ratings"},
            margin={"l": 40, "r": 40, "b": 40, "t": 40}
        )
    }

# run the app
if __name__ == "__main__":
    app.run_server(debug=True)