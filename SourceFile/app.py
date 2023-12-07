import dash
from dash import html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
import json
import os
import pandas as pd

import dataImporter as dI
import dataControl as dC

# Important websites for Gui:
# dash cheat sheet: https://dashcheatsheet.pythonanywhere.com/
# doku dash_bootstrap_components:    https://dash-bootstrap-components.opensource.faculty.ai/docs/components/card/
#                                   https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/explorer/
# doku dash: https://dash.plotly.com/dash-core-components/graph
# tutorial code: https://github.com/Coding-with-Adam/Dash-by-Plotly/blob/master/Bootstrap/bootstrap_card.py
# tutorial video: https://www.youtube.com/watch?v=THB9AEwdSXo&list=PLh3I780jNsiS3xlk-eLU2dpW3U-wCq4LW&index=11
# tutorial examples: https://dash-example-index.herokuapp.com/

# Todo:
# make code bulled proved
# auto generated user_settings file
# add more charts
# train AI to find the categories on a better level


# 0. Create data structure
directory = 'data_example'
directories = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]
dict_year_df = {}
keywords_income = {}
keywords_spending = {}

# 1. create Dash App
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],  # using BOOTSTRAP layout
                use_pages=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

# 2. Import source data
for year in directories:
    if year.isdigit():
        data = {}
        with open(directory + '/' + year + '/user_settings.json') as file:
            json_data = json.load(file)

        banks = json_data['banks']
        keywords_income = json_data['keywords_income']
        keywords_spending = json_data['keywords_spending']

        dict_year_df[year] = dI.DataImporter(directory, year, banks, keywords_income, keywords_spending)

list_years = list(dict_year_df.keys())

# app.config.suppress_callback_exceptions = True

# 3. Create Statusbar
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Row(
                html.H4("Budget Dashboard", className='text-left text-white my-3'),
            ),
            dbc.Row(
                    dbc.NavLink("Homepage", href="/", className='text-center text-white my-1 mx-auto'),
            ),
            dbc.Row(
                    dbc.NavLink("InputTable", href="/inputtable", className='text-center text-white my-1 mx-auto'),
            ),
            dbc.Row(
                dcc.Dropdown(
                    id="year-select",
                    options=list_years,
                    value=list_years[-1],
                    className='text-left my-3',

                ),
            ),
            dbc.Row(id='card-row', className="my-2")
        ],
        width=2,
        style={'background-color': 'rgba(2,50,51,255)'}
        ),
        dbc.Col(dash.page_container, width=10, style={'background-color': 'rgba(237,237,237,255)'}),
    ],
    # className="bg-primary"
    ),
], fluid=True)


# 4. Callback Homepage when year changed
@app.callback(
    [Output('graph-saving', 'figure'),
     Output('graph-bank-balance', 'figure'),
     Output('graph-pie-spending', 'figure'),
     Output('graph-pie-income', 'figure')],
    Input('year-select', 'value'),
)
def update_graph(selected_year):
    df_data = dict_year_df[selected_year]
    return dC.update_saving(df_data), dC.update_bank_balance(df_data), dC.update_pie_spending(df_data), dC.update_pie_income(df_data)


@app.callback(
    Output('graph-spending-category', 'figure'),
    [Input('month-select', 'value'),
     Input('year-select', 'value')],
)
def update_graph(month, year_selected):
    df_data = dict_year_df[year_selected]
    return dC.update_spending_category(df_data, month)


@app.callback(
    Output('graph-income-spending', 'figure'),
    [Input('select-category-income', 'value'),
     Input('select-category-spending', 'value'),
     Input('year-select', 'value')],
)
def update_graph(category_income, category_spending, year_selected):
    df_data = dict_year_df[year_selected]
    return dC.update_income_spending(df_data, category_income, category_spending)


@app.callback(
    Output('card-row', 'children'),
    Input('year-select', 'value'),
)
def update_card(selected_year):
    df_data = dict_year_df[selected_year]
    cards = []
    for name, start_money in df_data.start_money.items():
        cards.append(dbc.Row(dC.make_overview_card(name, start_money, df_data.end_money[name])))
    return cards


# 5. Callback Input table
@app.callback(
    [Output('data-table', 'data'),
     Output('add-row-button', 'n_clicks')],
    [Input('year-select', 'value'),
     Input('add-row-button', 'n_clicks')],
    [State('data-table', 'data')],
    prevent_initial_call=True  # Set this attribute to True
)
def update_table(year_selected, n_clicks, table_data):
    df_data = dict_year_df[year_selected].df
    # Convert the "Date" column to a formatted string
    df_data['Date'] = pd.to_datetime(df_data['Date'], format='%d.%m.%y').dt.strftime('%d.%m.%y')
    if n_clicks > 0:
        new_row = {'Date': ' ',
                   'Bank': ' ',
                   'Amount': 0,
                   'Purpose': 'aaa',
                   'Client': 'aaa',
                   'Category': 'aaa',
                   'Description': 'aaa'}
        table_data.append(new_row)
        return table_data, 0
    else:
        return df_data.to_dict('records'), 0


@app.callback(
    [Output('year-select', 'value'),
     Output('save-data-button', 'n_clicks')],
    [Input('save-data-button', 'n_clicks')],
    [State('data-table', 'data'),
     State('year-select', 'value')],
    prevent_initial_call=True  # Set this attribute to True
)
def save_modifyed_data(n_clicks, table_data, year_selected):
    if n_clicks > 0:
        if table_data is not None:
            new_df = pd.DataFrame(table_data)
            # new_df_opt = pd.DataFrame(data, columns=[c['name'] for c in columns])
            new_df["Date"] = pd.to_datetime(new_df["Date"], format='%d.%m.%y', dayfirst=True)

            dict_year_df[year_selected].create_all_dataframe(new_df)
            new_df.to_csv(dict_year_df[year_selected].data_path_source_file, encoding="utf-8-sig", index=False)

    return year_selected, 0


@app.callback(
    [Output('keyword-card-income', 'children'),
     Output('keyword-card-spending', 'children')],
    Input('year-select', 'value'),
)
def update_card(selected_year):
    df_data = dict_year_df[selected_year]
    return dC.make_keyword_card("Keyword Income:", list(df_data.keywords_income.keys())), dC.make_keyword_card(
        "Keyword Spending:", list(df_data.keywords_spending.keys()))


# 5. Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
