
# coding: utf-8

# In[3]:


import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
df = pd.read_csv("nama_10_gdp_1_Data.csv")

available_indicators = df['NA_ITEM'].unique()
Geo =df['GEO'].unique()
Years=df['TIME'].unique()
app.layout=html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label':i,'value':i} for i in available_indicators],
                value='Final consumption expenditure'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label':i,'value':i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display':'inline-block'}
            )
        ],
        style={'width':'48%','display':'inline-block'}),
    
        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label':i,'value':i} for i in available_indicators],
                value='Imports of services'
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label':i,'value':i} for i in ['Linear','Log']],
                value='Linear',
                labelStyle={'display':'inline-block'}
            )
        ],
        style={'width':'48%','float':'right','display':'inline-block'})
    

    ]),

    dcc.Graph(id='GDP-World'),
    dcc.Slider(
        id='year--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].min(),
        step=None,
        marks={str(year): str(year) for year in df['TIME'].unique()}
    ),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='yaxis-column1',
                options=[{'label':i,'value':i} for i in available_indicators],
                value='Imports of services'
            ),
          
        ],
        style={'width':'48%','float':'right','display':'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id='xaxis-column1',
                options=[{'label':i,'value':i} for i in Geo],
                value='Belgium'
            ),
            
        ],
        style={'width':'48%', 'display':'inline-block'})
        
        

    ]),

    dcc.Graph(id='GDP'),
    
])

@app.callback(
    dash.dependencies.Output('GDP-World','figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('yaxis-type', 'value'),
     dash.dependencies.Input('year--slider', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['TIME'] == year_value]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }


@app.callback(
    dash.dependencies.Output('GDP','figure'),
    [dash.dependencies.Input('xaxis-column1', 'value'),
     dash.dependencies.Input('yaxis-column1', 'value')])

def update_graph1(xaxis_column1_name, yaxis_column1_name):
   
    dff = df[df['GEO'] == xaxis_column1_name]
    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == yaxis_column1_name]['TIME'],
            y=dff[dff['NA_ITEM'] == yaxis_column1_name]['Value'],
           
            mode='line',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column1_name
            },
            yaxis={
                'title': yaxis_column1_name,
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }
if __name__ == '__main__':
    app.run_server()

