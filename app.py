from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import dash_vega_components as dvc
import altair as alt
import numpy as np
import pandas as pd
from vega_datasets import data

# To work with large datasets in Altair
alt.data_transformers.enable("vegafusion")

# Load data
df = data.cars()

# Initialize Dash app
app = Dash(__name__)
server = app.server

# Define layout
app.layout = html.Div(
    [
        html.H1("Cars dataset"),
        dcc.Dropdown(
            id="filter-dropdown",
            options=["Europe", "Japan", "USA"],
            multi=True,
        ),
        dvc.Vega(
            id="mychart",
            opt={"renderer": "svg", "actions": False},
            style={"width": "100%"},
        ),
    ]
)


# Controls
@callback(
    Output("mychart", "spec"),
    Input("filter-dropdown", "value"),
)
def update_chart(value):
    """
    Update the chart based on the selected values.
    """
    # Filter data
    if value:
        filtered_df = df[df["Origin"].isin(value)]
    else:
        filtered_df = df

    # Create chart
    chart = (
        alt.Chart(filtered_df)
        .mark_point()
        .encode(x="Weight_in_lbs", y="Horsepower", color="Origin")
    )
    return chart.to_dict(format="vega")


if __name__ == "__main__":
    app.run(debug=True)
