import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash import Dash, dcc, html, Input, Output
from app import app
import pathlib

#app = dash.Dash(__name__)

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

table = pd.read_excel(DATA_PATH.joinpath("Retail_Data.xlsx"), sheet_name = [0, 1, 2])

trans = table[0]
cus_demo = table[1]
cus_add = table[2]

cus_compl = pd.merge(cus_add, cus_demo, how='outer', on='customer_id')

cus_compl.dropna(inplace=True)
cus_compl.set_index('customer_id', inplace=True)

for i in cus_compl.index:
    if cus_compl.loc[i, 'age'] < 21:
        cus_compl.loc[i, 'age'] = 'Teen'
    elif cus_compl.loc[i, 'age'] > 20 and cus_compl.loc[i, 'age'] < 36:
        cus_compl.loc[i, 'age'] = 'Youth'
    elif cus_compl.loc[i, 'age'] > 35 and cus_compl.loc[i, 'age'] < 50:
        cus_compl.loc[i, 'age'] = '35-50'
    else:
        cus_compl.loc[i, 'age'] = '50+'

#app = dash.Dash(__name__)

layout = html.Div([

    html.Div([
        html.Pre(children="Customer Analysis of Bike Sales in Australia",
                 style={"text-align": "center", "font-size": "100%", "color": "black"})
    ]),

    html.Div([
        html.Label(['X-axis categories to compare:'], style={'font-weight': 'bold'}),
        dcc.RadioItems(
            id='xaxis_raditem',
            options=[
                {'label': 'Age groups of customers', 'value': 'age'},
                {'label': 'State', 'value': 'state'},
                {'label': 'Economical Status', 'value': 'wealth_segment'},
                {'label': 'Job Industrry', 'value': 'job_industry_category'}
            ],
            value='age',
            style={"width": "50%"}
        ),
    ]),

    html.Div([
        html.Br(),
        html.Label(['Y-axis values to compare:'], style={'font-weight': 'bold'}),
        dcc.RadioItems(
            id='yaxis_raditem',
            options=[
                {'label': 'Bike Purchases', 'value': 'past_3_years_bike_related_purchases'},

            ],
            value='past_3_years_bike_related_purchases',
            style={"width": "50%"}
        ),
    ]),

    html.Div([
        dcc.Graph(id='the_graph')
    ]),

])


@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='xaxis_raditem', component_property='value'),
     Input(component_id='yaxis_raditem', component_property='value')]
)
def update_graph(x_axis, y_axis):
    dff = cus_compl
    # print(dff[[x_axis,y_axis]][:1])

    barchart = px.bar(
        data_frame=dff,
        x=x_axis,
        y=y_axis,
        title=y_axis + ': by ' + x_axis,
        facet_col='age',
        color='state',
        barmode='group',
    )

    barchart.update_layout(xaxis={'categoryorder': 'total ascending'},
                           title={'xanchor': 'center', 'yanchor': 'top', 'y': 0.9, 'x': 0.5, })

    return (barchart)



