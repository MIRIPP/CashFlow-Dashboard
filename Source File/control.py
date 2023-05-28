# -*- coding: utf-8 -*-
import dash
import plotly.express as px
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import os
import numpy as np
from data_filtering import *


class Controller(SourceData):
    def __init__(self):
        super().__init__()

        """
        creating all kind of different graphs
        """

    def get_fig_spending_by_categories(self):
        self.fig_spending_by_categories = go.Figure()
        self.fig_spending_by_categories.add_trace(
            go.Bar(y=self.gr_spending_by_categories_monthlist[0].index.values.tolist(),
                   x=self.gr_spending_by_categories_monthlist[0]["Amount"].tolist(),
                   name="Avarage Spending",
                   orientation='h',
                   marker=dict(
                       color='rgba(360, 74, 48, 0.6)',
                   )
                   ))
        self.fig_spending_by_categories.add_trace(
            go.Bar(name="January Spending",
                   y=self.gr_spending_by_categories_average.index.values.tolist(),
                   x=self.gr_spending_by_categories_average["Amount"].tolist(),
                   orientation='h',
                   marker=dict(
                       color='red',
                   )
                   ))
        self.fig_spending_by_categories.update_layout(barmode='group',
                                                      legend={'orientation': 'h', 'x': 0, 'y': 1.1},
                                                      margin=dict(t=0, b=0, l=0, r=0),  # Remove graph margins
                                                      paper_bgcolor='rgba(0,0,0,0)',
                                                      plot_bgcolor='rgba(0,0,0,0)',
                                                      template="simple_white"
                                                      )
        graph_spending_by_categories = dcc.Graph(id='graph1',
                                                 figure=self.fig_spending_by_categories,
                                                 )
        return self.fig_spending_by_categories

    def get_fig_spending_by_moth(self):
        self.fig_spending_by_moth = go.Figure()
        self.fig_spending_by_moth.add_trace(go.Bar(y=self.gr_spending_by_moth["Amount"].tolist(),
                                                   x=self.gr_spending_by_moth.index,
                                                   name="Avarage Spending",
                                                   orientation='v',
                                                   marker=dict(
                                                       color='red',
                                                   )
                                                   ))
        self.fig_spending_by_moth.add_trace(go.Bar(name="blabla",
                                                   y=self.gr_income_by_moth["Amount"].tolist(),
                                                   x=self.gr_income_by_moth.index,
                                                   orientation='v',
                                                   marker=dict(
                                                       color='green',
                                                   )
                                                   ))
        self.fig_spending_by_moth.update_layout(barmode='relative')
        graph_spending_by_moth = dcc.Graph(id='graph2',
                                           figure=self.fig_spending_by_moth,
                                           )
        return self.fig_spending_by_moth

    def get_fig_saving_by_month(self):
        self.fig_saving_by_month = go.Figure()
        self.fig_saving_by_month.add_trace(go.Bar(y=self.gr_saving_by_month["Amount"].tolist(),
                                                  x=self.gr_saving_by_month.index,
                                                  name="Avarage Spending",
                                                  orientation='v',
                                                  marker=dict(
                                                      color='red',
                                                  )
                                                  ))
        self.fig_saving_by_month.update_layout(barmode='relative')
        graph_saving_by_month = dcc.Graph(id='graph3',
                                          figure=self.fig_saving_by_month,
                                          )
        return self.fig_saving_by_month

    def get_fig_bank_balance(self):
        layout = {'title': {'text': 'DISPLAY ME!'}}
        self.fig_bank_balance = go.Figure(layout=layout)
        # self.fig_bank_balance.add_trace(go.Scatter(x=self.df['Date'],
        #                                       y=self.df['cum_sum'],
        #                                       mode='lines+markers',
        #                                       name='lines+markers',
        #                                       marker=dict(color='black',
        #                                                   )
        #                                       ))
        # self.fig_bank_balance.add_trace(go.Scatter(x=self.df_dkb['Date'],
        #                                       y=self.df_dkb['cum_sum'],
        #                                       mode='lines+markers',
        #                                       name='lines+markers',
        #                                       marker=dict(color='blue',
        #                                                   )
        #                                       ))
        # self.fig_bank_balance.add_trace(go.Scatter(x=self.df_credit_card['Date'],
        #                                       y=self.df_credit_card['cum_sum'],
        #                                       mode='lines+markers',
        #                                       name='lines+markers',
        #                                       marker=dict(color='orange',
        #                                                   )
        #                                       ))
        # self.fig_bank_balance.add_trace(go.Scatter(x=self.df_ksk['Date'],
        #                                       y=self.df_ksk['cum_sum'],
        #                                       mode='lines+markers',
        #                                       name='lines+markers',
        #                                       marker=dict(color='yellow',
        #                                                   )
        #                                       ))
        # fig_bank_balance.update_layout(barmode='relative')
        graph_bank_balance = dcc.Graph(id='state_bank_graph',
                                       figure=self.fig_bank_balance,
                                       )
        return self.fig_bank_balance

        # # show one graph on a page
        # self.fig_bank_balance.show()
        #
        #
        # app = dash.Dash(
        #     __name__,
        #     meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
        # )
        # app.title = "Clinical Analytics Dashboard"
        #
        # server = app.server
        # app.config.suppress_callback_exceptions = True
        #
        # app.layout = html.Div(
        #     id="app-container",
        #     children=[
        #         # Banner
        #         html.Div(
        #             id="banner",
        #             className="banner",
        #             children=[html.Img(src=app.get_asset_url("plotly_logo.png"))],
        #         ),
        #         # Left column
        #         # html.Div(
        #         #     id="left-column",
        #         #     className="four columns",
        #         #     children=[description_card(), generate_control_card()]
        #         #              + [
        #         #                  html.Div(
        #         #                      ["initial child"], id="output-clientside", style={"display": "none"}
        #         #                  )
        #         #              ],
        #         # ),
        #         # Right column
        #         html.Div(
        #             id="right-column",
        #             className="eight columns",
        #             children=[
        #                 # Patient Volume Heatmap
        #                 html.Div(
        #                     id="patient_volume_card",
        #                     children=[
        #                         html.B("Patient Volume"),
        #                         html.Hr(),
        #                         dcc.Graph(id="patient_volume_hm"),
        #                     ],
        #                 ),
        #                 # Patient Wait time by Department
        #                 # html.Div(
        #                 #     id="wait_time_card",
        #                 #     children=[
        #                 #         html.B("Patient Wait Time and Satisfactory Scores"),
        #                 #         html.Hr(),
        #                 #         html.Div(id="wait_time_table", children=initialize_table()),
        #                 #     ],
        #                 # ),
        #             ],
        #         ),
        #     ],
        # )


if __name__ == "__main__":
    graps = DataAnalytics()
