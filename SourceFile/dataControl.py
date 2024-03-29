import pandas as pd
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px


def update_saving(data):
    x = data.gr_saving_by_month["Amount"].tolist()
    y_ts = data.gr_saving_by_month.index.tolist()  # y_ts = y_time_stamp
    y = [ts.strftime('%b') for ts in y_ts]

    fig = {
        'data': [
            {
                'x': y,
                'y': x,
                'type': 'bar',
                'text': [f'{val:,.2f} €' for val in x],  # Format text with desired format
                'textposition': 'outside',  # Show text outside the bars
                'insidetextanchor': 'start',  # Place text on top of the bars
                'textfont': {'size': 3 * 12},
                'marker': {'color': ['rgba(26,26,26,255)' if val < 0 else 'rgba(191,191,191,255)' for val in x],
                           'line': {'color': 'black', 'width': 1}}
            }
        ],
        'layout': {
            'margin': {'t': 30, 'b': 30, 'l': 30, 'r': 30},  # Remove graph margins
            'paper_bgcolor': 'rgba(0,0,0,0)',  # Set graph background color
            'plot_bgcolor': 'rgba(0,0,0,0)',  # Set graph background color
            "legend": {"orientation": "h", "yanchor": "top", "y": 1.0, "xanchor": "center", "x": 0.5}
        }
    }
    # Return the updated graph figure
    return fig


def update_income_spending_interactive(data, category_filtered):

    fig_data = []

    for category in category_filtered:
        category_data = data.gr_combined_by_month_and_category[data.gr_combined_by_month_and_category['Category'] == category]

        y = category_data['Amount'].tolist()
        x_ts = category_data['Month'].tolist()
        x = [ts.strftime('%b') for ts in x_ts]

        fig_data.append({
            'x': x,
            'y': y,
            'name': category,
            'type': 'bar',
            'marker': {'line': {'width': 1}},
        })

    fig = {
        'data': fig_data,
        'layout': {
            'margin': {'t': 30, 'b': 30, 'l': 30, 'r': 30},  # Remove graph margins
            'paper_bgcolor': 'rgba(0,0,0,0)',  # Set graph background color
            'plot_bgcolor': 'rgba(0,0,0,0)',  # Set graph background color
            'barmode': 'relative',
            'legend': {'orientation': 'h', 'yanchor': 'middle', 'y': 0.5, 'xanchor': 'right', 'x': 10.0}
            # Move legend to the right side
        }
    }

    return fig


def update_income_spending(data):

    # group dataframe for month
    gr_income_filtered_by_moth = data.df_income.groupby(pd.Grouper(key="Date", freq="M")).sum()
    gr_spending_filtered_by_moth = data.df_spending.groupby(pd.Grouper(key="Date", freq="M")).sum()

    y1 = gr_income_filtered_by_moth["Amount"].tolist()
    x1_ts = gr_income_filtered_by_moth.index.tolist()
    x1 = [ts.strftime('%b') for ts in x1_ts]

    y2 = gr_spending_filtered_by_moth["Amount"].tolist()
    x2_ts = gr_spending_filtered_by_moth.index.tolist()  # ts = timestamp
    x2 = [ts.strftime('%b') for ts in x2_ts]

    fig = {
        'data': [
            {
                'x': x1,
                'y': y1,
                'name': 'Income',
                'type': 'bar',
                'marker': {'color': 'rgba(26,26,26,255)',
                           'line': {'color': 'black', 'width': 1}}
            },
            {
                'x': x2,
                'y': y2,
                'name': 'Spending',
                'type': 'bar',
                'marker': {'color': 'rgba(191,191,191,255)',
                           'line': {'color': 'black', 'width': 1}}
            }
        ],
        'layout': {
            'margin': {'t': 30, 'b': 30, 'l': 30, 'r': 30},  # Remove graph margins
            'paper_bgcolor': 'rgba(0,0,0,0)',  # Set graph background color
            'plot_bgcolor': 'rgba(0,0,0,0)',  # Set graph background color
            'barmode': 'relative',
            "legend": {"orientation": "h", "yanchor": "top", "y": 1.05, "xanchor": "center", "x": 0.5}
        }
    }
    # Return the updated graph figure
    return fig


def update_spending_category(data, month):
    y1 = data.gr_spending_by_categories_average["Amount"].tolist()
    x1 = data.gr_spending_by_categories_average.index.tolist()

    y2 = data.gr_spending_by_categories_month_list[month]["Amount"].tolist()
    x2 = data.gr_spending_by_categories_month_list[month].index.tolist()

    fig = {
        'data': [
            {
                'x': y1,
                'y': x1,
                'orientation': 'h',
                'name': 'Avarrage',
                'type': 'bar',
                'marker': dict(color='rgba(191,191,191,255)'),
            },
            {
                'x': y2,
                'y': x2,
                'text': [f'{value:,.2f} €' for value in y2],  # Add the values of y2 as text
                'textposition': 'outside',  # Set text position to be outside the bars
                'orientation': 'h',
                'name': 'selected Month',
                'type': 'bar',
                'marker': dict(color='rgba(26,26,26,255)'),
            }
        ],
        'layout': {
            'margin': {'t': 30, 'b': 30, 'l': 100, 'r': 30},  # Remove graph margins
            'paper_bgcolor': 'rgba(0,0,0,0)',  # Set graph background color
            'plot_bgcolor': 'rgba(0,0,0,0)',  # Set graph background color
            'barmode': 'group',
            "legend": {"orientation": "h", "yanchor": "top", "y": 1.0, "xanchor": "center", "x": 0.5}
        }
    }
    # Return the updated graph figure
    return fig


