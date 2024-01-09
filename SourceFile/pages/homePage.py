from app import *

dash.register_page(__name__, path='/')

card_spendingByCategory = dbc.Card(
    [
        dbc.CardBody([
            html.H4("Spending by Category", style={'color': 'black', 'font-weight': 'bold'}),
            dbc.Row([
                dbc.Col([
                    # html.H6("Month", className="card-subtitle"),
                    dcc.RadioItems(
                        id="month-select",
                        options=[
                            {'label': 'Jan', 'value': 0},
                            {'label': 'Feb', 'value': 1},
                            {'label': 'Mar', 'value': 2},
                            {'label': 'Apr', 'value': 3},
                            {'label': 'May', 'value': 4},
                            {'label': 'Jun', 'value': 5},
                            {'label': 'Jul', 'value': 6},
                            {'label': 'Aug', 'value': 7},
                            {'label': 'Sep', 'value': 8},
                            {'label': 'Oct', 'value': 9},
                            {'label': 'Nov', 'value': 10},
                            {'label': 'Dec', 'value': 11},
                        ],
                        value=0,
                        labelStyle={'display': 'inline-block'},
                        inputStyle={'margin-right': '1px', 'margin-left': '10px'}
                    )
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='graph-spending-category'),
                ]),
            ]),
        ]),
    ],
    style={
        'background-color': 'rgba(237,237,237,1)',
        'border-color': 'rgba(2,50,51,1)'
    },
    # Alternative style:
    # className="shadow"
    # color="light",  # https://bootswatch.com/default/ for more card colors,
)

card_incomeSpending = dbc.Card(
    [
        dbc.CardBody([
            html.H4("Income / Spending", style={'color': 'black', 'font-weight': 'bold'}),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='graph-income-spending')
                ]),
            ])
        ]),
    ],
    style={
        'background-color': 'rgba(237,237,237,1)',
        'border-color': 'rgba(2,50,51,1)'
    },
    # Alternative style:
    # className="shadow"
    # color="light",  # https://bootswatch.com/default/ for more card colors,
)

card_saving = dbc.Card(
    [
        dbc.CardBody([
            html.H4("Savings", style={'color': 'black', 'font-weight': 'bold'}),
            dcc.Graph(id='graph-saving'),
            html.H6("."),
        ]
        ),
    ],
    style={
        'background-color': 'rgba(237,237,237,1)',
        'border-color': 'rgba(2,50,51,1)'
    },
    # Alternative style:
    # className="shadow"
    # color="light",  # https://bootswatch.com/default/ for more card colors,
)

card_bankBalance = dbc.Card(
    [
        dbc.CardBody([
            html.H4("Bank balance", style={'color': 'black', 'font-weight': 'bold'}),
            dcc.Graph(id='graph-bank-balance')
        ]),
    ],
    style={
        'background-color': 'rgba(237,237,237,1)',
        'border-color': 'rgba(2,50,51,1)'
    },
    # Alternative style:
    # className="shadow"
    # color="light",  # https://bootswatch.com/default/ for more card colors,
)

card_pie_chart_spending = dbc.Card(
    [
        dbc.CardBody([
            html.H4("Spending", style={'color': 'black', 'font-weight': 'bold'}),
            dcc.Graph(id='graph-pie-spending'),
        ]
        ),
    ],
    style={
        'background-color': 'rgba(237,237,237,1)',
        'border-color': 'rgba(2,50,51,1)'
    },
    # Alternative style:
    # className="shadow"
    # color="light",  # https://bootswatch.com/default/ for more card colors,
)

card_pie_chart_income = dbc.Card(
    [
        dbc.CardBody([
            html.H4("Income", style={'color': 'black', 'font-weight': 'bold'}),
            dcc.Graph(id='graph-pie-income')
        ]),
    ],
    style={
        'background-color': 'rgba(237,237,237,1)',
        'border-color': 'rgba(2,50,51,1)'
    },
    # Alternative style:
    # className="shadow"
    # color="light",  # https://bootswatch.com/default/ for more card colors,
)

card_overview_category = dbc.Card(
    [
        html.H4("Spending Overview", style={'color': 'black', 'font-weight': 'bold'}),
        html.Div(id='card-overview-category'),
    ],
    style={
        'background-color': 'rgba(237,237,237,1)',
        'border-color': 'rgba(2,50,51,1)'
    },
    # Alternative style:
    # className="shadow"
    # color="light",  # https://bootswatch.com/default/ for more card colors,
)

layout = html.Div([
    # dbc.Row(id='card-row', className="my-2"),
    dbc.Row(
        [
            dbc.Col(card_spendingByCategory, width=7),
            dbc.Col(card_overview_category, width=5),
        ],
        style={"margin-bottom": "20px"},  # distance to next cards
    ),
    dbc.Row(
        [
            dbc.Col(card_incomeSpending, width=8),
            dbc.Col(card_saving, width=4),
            # dbc.Col(card_pie_chart_income, width=3),

        ],
        style={"margin-bottom": "20px"},  # distance to next cards
    ),
    dbc.Row(
        [
            dbc.Col(card_bankBalance, width=6),
            dbc.Col(card_pie_chart_spending, width=6),
        ]
    ),
    dbc.Row(
        [
            dbc.Col(card_pie_chart_income, width=3),
        ]
    ),
], style={"padding": "20px"}
)
