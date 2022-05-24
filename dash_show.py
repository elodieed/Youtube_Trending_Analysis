# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

import time
from functools import reduce

from lib.function_test import get_nameCategory, get_monthNyears

app = Dash(__name__)


#----------------------------------------------------------------------------
data_path = './Data/FR_youtube_trending_data.csv'
yt_comment = pd.read_csv(data_path)

yt_comment['categoryId'] = yt_comment['categoryId'].apply(lambda x: get_nameCategory(int(x)))

yt_comment['publishedAt'] = yt_comment['publishedAt'].apply(lambda x: get_monthNyears(x))

df_monthCategory = yt_comment.groupby(['categoryId', 'publishedAt'])['view_count'].sum()
df_monthCategory = df_monthCategory.reset_index()

#--------------------------------------------------------------------------

list_categorie = list(yt_comment['categoryId'])
categorie = list(set(yt_comment['categoryId']))

nbr_video = [list_categorie.count(j) for j in categorie]

total = int(reduce(lambda x, y : x+y, nbr_video))
pourcentage = list(map(lambda x : round(x*100/total, 2), nbr_video))

df_pro = pd.DataFrame()
df_pro['Category'] = categorie
df_pro['Video %'] = pourcentage

#--------------------------------------------------------------------------

time.sleep(3)

fig = px.pie(df_pro, values='Video %', names='Category', hole=.3, color_discrete_sequence=px.colors.sequential.RdBu)

app.layout = html.Div(children=[
    html.H1(children='Youtube Analysis Dashboard', style={"text-align":"center"}),

    html.B(style={"backgroun-color":"cornflowerblue"}),
    html.Div([dcc.Dropdown(id="slect_years",
                    options=[
                        {"label": "2020", "value":2020},
                        {"label": "2021", "value":2021},
                        {"label": "2022", "value":2022}],
                        multi=False,
                        value=2020,
                        style={'wight':"40%"}),
    
    html.Br(),

    html.H3(children='''
        Number of view per month for all category
    '''),

    dcc.Graph(
        id='view-graph'
    )]),
    html.Br(),

    html.Div([html.H3(children='''Trend composition'''),

                dcc.Graph(
                    id='cat-graph', figure=fig )])
])

@app.callback(
    Output(component_id='view-graph', component_property='figure'), 
    [Input(component_id='slect_years', component_property='value')])

def update_graph(option_select):
    dff = df_monthCategory[df_monthCategory.publishedAt.str.contains(str(option_select))]

    fig = px.bar(dff, x="publishedAt", y="view_count", color="categoryId")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)