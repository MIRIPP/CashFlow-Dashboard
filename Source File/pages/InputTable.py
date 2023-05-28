import dash
from dash import dcc, html, Input, Output, State, callback
import plotly.express as px
import dash_table
import pandas as pd
from collections import OrderedDict
from control import Controller

dash.register_page(__name__)

controller = Controller()
df = controller.df

df['Date'] = df['Date'].dt.date
m_button_state = True

layout = html.Div([
    html.Button(id='save-data-button', n_clicks=0),
    html.Button('Add Row', id='editing-rows-button', n_clicks=0),
    dash_table.DataTable(
        id='data-table',
        data=df.to_dict('records'),
        columns=[
            {"name": 'Date', "id": 'Date', "deletable": False, 'type': 'datetime', "selectable": False, "hideable": True},
            {"name": 'Bank', "id": 'Bank', "deletable": False, 'type': 'text', "selectable": False, "hideable": True},
            {"name": 'Amount', "id": 'Amount', "deletable": False, 'type': 'numeric', "selectable": False,
             "hideable": True,
             "format": {
                 "specifier": "$,.2f",
                 "locale": {
                     "symbol": ["", " €"],
                     "group": ".",
                     "decimal": ",",
                 },
             },},
            {"name": 'Purpose', "id": 'Purpose', "deletable": False, 'type': 'text', "selectable": False, "hideable": True},
            {"name": 'Client', "id": 'Client', "deletable": False, 'type': 'text', "selectable": False, "hideable": True},
            {"name": 'Category', "id": 'Category', "deletable": False, 'type': 'text', "selectable": False, "hideable": True, 'presentation': 'dropdown'},
            {"name": 'Description', "id": 'Description', "deletable": False, 'type': 'text', "selectable": False, "hideable": True},
        ],
        filter_action="native",  # allow filtering of data by user ('native') or not ('none')
        sort_action="native",  # enables data to be sorted per-column by user or not ('none')
        sort_mode="multi",  # sort across 'multi' or 'single' columns
        row_deletable=True,  # choose if user can delete a row (True) or not (False)
        page_action="native",  # all data is passed to the table up-front or not ('none')
        page_current=0,  # page number that user is on
        editable=True,
        style_header={
            'backgroundColor': 'rgb(30, 30, 30)',
            'color': 'white'
        },
        # style_data={
        #     'backgroundColor': 'rgb(50, 50, 50)',
        #     'color': 'white'
        # },
        style_cell={
            # all three widths are needed
            'minWidth': '10px', 'width': '210px', 'maxWidth': '210px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        },
        # style_cell_conditional=[
        #     {'if': {'column_id': 'Date'},
        #      'width': '10%'},
        #     {'if': {'column_id': 'Bank'},
        #      'width': '10%'},
        # ],
        dropdown={
            'Category': {
                'options': [
                    {'label': i, 'value': i}
                    for i in df['Category'].unique()
                ]
            },
        }
    ),
    html.Div(id='table-dropdown-container'),
    ]
)

@callback(
    Output('data-table', 'data'),
    Input('editing-rows-button', 'n_clicks'),
    State('data-table', 'data'),
    State('data-table', 'columns'))
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows

@callback(
    Output('save-data-button', 'children'),
    Input('save-data-button', 'n_clicks'),
    State('data-table', 'data'),
 )
def save_modifyed_data(n_clicks, data):
    if n_clicks == 0:
        return "Save Changes"
    bool_disabled = n_clicks % 2
    df_table = df if data is None else pd.DataFrame(data)
    df_table.to_csv(controller.data_path.joinpath("source_file_edit" + ".csv"),
                    encoding="utf-8-sig", index=False)
    if bool_disabled:
        return "Saved! Press to Save Changes"
    else:
        return "Save Changes"
    # if n_clicks > 0:
    #     if m_button_state is False:
    #         m_button_state = True
    #         # df_table = df if data is None else pd.DataFrame(data)
    #         # df_table.to_csv(PATH.joinpath("data/" + "2020").resolve().joinpath("source_file_edit.csv"),
    #         #                 encoding="utf-8-sig", index=False)
    #         return ["Data Saved. Press for Reset Data"]
    #     else:
    #         return ["Save Data"]

