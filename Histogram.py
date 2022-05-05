import pandas as pd
import plotly.express as px 
import dash
from dash import Dash, dcc, html, Input, Output


# crear un dataframe con toda la informacion de la encuesta
df21 = pd.read_csv ('survey/survey_results_public2021.csv', index_col = [0]) # El indice sera la columna con el ID de la respuesta

# crear un dataframe con toda la informacion de la encuesta
df20 = pd.read_csv ('survey/survey_results_public2020.csv', index_col = [0]) # El indice sera la columna con el ID de la respuesta

# crear un nuevo df copiando solo la columna Age1stCode
df1 = df21[['Age1stCode']]

# normalizar todos los datos.
df1 = df1[df1['Age1stCode'].notna()] # eliminar los nulos

df1.loc[df1["Age1stCode"] == "Younger than 5 years", "Age1stCode"] = "04 - 04 years"  # ya hay un 05 anyos en el df.
df1.loc[df1["Age1stCode"] == "Older than 64 years", "Age1stCode"] = "65 - 65 years"  # ya hay un 05 anyos en el df.
df1.loc[df1["Age1stCode"] == "5 - 10 years", "Age1stCode"] = "05 - 10 years"

df3 = crime_year = pd.DataFrame(df1['Age1stCode'].value_counts().reset_index().values, columns=["RangoEdad", "count"])

# primero se seleccionan los digitos del string (la columna del df es string) y el resultado se convierte a entero
df3["min"] = df3.RangoEdad.astype(str).str[:2].astype(int) #la edad minima del rango es el primer numero

# cambiar el nombre de los nuevos rangos
df3.loc[df3["RangoEdad"] == "04 - 04 years", "RangoEdad"] = "Younger than 5 years"  # ya hay un 05 anyos en el df.
df3.loc[df3["RangoEdad"] == "65 - 65 years", "RangoEdad"] = "Older than 64 years"  # ya hay un 05 anyos en el df.

df3["csv"]=2020 # anyadir una columna para diferenciar el csv
# anyadir una columna para distingir el csv
df3["csv"] = 2021

# ordenar los datos del df.
df3.set_index('min',inplace=True)

df2 = df20[['Age1stCode']]

# normalizar todos los datos.
df2 = df2[df2['Age1stCode'].notna()] # eliminar los nulos

df2.loc[df2["Age1stCode"] == "Younger than 5 years", "Age1stCode"] = "4" # ya hay un 05 anyos en el df.
df2.loc[df2["Age1stCode"] == "Older than 85", "Age1stCode"] = "86"

df2['Age1stCode'] = df2.Age1stCode.astype(int) # toda la columna es enteros

# dado que el corte de edad es diferente entre ambos se crean cortes para dividir los datos igual
bins = [1, 5, 10, 18, 25, 35, 45, 55, 65, 75, 85, 86]
df4 = pd.DataFrame(df2['Age1stCode'].value_counts(bins= bins, sort=False).reset_index().values, columns=["Rango", "count"])

df4["min"] = df4.Rango.astype(str).str[6:9].astype(str) #la edad minima del rango es el primer numero
df4.loc[df4["min"] == ", 5", "min"] = "5"  
df4.loc[df4["min"] == "10.", "min"] = "10" 

df4["min"] = df4["min"].astype(int)

df4["csv"]=2020 #anyadir una columna para diferenciar el csv

df4["RangoEdad"] = ["Younger than 5 years", "05 - 10 years",
                    "11 - 17 years","18 - 24 years",
                    "25 - 34 years", "35 - 44 years",
                    "45 - 54 years","55 - 64 years",
                    "65 - 74 years","75 - 84 years",
                    "Older than 85 years"]

# se hace una copia del df.
df= df21.copy()

# normalizar todos los datos.
df.loc[df["MainBranch"] == "None of these", "MainBranch"] = "Other"


df = df.groupby(['MainBranch', ], as_index=False).size()

# el % = valor*100 / total
df['porcentaje'] = 100 * df['size'] / df['size'].sum()