def update_bank_balance(data):
    line_traces = []
    for balance_data, bank_name in zip(data.list_df_bank_balance, data.list_bank_names):
        trace = {'x': balance_data['Date'], 'y': balance_data['cum_sum'], 'type': 'line', 'name': bank_name}
        line_traces.append(trace)

    fig = {

        'data': line_traces,
        'layout': {
            'margin': {'t': 10, 'b': 30, 'l': 30, 'r': 30},  # Remove graph margins
            'paper_bgcolor': 'rgba(0,0,0,0)',  # Set graph background color
            'plot_bgcolor': 'rgba(0,0,0,0)',  # Set graph background color
            "legend": {"orientation": "h", "yanchor": "top", "y": 1.05, "xanchor": "center", "x": 0.5}
        }
    }
    # Return the updated graph figure
    return fig


def update_pie_spending(data):
    x = data.gr_spending_by_categories_average["Amount"].tolist()
    y = data.gr_spending_by_categories_average.index.tolist()

    fig = {
        'data': [
            {
                'labels': y,
                'values': x,
                'type': 'pie',
                'textinfo': 'none',
                'hoverinfo': 'text',
                'text': [f"{label}: {value:.2f} €" for label, value in zip(y, x)],
                #'showlegend': False,
                # 'marker': {
                #     'colors': ['#808080','#696969','#A9A9A9','#7B7B7B','#C0C0C0','#555555','#999999','#4C4C4C',
                #                '#D3D3D3','#888888','#B0B0B0','#333333', '#767676', '#EAEAEA','#666666']
                # }
            }
        ],
        'layout': {
           'margin': {'t': 30, 'b': 30, 'l': 30, 'r': 30},  # Remove graph margins
            'paper_bgcolor': 'rgba(0,0,0,0)',  # Set graph background color
            'plot_bgcolor': 'rgba(0,0,0,0)',  # Set graph background color
            'legend': {
                'orientation': 'h',
                'x': -0.2,  # Position the legend outside the pie chart
                'y': 0.5,
                'xanchor': 'center',
            }
        }
    }

    return fig


def update_pie_income(data):
    x = data.gr_income_by_categories_ges["Amount"].tolist()
    y = data.gr_income_by_categories_ges.index.tolist()

    fig = {
        'data': [
            {
                'labels': y,
                'values': x,
                'type': 'pie',
                'textinfo': 'none',
                'hoverinfo': 'text',
                'text': [f"{label}: {value:.2f} €" for label, value in zip(y, x)],
                #'showlegend': False,
                # 'marker': {
                #     'colors': ['#808080','#696969','#A9A9A9','#7B7B7B','#C0C0C0','#555555','#999999','#4C4C4C',
                #                '#D3D3D3','#888888','#B0B0B0','#333333', '#767676', '#EAEAEA','#666666']
                # }
            }
        ],
        'layout': {
           'margin': {'t': 30, 'b': 30, 'l': 30, 'r': 30},  # Remove graph margins
            'paper_bgcolor': 'rgba(0,0,0,0)',  # Set graph background color
            'plot_bgcolor': 'rgba(0,0,0,0)',  # Set graph background color
            'legend': {
                'orientation': 'h',
                'x': -0.2,  # Position the legend outside the pie chart
                'y': 0.5,
                'xanchor': 'center',
            }
        }
    }
    return fig


def make_overview_card(title, start, end):
    value = end - start
    if value < 0:
        str_class_name = "bi bi-caret-down-fill text-danger"
    else:
        str_class_name = "bi bi-caret-up-fill text-success"

    return dbc.Card(
        dbc.CardBody(
             [
                html.H4([html.I(className="bi bi-bank me-2"), title], className="text-nowrap"),
                html.H6(f"{int(start)} €", style={'color': 'white'}),
                html.Div(
                    [
                        html.I(f"{int(value)} €", className=str_class_name)
                    ]
                ),
                html.Hr(style={'margin-top': '5px', 'margin-bottom': '5px'}),
                html.H6(f"{int(end)} €", style={'color': 'white', 'font-weight': 'bold'}),
             ],
         ),
        style={'background-color': 'rgba(2,50,51,1)', 'border-color': 'white'},
        inverse=True,
        className="text-center m-2",
    )


def make_overview_category_card(data):
    return [
        html.Div(f"{category} - {total:.2f}€ - {average:.2f}€", className="card-text")
        for category, total, average in zip(data.categories, data.gr_spending_by_categories_ges["Amount"],
                                            data.gr_spending_by_categories_average["Amount"])
        ]



def make_keyword_card(title, keywords):
    list_string = ', '.join(keywords)
    return dbc.Card(
        dbc.CardBody(
            [
                html.H6(title, className="text-nowrap"),
                html.P(list_string),
            ],
        ),
        className="text-center m-0",
    )
