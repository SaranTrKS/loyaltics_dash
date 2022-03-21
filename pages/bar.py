import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash import Dash, dcc, html, Input, Output
import pathlib
from app import app

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#
# app = Dash(__name__, external_stylesheets = external_stylesheets)
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

table = pd.read_excel(DATA_PATH.joinpath("Retail_Data.xlsx"), sheet_name = [0, 1, 2])

trans = table[0]
cus_demo = table[1]
cus_add = table[2]

trans = trans.dropna()
trans['profit'] = trans['list_price'] - trans['standard_cost']

trans['count'] = [1 for i in range(len(trans))]

cus_compl = pd.merge(cus_add,cus_demo, how = 'outer', on = 'customer_id')

cus_compl.dropna(inplace = True)
cus_compl.set_index('customer_id', inplace=True)

for i in cus_compl.index:
    if cus_compl.loc[i,'age'] < 21:
        cus_compl.loc[i,'age'] = 'Teen'
    elif cus_compl.loc[i,'age'] > 20 and cus_compl.loc[i,'age'] < 36:
        cus_compl.loc[i,'age'] = 'Youth'
    elif cus_compl.loc[i,'age'] > 35 and cus_compl.loc[i,'age'] < 50:
        cus_compl.loc[i,'age'] = '35-50'
    else:
        cus_compl.loc[i,'age'] = '50+'

layout = html.Div([
    dcc.Dropdown(id = 'dpdn2', value= ['Mass Customer'], multi = True,
                 options= [{'label': x, 'value':x} for x in
                           cus_compl.wealth_segment.unique()]),
    html.Div([
        dcc.Graph(id= 'pie-graph', figure = {}, className= 'six columns'),
        dcc.Graph(id = 'my-graph', figure = {}, clickData=None, hoverData=None,
                  config={
                    'staticPlot': False,     # True, False
                      'scrollZoom': True,      # True, False
                      'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
                      'showTips': False,       # True, False
                      'displayModeBar': True,  # True, False, 'hover'
                      'watermark': True,
                  },
                  className='six columns'
                  )
    ])
])

@app.callback(
    Output(component_id='my-graph', component_property='figure'),
    Input(component_id='dpdn2',component_property='value'),
)
def update_graph(wealth_chosen):
    dff = cus_compl[cus_compl.wealth_segment.isin(wealth_chosen)]
    fig = px.scatter(data_frame=dff, x='age', y='past_3_years_bike_related_purchases', color='wealth_segment',
                  custom_data=['job_industry_category', 'gender', 'job_industry_category', 'state'])
    fig.update_traces(mode='markers')
    return fig


@app.callback(
    Output(component_id='pie-graph', component_property='figure'),
    Input(component_id='my-graph', component_property='hoverData'),
    Input(component_id='my-graph', component_property='clickData'),
    Input(component_id='my-graph', component_property='selectedData'),
    Input(component_id='dpdn2', component_property='value')
)
def update_side_graph(hov_data, clk_data, slct_data, wealth_chosen):
    if hov_data is None:
        dff2 = cus_compl[cus_compl.wealth_segment.isin(wealth_chosen)]
        dff2 = dff2[dff2.age == 'Teen']
        print(dff2)
        fig2 = px.pie(data_frame=dff2, values='job_industry_category', names='state',
                      title='Customer Analysis')
        return fig2
    else:
        print(f'hover data: {hov_data}')
        # print(hov_data['points'][0]['customdata'][0])
        # print(f'click data: {clk_data}')
        # print(f'selected data: {slct_data}')
        dff2 = cus_compl[cus_compl.wealth_segment.isin(wealth_chosen)]
        hov_age = hov_data['points'][0]['x']
        dff2 = dff2[dff2.age == hov_age]
        fig2 = px.pie(data_frame=dff2, values='past_3_years_bike_related_purchases', names='state', title=f'Analysis for: {hov_age}')
        return fig2

