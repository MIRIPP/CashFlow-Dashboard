import dash
from dash import dcc, html
from dash import html, dcc, callback, Output, Input, State
from dash.exceptions import PreventUpdate
import pandas as pd
import pathlib

import datetime
import json
import time

dash.register_page(__name__)

# layout = html.Div(
#     [
#         dcc.Markdown('# This will be the content of Page 3')
#     ]
# )

def category_input_lines():
    lines = []
    for i in range(1, 10):
        line = html.Div(
            id="accounts-overview",
            children=[ dcc.Input(id='input_category-{}'.format(i), type='text'),
                       dcc.Input(id='input_keywords-{}'.format(i), type='text'),
                       ])

        lines.append(line)
    # lines.append(html.Button(id='submit-button', n_clicks=0, children='Submit'))
    # lines.append(dcc.Store(id='data'))
    return lines


layout = html.Div(
    id="inporter",
    children=[
        html.Div(
            id="category_import",
            children=category_input_lines(),
            style={
                "width": "80%",  # feste breite
                "float": "left",
                "padding": "20px 20px 20px 20px",  # rand um den text (innerer Rand)
                "margin": "20px 20px 20px 20px",  # abstand zur nächsten box (äuserer Rand)
                "border-radius": "20px",  # radius grenzen, abrundung
                "background-color": "#e9a8538e",  # farben
            }
        ),
        dcc.Store(id='data'),
        html.Button(id='submit-button', n_clicks=0, children='Submit')
    ])

@callback(
    Output('store', 'data'),
    Input('submit-button', 'n_clicks'),
    [State('input_category-{}'.format(i), 'value') for i in range(1, 11)],
    [State('input_keywords-{}'.format(i), 'value') for i in range(1, 11)])
def clicks(*args):

    df = pd.DataFrame()
    for i in range(1, 11):
        df = df.append({"Category": args[i], "Keywords": args[i + 10]}, ignore_index=True)

    path = pathlib.Path(__file__).parent.joinpath("../data/settings").resolve()
    df.to_csv(path.joinpath("categorys.csv"), encoding="utf-8-sig", index=False)

    return df.to_json(date_format='iso', orient='split')
