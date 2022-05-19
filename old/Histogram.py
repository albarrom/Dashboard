import pandas as pd
import plotly.express as px 
import dash
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import numpy as np

#crear un dataframe con toda la informacion de la encuesta
df21 = pd.read_csv ('survey/survey_results_public2021.csv', index_col = [0]) # El indice sera la columna con el ID de la respuesta


#crear un dataframe con toda la informacion de la encuesta
df20 = pd.read_csv ('survey/survey_results_public2020.csv', index_col = [0]) # El indice sera la columna con el ID de la respuesta
df20 #mostrar df ()

#crear un nuevo df copiando solo la columna Age1stCode
df1 = df21[['Age1stCode']]


#normalizar todos los datos.
df1 = df1[df1['Age1stCode'].notna()] #eliminar los nulos


df1.loc[df1["Age1stCode"] == "Younger than 5 years", "Age1stCode"] = "04 - 04 years" #ya hay un 05 anyos en el df. 
df1.loc[df1["Age1stCode"] == "Older than 64 years", "Age1stCode"] = "65 - 65 years" #ya hay un 05 anyos en el df. 
df1.loc[df1["Age1stCode"] == "5 - 10 years", "Age1stCode"] = "05 - 10 years"

df3 = crime_year = pd.DataFrame(df1['Age1stCode'].value_counts().reset_index().values, columns=["RangoEdad", "count"])

#primero se seleccionan los digitos del string (la columna del df es string) y el resultado se convierte a entero
df3["min"] = df3.RangoEdad.astype(str).str[:2].astype(int) #la edad minima del rango es el primer numero

#cambiar el nombre de los nuevos rangos
df3.loc[df3["RangoEdad"] == "04 - 04 years", "RangoEdad"] = "Younger than 5 years" #ya hay un 05 anyos en el df. 
df3.loc[df3["RangoEdad"] == "65 - 65 years", "RangoEdad"] = "Older than 64 years" #ya hay un 05 anyos en el df. 

df3["csv"]=2020 #anyadir una columna para diferenciar el csv
#anyadir una columna para distingir el csv
df3["csv"] = 2021

#ordenar los datos del df. 
df3.set_index('min',inplace=True)



df2 = df20[['Age1stCode']]

#normalizar todos los datos.
df2 = df2[df2['Age1stCode'].notna()] #eliminar los nulos

df2.loc[df2["Age1stCode"] == "Younger than 5 years", "Age1stCode"] = "4" #ya hay un 05 anyos en el df. 
df2.loc[df2["Age1stCode"] == "Older than 85", "Age1stCode"] = "86"

df2['Age1stCode'] = df2.Age1stCode.astype(int) # toda la columna es enteros


#dado que el corte de edad es diferente entre ambos se crean cortes para dividir los datos igual
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

#se hace una copia del df.
df= df21.copy()

#normalizar todos los datos.
df.loc[df["MainBranch"] == "None of these", "MainBranch"] = "Other"

df= df.groupby(['MainBranch',],as_index=False).size()

#el % = valor*100 / total
df['porcentaje'] = 100 *df['size']/ df['size'].sum()


# Initialise the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport', #permite ser responsive en movil
                            'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}]
                )
server = app.server #heroku


# styling the sidebar

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 2rem",
    #,
    
}

FOOTER_STYLE = {
    "margin-left": "0rem",
    "margin-right": "0rem",
    "margin-bottom": "0rem",
    "margin-top": "0rem",
    #"padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    
    #"width": "calc(100% - 2rem)",
    #"fluid": "True",
}

