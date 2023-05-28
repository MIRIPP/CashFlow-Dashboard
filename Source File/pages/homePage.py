import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

from control import *

import plotly.express as px

df = px.data.gapminder()

dash.register_page(__name__, path='/')

controller = Controller()

data = {
    'Category': ['A', 'B', 'C', 'D'],
    'Positive': [10, 15, 7, 12],
    'Negative': [-5, -10, -3, -8]
}

data2 = {
    'Category': ['A', 'B', 'C', 'D', 'e', 'f', 'g', 'h', 'i', 'j', 'l', 'm'],
    'Value': [10, -15, 7, -12, 10, -15, 7, -12, 10, -15, 7, -12]
}

data3 = {
    'Category': ['A', 'B', 'C', 'D'],
    'Line1': [10, -15, 7, -12],
    'Line2': [-5, 8, -11, 6],
    'Line3': [12, 9, -4, -7],
    'Line4': [-8, -3, 6, 11]
}
summary = {"Sales": "$100K", "Profit": "$5K", "Orders": "6K", "Customers": "300", "Sales1": "$100K", "Profit1": "$5K",
           "Orders1": "6K", "Customers1": "300"}

card_spendingByCategory = dbc.Card(
    [
        dbc.CardHeader(html.H4("Spending by Category", className="card-title")),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.H6("Select Month", className="card-subtitle"),
                    dcc.RadioItems(
                        options=[
                            {'label': 'Jan.  ', 'value': 'January'},
                            {'label': 'Feb.  ', 'value': 'February'},
                            {'label': 'Mar.  ', 'value': 'March'},
                            {'label': 'Apr.  ', 'value': 'April'},
                            {'label': 'May', 'value': 'May'},
                            {'label': 'Jun', 'value': 'June'},
                            {'label': 'Jul', 'value': 'July'},
                            {'label': 'Aug', 'value': 'August'},
                            {'label': 'Sep', 'value': 'September'},
                            {'label': 'Ocz', 'value': 'October'},
                            {'label': 'Nov', 'value': 'November'},
                            {'label': 'Dec', 'value': 'December'},
                        ],
                        inline=True,
                        style={"width": "50px"},
                        # className="pe-3 border border-dark border-1"
                        # df.columns, df.columns[0:2].values
                        # (df.nation.unique(), df.nation.unique()[0:2])
                    ),
                ], width=2, className="pe-1 border-end border-dark border-1"),

                dbc.Col([
                    dcc.Graph(id="spending_category_graph",
                              figure=controller.get_fig_spending_by_categories()),
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
                    dcc.Graph(
                        figure={
                            'data': [
                                {
                                    'x': data['Category'],  # Use 'Category' for x-axis
                                    'y': data['Positive'],  # Use 'Positive' for y-axis
                                    'name': 'Positive',
                                    'type': 'bar'
                                },
                                {
                                    'x': data['Category'],  # Use 'Category' for x-axis
                                    'y': data['Negative'],  # Use 'Negative' for y-axis
                                    'name': 'Negative',
                                    'type': 'bar'
                                }
                            ],
                            'layout': {
                                'margin': {'t': 0, 'b': 0, 'l': 0, 'r': 0},  # Remove graph margins
                                'paper_bgcolor': 'rgba(0,0,0,0)',  # Set graph background color
                                'plot_bgcolor': 'rgba(0,0,0,0)',  # Set graph background color
                                'barmode': 'relative',
                                'template': "simple_white"
                                # Set barmode to 'relative' for independent positive and negative bars
                            }
                        }
                    )
                ]),
                dbc.Col([
                    html.P("Select Category Spending", className="card-subtitle"),
                    dcc.Dropdown(
                        id="select_category_spending",
                        options=[{"label": i, "value": i} for i in controller.keywords_spending],
                        value=list(controller.keywords_spending.keys()),
                        multi=True,
                    ),
                    html.Br(),
                    html.P("Select Category Income", className="card-subtitle"),
                    dcc.Dropdown(
                        id="select_category_income",
                        options=[{"label": i, "value": i} for i in controller.keyowrds_income],
                        value=list(controller.keyowrds_income.keys()),
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
            dcc.Graph(
                figure={
                    'data': [
                        {
                            'x': data2['Category'],
                            'y': data2['Value'],
                            'text': [f"{category}:\n {value}" for category, value in
                                     zip(data2['Category'], data2['Value'])],  # Display category and value on each bar
                            'textposition': 'auto',  # Show text on bars
                            'type': 'bar',
                            'marker': {'color': ['red' if val < 0 else 'green' for val in data2['Value']],
                                       'line': {'color': 'black', 'width': 1}}
                            # Customize bar colors and outline
                        }
                    ],
                    'layout': {
                        'margin': {'t': 0, 'b': 0, 'l': 0, 'r': 0},  # Remove graph margins
                        'paper_bgcolor': 'rgba(0,0,0,0)',  # Set graph background color
                        'plot_bgcolor': 'rgba(0,0,0,0)',  # Set graph background color
                        'template': "simple_white"
                    }
                },
                # style={'width': '100%'}  # Set graph height to fill the card
            )
        ]
        ),
    ], color="light",
    # style={'width': '50%', 'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
    className="shadow"
)

fig = go.Figure()

for line_name in ['Line1', 'Line2', 'Line3', 'Line4']:
    fig.add_trace(go.Scatter(
        x=data3['Category'],
        y=data3[line_name],
        mode='lines',
        name=line_name,
        hovertemplate='Category: %{x}<br>Value: %{y}',
        line=dict(color='green', width=2),
        marker=dict(
            size=8,
            color=['orange' if val >= 0 else 'red' for val in data3[line_name]],
            line=dict(width=2, color='black')
        ),
        showlegend=True
    ))

fig.update_layout(
    # margin=dict(t=50, b=50, l=50, r=50),
    legend=dict(orientation='h', yanchor='bottom', y=1.02),
    margin=dict(t=0, b=0, l=0, r=0),  # Remove graph margins
    # plot_bgcolor='white',  # Set graph background color
    template="simple_white",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

card_bankBalance = dbc.Card(
    [
        dbc.CardHeader(html.H4("Bank balance", className="card-title")),
        dbc.CardBody([
            dcc.Graph(
                id='line-graph',
                figure=fig,
            )
        ]),
    ], color="light",
    className="shadow"
)


def make_card(title, amount):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H4([html.I(className="bi bi-bank me-2"), title], className="text-nowrap"),
                html.H6(amount, ),
                html.Div(
                    [
                        html.I("12.3%", className="bi bi-caret-down-fill text-danger"),
                        " vs LY",
                    ]
                ),
            ], className="border-start border-danger border-5"
        ),
        className="text-center m-2",
    )


layout = html.Div([
    dbc.Row([dbc.Col(make_card(k, v)) for k, v in summary.items()], className="my-4"),
    dbc.Row(
        [
            dbc.Col(card_spendingByCategory, width=7),
            dbc.Col(card_saving, width=5),
        ],
        style={"margin-bottom": "20px"},
        align="stretch"  # Make cards stretch vertically to have the same height
    ),
    dbc.Row(
        [
            dbc.Col(card_bankBalance, width=5),
            dbc.Col(card_incomeSpending, width=7),
        ]
    )

    # dbc.CardColumns([  # Cards organised into Masonry-like columns
    #     card_bankBalance,
    #     dbc.CardGroup([card_spendingSaving, card_categorySelection]),
    #     card_saving,
    #     dbc.CardGroup([card_spendingMonth, card_monthSelection]),
    #
    # ])
], style={"padding": "20px"}
)
