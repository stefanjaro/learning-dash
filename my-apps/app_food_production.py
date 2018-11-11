# import libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

# import data
df = pd.read_csv("FAO.csv", encoding="iso-8859-1")
# get column names of production years
year_col_names = list(df.columns[10:])

# set external stylesheets and initiate app instance
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# configure app layout
app.layout = html.Div([
    html.Div([
        html.H1("Worldwide Food & Feed Production", style={"text-align": "center"})
    ]),

    # dropdown for country
    html.Div([
        html.Label("Country"),
        dcc.Dropdown(
            id="selected-country",
            options=[{"label": i, "value": i} for i in df.Area.unique()],
            value="Afghanistan"
        )], style={"width": "30%", "display": "inline-block"}),

    # dropdown for item
    html.Div([
        html.Label("Item"),
        dcc.Dropdown(
            id="selected-item",
            options=[{"label": i, "value": i} for i in df.Item.unique()],
            value="Wheat and products"
        )], style={"width": "30%", "display": "inline-block"}),

    # dropdown for element
    html.Div([
        html.Label("Element"),
        dcc.Dropdown(id="selected-element")
        ], style={"width": "30%", "display": "inline-block"}),

    # graph element to be populated
    html.Div([
        dcc.Graph(id="graph-element")
    ], style={"width": "100%", "display": "inline-block"}),
])


# update element dropdown because some choices don't have both food and feed
@app.callback(
    Output("selected-element", "options"),
    [Input("selected-country", "value"),
     Input("selected-item", "value")]
)
def update_element_choices(selected_country, selected_item):
    # filter df
    filtered_df = df[(df["Area"] == selected_country) &
                     (df["Item"] == selected_item)]
    # return choices
    return [
        {"label": i, "value": i} for i in filtered_df.Element.unique()
    ]

# return a default value to element dropdown
@app.callback(
    Output("selected-element", "value"),
    [Input("selected-element", "options")]
)
def update_element_value(available_options):
    return available_options[0]["value"]

# update graph
@app.callback(
    Output("graph-element", "figure"),
    [Input("selected-country", "value"),
     Input("selected-item", "value"),
     Input("selected-element", "value")]
)
def update_graph(selected_country, selected_item, selected_element):
    # filter dataframe
    filtered_df = df[(df["Area"] == selected_country) &
                     (df["Item"] == selected_item) &
                     (df["Element"] == selected_element)]

    # return graph parameters
    return {
        "data": [
            go.Bar(
                x=year_col_names,
                y=filtered_df[year_col_names].values.tolist()[0]
            )
        ],

        "layout": go.Layout(
            xaxis={"title": "Production Years"},
            yaxis={"title": "1000 Tonnes"}
        )
    }

if __name__ == "__main__":
    app.run_server(debug=True)