from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.BOOTSTRAP]
df = pd.read_csv('/Users/sudhanshuranjan/Documents/dataScience_salaries/explored_data_for_model.csv')


def plot_scatter(df,selection = None):
    if selection:
        query_df = df[df['job_title_simplified'] == selection].groupby('Sector').agg({
            'avg_salary': 'mean',
            'Rating': 'mean',
            'Job Title': 'size'
        }).reset_index()
    else:
        query_df = df.groupby('Sector').agg({
            'avg_salary': 'mean',
            'Rating': 'mean',
            'Job Title': 'size'
        }).reset_index()

    query_df.rename(columns={'Job Title': 'count'}, inplace=True)
    query_df = query_df[query_df['Sector'] != '-1']

    fig_scatter = px.scatter(query_df, x="avg_salary", y="Rating",
                    size="count",color='Sector',
                    log_x=True, size_max=90)
    if selection:
        fig_scatter.update_layout(
            title_text = '2024 | Inductry - Sector Wise Analysis',
            geo_scope='usa', # limite map scope to USA
            showlegend=False
        )
    else:
        fig_scatter.update_layout(
            title_text = '2024 | Inductry - Sector Wise Analysis ({})'.format(selection),
            geo_scope='usa', # limite map scope to USA
            showlegend=False
        )
    return fig_scatter


def plot_map(df,selection = None):
    if selection:
        query_df = df[df['job_title_simplified'] == selection].groupby('job_state').agg({
            'avg_salary': 'mean',
        }).reset_index()
    else:
        query_df = df.groupby('job_state').agg({
            'avg_salary': 'mean',
        }).reset_index()

    fig_map = go.Figure(
            data=go.Choropleth(
                locations=query_df['job_state'], # Spatial coordinates
                z = query_df['avg_salary'].astype(float), # Data to be color-coded
                locationmode = 'USA-states', # set of locations match entries in `locations`
                colorscale = 'Greens',
                colorbar_title = "Thousands USD",
            )
        )
    if selection:
        fig_map.update_layout(
            title_text = '2024 | Salaries for Data science field ({})'.format(selection),
            geo_scope='usa', # limite map scope to USA
        )
    else:
        fig_map.update_layout(
            title_text = '2024 | Salaries for Data science field',
            geo_scope='usa', # limite map scope to USA
        )
    return fig_map

def plot_bar_counts(df = df[df['job_title_simplified'] != 'na']):
    query_df = df.groupby('job_title_simplified').agg({
            'avg_salary': 'mean',
            'Job Title': 'size'
        }).reset_index()
    query_df.rename(columns={'Job Title': 'count'}, inplace=True)
    bar_plot = go.Figure(
    data = go.Bar(
    x=query_df['count'],
    y=query_df['job_title_simplified'],
    orientation='h',
    marker=dict(color='grey'),  # Bar color
    text=query_df['count']
    ))

    bar_plot.update_layout(
        title='Role wise Total Jobs',
        xaxis={'title': 'Total Jobs'},
        yaxis={'title': 'Job Title'},
        hovermode='closest'
    )
    return bar_plot

def plot_bar_salary(df = df[df['job_title_simplified'] != 'na']):
    query_df = df.groupby('job_title_simplified').agg({
            'avg_salary': 'mean',
            'Job Title': 'size'
        }).reset_index()
    query_df.rename(columns={'Job Title': 'count'}, inplace=True)

    bar_plot = go.Figure(
    data = go.Bar(
    x=query_df['avg_salary'],
    y=query_df['job_title_simplified'],
    orientation='h',
    marker=dict(color='green'),  # Bar color
    text= query_df['avg_salary'].apply(lambda x: '$'+str(round(x)) + ' K')
    ))

    bar_plot.update_layout(
        title='Role wise avg Salaries',
        xaxis={'title': 'Avg Salary (in thousand $)'},
        yaxis={'title': 'Job Title'},
        hovermode='closest'
    )
    return bar_plot


def create_dash_app(flask_server):
    dash_app = Dash(__name__, server=flask_server, url_base_pathname='/dashboard/', external_stylesheets=external_stylesheets)
    dash_app.layout = dbc.Container([
    html.Br(),
    html.H3(children='Data Science Salaries', style={'textAlign':'center'}),
    html.Br(),
    html.H4(children ='Avg Salaries vs Job counts (by role)',style = {'textAlign':'left'}),
    html.Hr(),
    dbc.Row([
        dbc.Col(
            dcc.Graph(
                id='Total Jobs by role',
                figure=plot_bar_counts()
            )
        ),
        dbc.Col(
            dcc.Graph(
                id='Avg Salary by role',
                figure=plot_bar_salary()
            )
        )
    ]),
    html.Hr(),
    dcc.Dropdown(df[df['job_title_simplified'] != 'na']['job_title_simplified'].unique(), 'data scientist', id='job_title_selection'),
    dbc.Row([
        dbc.Col(
            dcc.Graph(
                id='sector_wise_salaries',
                figure=plot_scatter(df)
            )
        ),
        dbc.Col(
            dcc.Graph(
                id='avg_salaries_in_states',
                figure=plot_map(df)
            )
        ),
        ])
    ])

    @dash_app.callback(
    [Output('sector_wise_salaries', 'figure'),
     Output('avg_salaries_in_states', 'figure')],
    [Input('job_title_selection', 'value')]
    )
    def update_graph(selected_metric):

        fig_map = plot_map(df,selected_metric)
        fig_scatter = plot_scatter(df,selected_metric)
        return fig_map, fig_scatter
    
    return dash_app
