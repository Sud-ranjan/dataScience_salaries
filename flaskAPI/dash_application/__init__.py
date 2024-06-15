from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.BOOTSTRAP]
df = pd.read_csv('/Users/sudhanshuranjan/Documents/dataScience_salaries/explored_data_for_model.csv')
    
query_df = df.groupby('Sector').agg({
    'avg_salary': 'mean',
    'Rating': 'mean',
    'Job Title': 'size'
}).reset_index()

grouped_df = df.groupby('job_state').agg({
    'avg_salary': 'mean',
}).reset_index()


fig_map = go.Figure(data=go.Choropleth(
    locations=grouped_df['job_state'], # Spatial coordinates
    z = grouped_df['avg_salary'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Greens',
    colorbar_title = "Thousands USD",
))

fig_map.update_layout(
    title_text = '2024 | Salaries for Data science field',
    geo_scope='usa', # limite map scope to USA
)



query_df.rename(columns={'Job Title': 'count'}, inplace=True)
query_df = query_df[query_df['Sector'] != '-1']

fig_scatter = px.scatter(query_df, x="avg_salary", y="Rating",
                size="count",color='Sector',
                log_x=True, size_max=90)

fig_scatter.update_layout(
    title_text = '2024 | Inductry - Sector Wise Analysis',
    geo_scope='usa', # limite map scope to USA
)

def create_dash_app(flask_server):
    dash_app = Dash(__name__, server=flask_server, url_base_pathname='/dashboard/', external_stylesheets=external_stylesheets)    
    # dash_app.layout = html.Div([
    #     html.H1(children='Data Science Salaries', style={'textAlign':'center'}),
    #     dcc.Dropdown(df['job_title_simplified'].unique(), 'data scientist', id='job_title_selection'),
    #     dbc.Row(
    #         [
    #             dbc.Col(
    #                 dcc.Graph(
    #                     id='sector_wise_salaries',
    #                     figure=fig_scatter
    #                     # style={'width': '80%', 'height': '800px', 'margin': 'auto'}        
    #                 ),width=6
    #             ),
    #             dbc.Col(
    #                 dcc.Graph(
    #                     id='avg_salaries_in_states',
    #                     figure=fig_map
    #                     # style={'width': '80%', 'height': '800px', 'margin': 'auto'}        
    #                 ),width=6
    #             ),
    #         ],
    #     )
    # ])
    dash_app.layout = dbc.Container([
    html.H1(children='Data Science Salaries', style={'textAlign':'center'}),
    dcc.Dropdown(df['job_title_simplified'].unique(), 'data scientist', id='job_title_selection'),
    dbc.Row([
        dbc.Col(
            dcc.Graph(
                id='sector_wise_salaries',
                figure=fig_scatter
                # style={'width': '80%', 'height': '100%', 'margin': 'auto'}        
            ),
            width=6
        ),
        dbc.Col(
            dcc.Graph(
                id='avg_salaries_in_states',
                figure=fig_map
                # style={'width': '80%', 'height': '100%', 'margin': 'auto'}        
            ),
            width=6
        ),
    ])
])



    @dash_app.callback(
    [Output('sector_wise_salaries', 'figure'),
     Output('avg_salaries_in_states', 'figure')],
    [Input('job_title_selection', 'value')]
    )
    def update_graph(selected_metric):

        grouped_df = df[df['job_title_simplified'] == selected_metric].groupby('job_state').agg({
            'avg_salary': 'mean',
        }).reset_index()


        fig_map = go.Figure(data=go.Choropleth(
            locations=grouped_df['job_state'], # Spatial coordinates
            z = grouped_df['avg_salary'].astype(float), # Data to be color-coded
            locationmode = 'USA-states', # set of locations match entries in `locations`
            colorscale = 'Greens',
            colorbar_title = "Thousands USD",
        ))

        fig_map.update_layout(
            title_text = '2024 | Salaries for Data science field ({})'.format(selected_metric),
            geo_scope='usa', # limite map scope to USA
        )

        query_df = df[df['job_title_simplified'] == selected_metric].groupby('Sector').agg({
            'avg_salary': 'mean',
            'Rating': 'mean',
            'Job Title': 'size'
        }).reset_index()

        query_df.rename(columns={'Job Title': 'count'}, inplace=True)
        query_df = query_df[query_df['Sector'] != '-1']

        fig_scatter = px.scatter(query_df, x="avg_salary", y="Rating",
                        size="count",color='Sector',
                        log_x=True, size_max=90)

        fig_scatter.update_layout(
            title_text = '2024 | Inductry - Sector Wise Analysis ({})'.format(selected_metric),
            geo_scope='usa', # limite map scope to USA
        )

        return fig_map, fig_scatter

    return dash_app
