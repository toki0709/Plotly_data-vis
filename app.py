from logging import debug
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
from pandas.io.formats import style
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import pandas_datareader.data as web
import datetime
from datetime import date

today = datetime.datetime.today()
start = datetime.datetime(2020, 1, 1)

# Fetching the API with pandas dataread for the following stocks
# --------------- % % % % ----------------------

# df = web.DataReader(['AMZN', 'GOOGL', 'FB', 'PFE', 'BNTX',
#                      'MRNA'], 'yahoo', start=start, end=today)


# df = df.stack().reset_index()

# df.to_csv('Data_file.csv', index=False)

# Converting the API data to CSV
# ---------------- % % %  % -----------------
df = pd.read_csv('Data_file.csv')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale:1.0'}])


# Layout with BOOTSTRAP
# -----------------------  % % % % ---------------------

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1('Stock Market DashBoard',
                        className='text-center mb-4 p-5 text-primary'), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='my-dpdn', multi=False, value='AMZN',
                         options=[{'label': x, 'value': x}
                                  for x in sorted(df['Symbols'].unique())]),
            dcc.Graph(id='line-fig', figure={})
        ],  # width={'size':5, 'offset':1},
            xs=12, sm=12, md=12, lg=5, xl=5, className='flex-fill text-primary'),

        dbc.Col([
            dcc.Dropdown(id='my-dpdn2', multi=True, value=['GOOGL', 'FB', 'PFE'],
                         options=[{'label': x, 'value': x}
                                  for x in sorted(df['Symbols'].unique())]),

            dcc.Graph(id='line-fig2', figure={})
        ],  # width={'size':5, 'offset':1},
            xs=12, sm=12, md=12, lg=5, xl=5, className='flex-fill text-primary'),
    ]),

    dbc.Row([
        dbc.Col([
            html.P("Select Company Stock:",
                   className='text-center text-primary'),
            dcc.Checklist(id='my-checklist', value=['FB', 'GOOGL', 'AMZN'],
                          options=[{'label': x, 'value': x}
                                   for x in sorted(df['Symbols'].unique())],
                          labelClassName="px-3 "),
            dcc.Graph(id='my-hist', figure={}),
        ],  # width={'size':5, 'offset':1},
            xs=12, sm=12, md=12, lg=5, xl=5
        )
    ],  className='justify-content-center'),  # Vertical: start, center, end

    dbc.Row([
        dbc.Col(html.P('Created by Toki Tazwar 04.11.2021',
                       className='text-center p-2 text-info'), width=12)
    ]),

])


# app callbacks
# ---------------------- % % % % -----------------------

@app.callback(
    Output('line-fig', 'figure'),
    Input('my-dpdn', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['Symbols'] == stock_slctd]
    figln = px.line(dff, x='Date', y='High')
    return figln


# Line chart - multiple
@app.callback(
    Output('line-fig2', 'figure'),
    Input('my-dpdn2', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['Symbols'].isin(stock_slctd)]
    figln2 = px.line(dff, x='Date', y='Open', color='Symbols')
    return figln2


# Histogram
@app.callback(
    Output('my-hist', 'figure'),
    Input('my-checklist', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['Symbols'].isin(stock_slctd)]
    dff = dff[dff['Date'] == '2020-12-03']
    fighist = px.histogram(dff, x='Symbols', y='Close')
    return fighist


# Running the app
# ------------ % % % % ---------------
if __name__ == '__main__':
    app.run_server(debug=True, port=3000)
