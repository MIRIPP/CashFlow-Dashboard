import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import numpy as np

# Assuming you have df_spending_filtered and df_income_filtered DataFrames
# Replace this with your actual data

# Sample DataFrames for demonstration purposes
df_spending_filtered = pd.DataFrame({
    'Date': pd.date_range('2022-01-01', '2022-12-31', freq='D'),
    'Amount': np.random.randint(-100, 100, size=(365)),
    'Category': np.random.choice(['Category1', 'Category2', 'Category3'], size=(365))
})

df_income_filtered = pd.DataFrame({
    'Date': pd.date_range('2022-01-01', '2022-12-31', freq='D'),
    'Amount': np.random.randint(0, 200, size=(365)),
    'Category': np.random.choice(['Income1', 'Income2', 'Income3'], size=(365))
})

# Combine spending and income DataFrames
combined_df = pd.concat([df_spending_filtered, df_income_filtered])

# Extract month from Date
combined_df['Month'] = combined_df['Date'].dt.to_period('M')

# Group by Month and Category, summing up the Amount
gr_combined_by_month_and_category = combined_df.groupby(['Month', 'Category']).sum().reset_index()

# Create Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    dcc.Graph(
        id='monthly-bar-chart',
        figure={}
    )
])

# Callback function to update the graph based on user input
@app.callback(
    dash.dependencies.Output('monthly-bar-chart', 'figure'),
    [dash.dependencies.Input('monthly-bar-chart', 'value')]
)
def update_graph(value):
    # Create a bar chart using Plotly Express
    fig = px.bar(
        gr_combined_by_month_and_category,
        x='Month',
        y='Amount',
        color='Category',
        labels={'Amount': 'Total Amount'},
        title='Monthly Spending and Income by Category'
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)