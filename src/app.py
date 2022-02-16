import altair as alt
from dash import Dash, html, dcc, Input, Output
from vega_datasets import data

seattle_temps = data.seattle_temps()
seattle_temps["month"] = seattle_temps["date"].dt.month_name()
seattle_temps["day"] = seattle_temps["date"].dt.day

def plot_seattle_temps(months):
    plot = (
        alt.Chart(seattle_temps[seattle_temps["month"] == months])
        .encode(x="day",
                y=alt.Y("mean(temp)",
                        scale=alt.Scale(zero=False)),
                tooltip=["mean(temp)"])
        .mark_line()
    )

    return (plot + plot.mark_circle()).to_html()

app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server

app.layout = html.Div(
    [
        dcc.Dropdown(
            id="months",
            value="January",
            options={month: month for month in seattle_temps["month"].unique()}
        ),
        html.Iframe(
            id="line_temp",
            style={"border-width": "0", "width": "100%", "height": "400px" },
            srcDoc=plot_seattle_temps(months="January")
        )
    ]
)

@app.callback(
    Output("line_temp", "srcDoc"),
    Input("months", "value")
)
def update_plot(months):
    return plot_seattle_temps(months)

if __name__ == "__main__":
    app.run_server(debug=True)