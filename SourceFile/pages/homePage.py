from app import *

dash.register_page(__name__, path='/')

card_spendingByCategory = dbc.Card(
    [
        dbc.CardHeader(html.H4("Spending by Category", className="card-title")),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.H6("Month", className="card-subtitle"),
                    dcc.RadioItems(
                        id="month-select",
                        options=[
                            {'label': 'Jan.  ', 'value': 0},
                            {'label': 'Feb.  ', 'value': 1},
                            {'label': 'Mar.  ', 'value': 2},
                            {'label': 'Apr.  ', 'value': 3},
                            {'label': 'May', 'value': 4},
                            {'label': 'Jun', 'value': 5},
                            {'label': 'Jul', 'value': 6},
                            {'label': 'Aug', 'value': 7},
                            {'label': 'Sep', 'value': 8},
                            {'label': 'Ocz', 'value': 9},
                            {'label': 'Nov', 'value': 10},
                            {'label': 'Dec', 'value': 11},
                        ],
                        inline=True,
                        value=0,
                        style={"width": "50px"},
                    )
                ], width=1, className="pe-1 border-end border-dark border-1"),

                dbc.Col([
                    dcc.Graph(id='graph-spending-category'),
                ]),
            ]),
        ]),
    ],
    color="light",  # https://bootswatch.com/default/ for more card colors
    className="shadow"
)

card_incomeSpending = dbc.Card(
    [
        dbc.CardHeader(html.H4("Income / Spending", className="card-title")),
        dbc.CardBody(
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='graph-income-spending')
                ]),
                dbc.Col([
                    html.P("Select Category Spending", className="card-subtitle"),
                    dcc.Dropdown(
                        id="select-category-spending",
                        options=[{"label": i, "value": i} for i in keywords_spending],
                        value=list(keywords_spending.keys()),
                        multi=True,
                    ),
                    html.Br(),
                    html.P("Select Category Income", className="card-subtitle"),
                    dcc.Dropdown(
                        id="select-category-income",
                        options=[{"label": i, "value": i} for i in keywords_income],
                        value=list(keywords_income.keys()),
                        multi=True,
                    ),
                ],
                    width=5)
            ])
        ),
    ],
    color="light",  # https://bootswatch.com/default/ for more card colors
    className="shadow"
)

card_saving = dbc.Card(
    [
        dbc.CardHeader(html.H4("Savings", className="card-title")),
        dbc.CardBody([
            dcc.Graph(id='graph-saving')
        ]
        ),
    ], color="light",
    className="shadow"
)

card_bankBalance = dbc.Card(
    [
        dbc.CardHeader(html.H4("Bank balance", className="card-title")),
        dbc.CardBody([
            dcc.Graph(id='graph-bank-balance')
        ]),
    ], color="light",
    className="shadow"
)

card_pie_chart_spending = dbc.Card(
    [
        dbc.CardHeader(html.H4("Spending", className="card-title")),
        dbc.CardBody([
            dcc.Graph(id='graph-pie-spending')
        ]
        ),
    ], color="light",
    className="shadow"
)

card_pie_chart_income = dbc.Card(
    [
        dbc.CardHeader(html.H4("Income", className="card-title")),
        dbc.CardBody([
            dcc.Graph(id='graph-pie-income')
        ]),
    ], color="light",
    className="shadow"
)

layout = html.Div([
    dbc.Row(id='card-row', className="my-2"),
    dbc.Row(
        [
            dbc.Col(card_spendingByCategory, width=7),
            dbc.Col(card_saving, width=5),
        ],
        style={"margin-bottom": "20px"},  # distance to next cards
    ),
    dbc.Row(
        [
            dbc.Col(card_bankBalance, width=5),
            dbc.Col(card_incomeSpending, width=7),
        ],
        style={"margin-bottom": "20px"},  # distance to next cards
    ),
    dbc.Row(
        [
            dbc.Col(card_pie_chart_income, width=5),
            dbc.Col(card_pie_chart_spending, width=7),
        ]
    )
], style={"padding": "20px"}
)
