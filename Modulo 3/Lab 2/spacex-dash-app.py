# Importar las librerías requeridas
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Leer los datos de la aerolínea en un dataframe de pandas
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Crear una aplicación de dash
app = dash.Dash(__name__)

# Crear el layout de la aplicación
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TAREA 1: Agregar un componente de menú desplegable para seleccionar el sitio de lanzamiento
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'},
                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                 ],
                 value='ALL',
                 placeholder="Select a Launch Site here",
                 searchable=True
                 ),
    html.Br(),

    # TAREA 2: Agregar un gráfico circular para mostrar la tasa de éxito de los lanzamientos
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    
    # TAREA 3: Agregar un control deslizante para seleccionar el rango de la carga útil
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={i: f'{i}' for i in range(0, 10001, 2500)},
                    value=[min_payload, max_payload]
                    ),

    # TAREA 4: Agregar un gráfico de dispersión para mostrar la correlación entre la carga útil y el éxito
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TAREA 2:
# Agregar una función de callback para renderizar el gráfico success-pie-chart basado en la selección del sitio
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, 
                     values='class', 
                     names='Launch Site', 
                     title='Total Success Launches By Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        site_df = filtered_df.groupby(['class']).size().reset_index(name='class count')
        fig = px.pie(site_df, 
                     values='class count', 
                     names='class', 
                     title=f'Total Success Launches for site {entered_site}')
        return fig

# TAREA 4:
# Agregar una función de callback para renderizar el gráfico success-payload-scatter-chart
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
               Input(component_id="payload-slider", component_property="value")])
def update_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]

    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, 
                         x='Payload Mass (kg)', 
                         y='class', 
                         color='Booster Version Category',
                         title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        site_filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(site_filtered_df, 
                         x='Payload Mass (kg)', 
                         y='class', 
                         color='Booster Version Category',
                         title=f'Correlation between Payload and Success for site {entered_site}')
        return fig

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)