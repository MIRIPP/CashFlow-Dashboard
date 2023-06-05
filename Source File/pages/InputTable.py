from app import *
from dash import dash_table

dash.register_page(__name__)

m_button_state = True

layout = html.Div([
    dbc.Row([
        dbc.Col(id='keyword-card-income'),
        dbc.Col(id='keyword-card-spending'),
    ]),
    dbc.Row(
        [
            dbc.Col([
                html.Button('Save State', id='save-data-button', n_clicks=0),
            ]),
        ],
    ),
    dbc.Row(
        [
            html.Div([
                dash_table.DataTable(
                    id='data-table',
                    data=[],
                    columns=[
                        {"name": 'Date', "id": 'Date', "deletable": False, 'type': 'datetime', "selectable": False,
                         "hideable": True, "format": {"specifier": "%d.%m.%y"}, 'editable': False},
                        {"name": 'Bank', "id": 'Bank', "deletable": False, 'type': 'text', "selectable": False,
                         "hideable": True, 'editable': False},
                        {"name": 'Amount', "id": 'Amount', "deletable": False, 'type': 'numeric', "selectable": False,
                         "hideable": True,'editable': False,
                         "format": {
                             "specifier": "$,.2f",
                             "locale": {
                                 "symbol": ["", " €"],
                                 "group": ".",
                                 "decimal": ",",
                             },
                         }},
                        {"name": 'Purpose', "id": 'Purpose', "deletable": False, 'type': 'text', "selectable": False,
                         "hideable": True, 'editable': False},
                        {"name": 'Client', "id": 'Client', "deletable": False, 'type': 'text', "selectable": False,
                         "hideable": True},
                        {"name": 'Category', "id": 'Category', "deletable": False, 'type': 'text', "selectable": False,
                         "hideable": True},
                        {"name": 'Description', "id": 'Description', "deletable": False, 'type': 'text',
                         "selectable": False},
                    ],
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    row_deletable=True,
                    page_action="native",
                    page_current=0,
                    style_header={
                        'backgroundColor': 'rgb(30, 30, 30)',
                        'color': 'white'
                    },
                    style_cell={
                        'minWidth': '0px',
                        'whiteSpace': 'normal',
                        'maxWidth': '510px',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                    },
                    editable=True,

                ),
                html.Div(id='table-dropdown-container')
            ])
        ]
    ),
    dbc.Row(
        html.Button('Add Row', id='add-row-button', n_clicks=0)
    )

], style={"padding": "20px"}
)
