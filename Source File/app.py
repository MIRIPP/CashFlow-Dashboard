import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

from datetime import datetime as dt
import datetime



# importen websites for Gui:
# cheat sheet: https://dashcheatsheet.pythonanywhere.com/
# doku dash_bootstrap_components: https://dash-bootstrap-components.opensource.faculty.ai/docs/components/card/
# https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/explorer/
# doku dash: https://dash.plotly.com/dash-core-components/graph
# tutorail code: https://github.com/Coding-with-Adam/Dash-by-Plotly/blob/master/Bootstrap/bootstrap_card.py
# tutorial video: https://www.youtube.com/watch?v=THB9AEwdSXo&list=PLh3I780jNsiS3xlk-eLU2dpW3U-wCq4LW&index=11
# tutorial examples: https://dash-example-index.herokuapp.com/

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
                use_pages=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

app.title = "Budget Dashboard"  # do I need?

app.config.suppress_callback_exceptions = True  # do I need?

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.H4("Budget Dashboard", className='text-left text-white my-3'),
            width=4),
        dbc.Col(
            dbc.Nav([
                dbc.NavLink("Homepage", href="/",  className='text-centre text-white'),
                dbc.NavLink("Importtable", href="/importerpage",  className='text-centre text-white'),
                dbc.NavLink("InputTable", href="/inputtable", className='text-centre text-white'),
            ],             horizontal=True,
                className='d-flex justify-content-center my-3'),
            width=4),
        dbc.Col(
            dcc.Dropdown(
                id="year-select",
                options=[{"label": i, "value": i} for i in
                         range(datetime.date.today().year - 10, datetime.date.today().year + 1)],
                value=datetime.date.today().year, className='text-left my-3',
            ),
            width={'size':2, 'offset':2})
    ],
        className="bg-primary"
    ),

    dbc.Row(
        dash.page_container
    ),
], fluid=True)




@callback(
    Output("date-picker-select", "start_date"),
    [
        Input("year-select", "value"),
    ],
)
def update_start_date(value):
    if value is not None:
        return dt(value, 1, 1)


# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