app.layout = html.Div([
    dbc.Navbar([
        
        dbc.Row([ #logo
            dbc.Col(html.Img(src="https://appharbor.com/assets/images/stackoverflow-logo.png", 
                             height="35px",className='text-end ms-5')),
            dbc.Col(dbc.NavbarBrand("Dashboard", className='text-start')),
         #logo
        
            dbc.Col([ #col
                dbc.DropdownMenu(
                    children=[
                        #IMP: para navegar en la misma pagina: 
            #1: crear etiquetas id en los html (como si se fuesen a unar en el callback.)
            #2. en el navbar, anyadir # delante del href pare referenciar esa id.
            #3. poner la etiqueta de external_link=true en el navbar para que funcione en la misma pg
        
                        dbc.DropdownMenuItem("Titulo 1", href="#uno", external_link=True),
                        dbc.DropdownMenuItem("Titulo 2", href="#dos", external_link=True),
                    ],
                    nav=True,
                    in_navbar=True,
                    label="Menu",
                    className="position-absolute top-0 end-0",
                ) #dropdown
            ]) #col
        ])

        ], #logo
        sticky="top",
    ), 
        
    
    #colores de fuente: docs: https://dash-bootstrap-components.opensource.faculty.ai/docs/components/alert/
        #text-primary: azul
        #text-secondary: gris
        #text-warning: amarillo 
        #text-success: verde
        #text-info: azul claro
        #imp: estos colores solo son validos para el tema bootstrap. Cian tiene otro esquema, ver docs

    dbc.Row([ #contenido
    
        dbc.Row([
            dbc.Col(html.H1("Titulo 1", id = "uno", className="text-center"))
            
        ], justify="center",
        style={'color': 'LightBlue'},
        ), #cabecero

        dbc.Row([
            dbc.Col([

                html.H2('Age - histogram'), 
                html.P('Different age groups and their recurrence'),
                dcc.Graph(id='primero', figure={}),

                    ]#, xs=5, sm=6, md=7, lg=8, xl=10
            )


        ], justify="center"
        ), #primer grafico

        dbc.Row([
            dbc.Col([
                dcc.Dropdown(id="select_opt",  multi=False, value='2021',
                             options=[ #el usuario va a ver las label.
                    {"label": "2021", "value": 2021},
                    {"label": "2020", "value": 2020}],
                            ),
            ]#, xs=5, sm=6, md=7, lg=8, xl=10

            )
        ]), #dropdown. Eliminar

        dbc.Row([
            dbc.Col([
                html.H2('Main Branch - Pie chart'), 
                html.P('Correlation between with software development and stackoverflow users'),
                dcc.Graph(id='segundo', figure={})


            ]#, xs=5, sm=6, md=7, lg=8, xl=10
            )

        ], justify="center"

        ), #segundo grafico


        dbc.Row([
            dbc.Col([
                html.H2('Main Branch - Bar char'), 
                html.P('Correlation between with software development and stackoverflow users.'),
                dcc.Graph(id='tercero', figure={})
            ]#, xs=5, sm=6, md=7, lg=8, xl=10
               #, brand_href="uno",
            )
        ], justify="center",
            
        ), #tercer grafico.
        
        #nuevo titulo
        dbc.Row([
            dbc.Col(html.H1("Titulo dos", id = "dos", className="text-center"))
        ], justify="center",
        style={'color': 'LightBlue'},
        ), #titulo
        
        
        dbc.Row([
            dbc.Col([
                html.H2('Nuevo grafico aqui'), 
                html.P('Correlation between with software development and stackoverflow users.'),
                #dcc.Graph(id='tercero', figure={})
            ]#, xs=5, sm=6, md=7, lg=8, xl=10
               #, brand_href="uno",
            )
        ], justify="center",
            
        ), #tercer grafico.

    ],style=CONTENT_STYLE,
        

    #fluid=True # que el grafico se ajuste al ancho pg

    ), #contenido

    dbc.Row([ #footer
        
        dbc.Col([ #Texto
            dbc.Col(html.H4("Info", className="text-center mb-4 d-none d-lg-block")), #mb: margin bottom
            dbc.Col(html.P("Stackoverflow survey data has been used to create this dashboard.", 
                           className="ms-5 me-5 d-none d-lg-block")),
              #Para realizar este dashboard se han usado los datos de encuestas de Stackoverflow.
              # To create this dashboard, data from Stackoverflow surveys have been used. 
        ],className= "border-end",
            #"d-flex justify-content-center justify-content-lg-between p-4 border-bottom",
        ), #sociales
        
        
        dbc.Col([ # hecho con #ms: margin start, para que quede bonito 
            dbc.Col(html.H4("Made with ", className="text-start mb-4 ms-5 d-none d-lg-block")),
            html.A(#className='text-center text-primary mb-4'
                dbc.Col(html.P("Dash", className='text-start text-secondary ms-5')),
                # dbc.Col(html.Img(src="https://logonoid.com/images/stack-overflow-logo.png", height="30px")),
             href="https://dash.plotly.com/",
            style={"textDecoration": "none"},
            ), #link github
            html.A(#className='text-center text-primary mb-4'
                dbc.Col(html.P("Heroku", className='text-start text-secondary ms-5')),
                # dbc.Col(html.Img(src="https://logonoid.com/images/stack-overflow-logo.png", height="30px")),
             href="https://devcenter.heroku.com/categories/reference",
            style={"textDecoration": "none"},               
            ), #link heroku
              
        ]#,className="d-flex justify-content-center justify-content-lg-between p-4 border-bottom",
        ), # Hecho con
        
        
        dbc.Col([ # links
            dbc.Col(html.H4("Interesting links",className="text-start mb-4 ms-5 d-none d-lg-block")),
            #
            html.A(#className='text-center text-primary mb-4'
                dbc.Col(html.P("Stackoverflow dashboard 2021", className='text-start text-secondary ms-5')),
             href="https://insights.stackoverflow.com/survey/2021",
            style={"textDecoration": "none"},               
            ), #link stack
            html.A(#className='text-center text-primary mb-4'
                dbc.Col(html.P("Stackoverflow survey", className='text-start text-secondary ms-5')),
                # dbc.Col(html.Img(src="https://logonoid.com/images/stack-overflow-logo.png", height="30px")),
             href="https://insights.stackoverflow.com/survey?_ga=2.189292843.1285052511.1645528337-438523718.1645528337",
            style={"textDecoration": "none"},               
            ), #link stack
            
            
        ]), #links
    
        
        #colores de fuente: docs: https://dash-bootstrap-components.opensource.faculty.ai/docs/components/alert/
        #text-primary: azul
        #text-secondary: gris
        #text-warning: amarillo
        #text-success: verde
        #text-info: azul claro
        #imp: estos colores solo son validos para el tema bootstrap. Cian tiene otro esquema, ver docs
    
        dbc.Col([ #sociales
            dbc.Col(html.H4("Contact ", className="text-start mb-5 ms-5 d-none d-lg-block")),
            html.A(#className='text-center text-primary mb-4'
                dbc.Col(html.P("Github", className='text-start text-secondary ms-5')),
                # dbc.Col(html.Img(src="https://logonoid.com/images/stack-overflow-logo.png", height="30px")),
             href="https://github.com/albarrom",
            style={"textDecoration": "none"},               
            ), #link github
        
              
        ]#,className="d-flex justify-content-center justify-content-lg-between p-4 border-bottom",
        ), #sociales
        
        html.Hr(), #barra decorativa
        
        dbc.Row([ # ultima linea
            dbc.Col(html.P("2022 TFG - GII_O_MA_21.05", className="text-center")),
        ])#c ultima linea
    
    ], className="text-secondary", # hacer el texto gris
        style=FOOTER_STYLE,
    )#footer
    
]) #layout



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
