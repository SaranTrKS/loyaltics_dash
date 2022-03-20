import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash import Dash, dcc, html, Input, Output
from pages import bar, customerAnalysis

from app import app
from app import server
import pathlib

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets = external_stylesheets)
server = app.server


table = pd.read_excel('Retail_Data.xlsx', sheet_name = [0, 1, 2])

trans = table[0]
cus_demo = table[1]
cus_add = table[2]

trans = trans.dropna()
trans['profit'] = trans['list_price'] - trans['standard_cost']
#df1 = trans.groupby()

# App layout
fig1 = px.bar(trans, x="brand", y="profit", color="product_size", barmode="group",
                        facet_row="online_order", facet_col="product_line")
    #              category_orders={"day": ["Thur", "Fri", "Sat", "Sun"],
    #                               "time": ["Lunch", "Dinner"]}
    #fig1.show()
app.layout = html.Div([
    dcc.Location(id='url', refresh= False),
    html.Div([
        dcc.Link('barcharts', href='/pages/bar'),
        dcc.Link('Customer Analysis', href='/pages/customerAnalysis'),
    ], className="row"),
    html.Div(id='page-content', children=[]),
    html.H4('Loyaltics Case Study'),
    html.P("Orders"),
    dcc.Dropdown(id='orders',
        options=['online_order', 'order_status', 'brand', 'product_line','product_class'],
        value='product_class', clearable=False
    ),
    html.P("Values:"),
    dcc.Dropdown(id='values',
        options=['list_price', 'standard_cost','profit'],
        value='list_price', clearable=False
    ),
    dcc.Graph(id="graph"),
    html.H4('Analysis on bikes'),
    dcc.Graph(id = 'graph2',
              figure = fig1),
])


@app.callback(
    Output("graph", "figure"),

    Input("orders", "value"),
    Input("values", "value"))
def generate_chart(names, values):
    df = trans
    fig = px.pie(df, values=values, names=names, hole=.3, title= " Analysis of Orders",
                template = 'gridon')
    fig.update_traces(textposition= 'outside', textinfo= 'percent+label')


    return fig

@app.callback(Output('page-content','children'),
          Input('url','pathname'))
def display_page(pathname):
    if pathname == '/pages/bar':
        return bar.layout
    elif pathname == '/pages/customerAnalysis':
        return customerAnalysis.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=False)