# Initialise the app
app = dash.Dash(__name__, assets_folder='assets/')  # dash.Dash para que pueda coger el css
server = app.server  # heroku
sidebar = html.Div(
    children=[
        html.H2('DASH - STACKOVERFLOW'),
        html.P('Visualising data with Plotly - Dash.'),
        html.P('Pick one year from the dropdown below.'),
        html.Div(
            className='div-user-controls',
            children=[
                html.Div(
                    className='div-for-dropdown',
                    children=[
                        dcc.Dropdown(id="select_opt",  options=[ #el usuario va a ver las label.
                            {"label": "2021", "value": 2021},
                            {"label": "2020", "value": 2020}],
                                     multi=False,
                                     value="2020"
                                     #style={'width': "50%"}
                                    )
                    ],
                ),
            ]
        )
    ],
    style = {'position': 'fixed','left': '0px','top': '0px','bottom': '0px',
                     'width': '329px','height': '100%','background-color': '#edeff2'}

)


content = html.Div(
    id= "page-content",#className='main',
    # aqui dentro se pueden meter mas menus para un grafico en particular. IE:
    #children=[
    #dcc.Dropdown(id="select_option",  options=[ #el usuario va a ver las label.
    #                    {"label": "2021", "value": 2021},
    #                    {"label": "2020", "value": 2020}],
    #                multi=False,
    #                value="2020",
    #                style={'width': "40%"}
    #                ),

    children=[
        html.Div(
            className='div-for-text',
            children=[
                html.H2('Age - histogram'), 
                html.P('''Different age groups and their recurrence''')
            ]
        ),
        html.Div(
            className='div-for-charts',
            children = [dcc.Graph(id='primero', figure={}) # graph container
                       ]
            
        ),
        html.Div(
            className='div-for-text',
            children=[
                html.H2('Main Branch - Pie chart'), 
                html.P('''Correlation between with software development and stackoverflow users''')
            ]
        ),
        html.Div(
            className='div-for-charts',
            children = [dcc.Graph(id='segundo', figure={})]
            
        ),
        html.Div(
            className='div-for-text',
            children=[
                html.H2('Main Branch - Bar char'), 
                html.P('''A basic Dashboard with Dash and Plotly, showing the adjusted price history of several car companies.''')
            ]
        ),
        html.Div(
            className='div-for-charts',
            children = [dcc.Graph(id='tercero', figure={})]
            
        ),
        
    ],
    style= {'height': '100%','padding-left': '329px','background-color': '#edeff2',
            'font-family': 'Oswald, sans-serif','color': 'rgba(0, 0, 0, 0.74)',
            'font-size': '16px','line-height': '20px'}
)       


# layout de los dos componentes
app.layout = html.Div([sidebar, content])



@app.callback(
    Output(component_id='primero', component_property='figure'),
    Input(component_id='select_opt', component_property='value'))
def update_graph(option_slctd):
    #filtered_df = df[df.year == selected_year]
    cfg = [("x", "RangoEdad"), ("y", "count")]
    
    if (option_slctd == 2021): 
        fig = px.histogram(df3, **{ax: col for ax, col in cfg}, 
                           category_orders={'RangoEdad':["Younger than 5 years", 
                            "05 - 10 years", "11 - 17 years", "18 - 24 years", "25 - 34 years", "35 - 44 years",
                            "45 - 54 years", "55 - 64 years", "Older than 64 years"]},
                          labels={"count":"# Responses", "RangoEdad":"Age range"})            
        # 'ggplot2', 'seaborn', 'simple_white', 'plotly',
                                  # 'plotly_white', 'plotly_dark', 'presentation',
                                  # 'xgridoff', 'ygridoff', 'gridon', 'none')

        # category_orders={'year':    
                           # force a specific ordering of values per column
    # [2013,2012,2011,2010,2009,2008,2007,2006,2005,2004,2003,2002,2001]},)
    else: fig = px.histogram(df4, **{ax: col for ax, col in cfg})
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',}) #fondo transparente
    fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False)) #eliminar grid
    
    return fig

@app.callback( #diagrama de quesito
    Output(component_id='segundo', component_property='figure'),
    Input(component_id='select_opt', component_property='value'))
def update_graph(optionse):
    fig=px.pie(data_frame=df, names=df['MainBranch'], values = df['size'],hole=.3,)
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',})
    return fig


@app.callback( #diagrama de quesito
    Output(component_id='tercero', component_property='figure'),
    Input(component_id='select_opt', component_property='value'))
def update_graph(optionse):
    fig= px.bar(df, x= df['size'], 
                 y=df['MainBranch'], 
                 orientation = "h", # orientacion "h"/"v"
                 text = df['size'],
                labels={"size":"# Responses", "MainBranch":"Main Branch"})
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',})              
    fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
    return fig



# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
