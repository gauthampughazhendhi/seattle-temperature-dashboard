import altair as alt
from dash import Dash, html, dcc, Input, Output
from vega_datasets import data

seattle_temps = data.seattle_temps()
seattle_temps["month"] = seattle_temps["date"].dt.month_name()
seattle_temps["day"] = seattle_temps["date"].dt.day

def plot_seattle_temps(month):

    plot = (
        alt.Chart(seattle_temps[seattle_temps["month"] == (month or "January")],
                  title=f"Daily average temperature of Seattle in {month or 'January'} 2010",
                  height=400,
                  width=620)
        .encode(x=alt.X("day:N",
                        title="Month day",
                        axis=alt.Axis(labelAngle=0)),
                y=alt.Y("mean(temp)",
                        scale=alt.Scale(zero=False),
                        title="Average daily temperature (F)"),
                tooltip=alt.Tooltip(["mean(temp)"],
                                    format=".1f",
                                    title="Avg. temperature in F"))
        .mark_line()
    )

    return (plot + plot.mark_circle()).to_html()

app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server

app.layout = html.Div(
    [
        dcc.Dropdown(
            id="month",
            value="January",
            options={month: month for month in seattle_temps["month"].unique()}
        ),
        html.Iframe(
            id="line_temp",
            style={"border-width": "0", "width": "720px", "height": "500px", "margin-top": "50px"},
            srcDoc=plot_seattle_temps(month="January")
        )
    ],
    style={"width": "720px", "margin": "100px auto"}
)

@app.callback(
    Output("line_temp", "srcDoc"),
    Input("month", "value")
)
def update_plot(month):
    return plot_seattle_temps(month)

if __name__ == "__main__":
    app.run_server()