# # 1. importar librerias necesarias

import pandas as pd
import numpy as np 

import plotly.express as px 
from plotly.subplots import make_subplots

import dash
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc #bootstrap


# # 2. Importar los dataframe que van a analizarse

#crear un dataframe con toda la informacion de la encuesta
df21 = pd.read_csv('data/survey_results_public2021.csv', index_col = [0]) # El indice sera la columna con el ID de la respuesta

#crear un dataframe con toda la informacion de la encuesta
df20 = pd.read_csv ('data/survey_results_public2020.csv', index_col = [0]) # El indice sera la columna con el ID de la respuesta


# # 3. Funciones auxiliares: 

#crear un dataframe con toda la informacion de la encuesta
#crear un dataframe con toda la informacion de la encuesta
#crear un nuevo df copiando solo la columna Age1stCode
df1 = df21[['Age1stCode']]

#normalizar todos los datos.
df1 = df1[df1['Age1stCode'].notna()] #eliminar los nulos

#Cambiar nombre valores de columna
df1.loc[df1["Age1stCode"] == "Younger than 5 years", "Age1stCode"] = "04 - 04 years" #ya hay un 05 anyos en el df. 
df1.loc[df1["Age1stCode"] == "Older than 64 years", "Age1stCode"] = "65 - 65 years" #ya hay un 05 anyos en el df. 
df1.loc[df1["Age1stCode"] == "5 - 10 years", "Age1stCode"] = "05 - 10 years"

df2= df1.groupby(['Age1stCode',],as_index=False).size() #agrupar el nuevo df por edad1stcode

df2.columns = ["RangoEdad", "Count1st"] #renombrar columnas


#Crear una funcion que extraiga columnas del df ya procesadas. La funcion podra procesar 
#las columnas Age1stCode y YearsCode del año 2020 y tan solo YearsCode del año 2021
def getRangeAge (dataframe, nombre_columna, nueva_columna):
    
    df= dataframe[[nombre_columna]]

    df = df[df[nombre_columna].notna()] #eliminar los nulos

    #para que no sea una columna string
    df.loc[df[nombre_columna] == "Less than 1 year", nombre_columna] = "0" #no hay 0 
    
    if "Older than 85" in df.values:
        df.loc[df[nombre_columna] == "Younger than 5 years", nombre_columna] = 4
        df.loc[df[nombre_columna] == "Older than 85", nombre_columna] = 86 #ya hay un 05 anyos en el df. 
        bins = [1, 5, 10, 18, 25, 35, 45, 55, 65, 75, 85, 86]
        
    else: 
        #Eliminar valores que no van a poder compararse correctamente
        df = df.drop(df[df[nombre_columna] == "More than 50 years"].index)
        bins = [1, 5, 10, 18, 25, 35, 45, 55]
        
    df[nombre_columna] = df[nombre_columna].astype(int) # toda la columna es enteros
    
    #crear nuevo df con los valores ordenados
    df1 = pd.DataFrame(df[nombre_columna].value_counts(bins= bins, sort=False).reset_index().values, 
                       columns=[nueva_columna, "Count"+nueva_columna]) #renombrar las nuevas columnas

    
    return df1

#2021
df3 = getRangeAge(df21,"YearsCode","Pro")
df2021 = pd.concat([df2, df3["CountPro"]], axis =1)

df2021.loc[df2021["RangoEdad"] == "04 - 04 years", "RangoEdad"] = "Younger than 5 years" #ya hay un 05 anyos en el df. 
df2021.loc[df2021["RangoEdad"] == "65 - 65 years", "RangoEdad"] = "Older than 64 years" #ya hay un 05 anyos en el df. 
df2021.fillna(0, inplace=True) #convertir los nan a 0 (ayudara con el grafico)

#2020
dfPro = getRangeAge(df20,"YearsCode","Pro")
df1st = getRangeAge(df20,"Age1stCode","s1st")

df1st["s1st"] = ["Younger than 5 years",
                 "05 - 10 years",
                 "11 - 17 years",
                 "18 - 24 years",
                 "25 - 34 years",
                 "35 - 44 years",
                 "45 - 54 years",
                 "55 - 64 years",
                 "65 - 74 years",
                 "75 - 84 years",
                 "Older than 84 years"]

df2020 = pd.concat([df1st, dfPro["CountPro"]], axis =1)
df2020.fillna(0, inplace=True) #convertir los nan a 0 (ayudara con el grafico)

def branchGraph (df):
    
    #normalizar todos los datos.
    df.loc[df["MainBranch"] == "None of these", "MainBranch"] = "Other"

    df= df.groupby(['MainBranch',],as_index=False).size()

    #el % = valor*100 / total
    #df['porcentaje'] = 100 *df['size']/ df['size'].sum()

    return df


def branchEmploymentEd (df):
    
    #normalizar todos los datos/eliminar valores que no aportan nada
    df.drop(df.index[df['MainBranch'] == "None of these"], inplace=True) 
    df.drop(df.index[df['Employment'] == "I prefer not to say"], inplace=True) 
    df.drop(df.index[df['EdLevel'] == "Something else"], inplace=True) 

    #eliminar los nan
    df.dropna(subset = ['EdLevel','MainBranch','Employment'])
    
    #modificar el df para que sea mejor visualmente:
    df['EdLevel'] = df['EdLevel'].str.replace(r"\(.*?\)", "", regex=True) #eliminar parentesis en educacion
    

    #generar nuevo df agrupado por las 3 columnas procesadas
    df= df.groupby(['MainBranch','Employment','EdLevel',],as_index=False).size()
    return df


# # 4. Layout


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
    
    #---------------- NAVBAR ------------
    
    dbc.Navbar([
        
        dbc.Row([ #logo
            dbc.Col(html.Img(src="https://appharbor.com/assets/images/stackoverflow-logo.png", 
                             height="35px",className='text-end ms-5')),
            dbc.Col(dbc.NavbarBrand("Dashboard", className='text-start')),
         #logo
        
            dbc.Col([ #col: dropdown al final de la fila
                dbc.DropdownMenu(
                    children=[
                        #IMP: para navegar en la misma pagina: 
            #1: crear etiquetas id en los html (como si se fuesen a unar en el callback.)
            #2. en el navbar, anyadir # delante del href pare referenciar esa id.
            #3. poner la etiqueta de external_link=true en el navbar para que funcione en la misma pg
        
                        dbc.DropdownMenuItem("Developer Profile", href="#uno", external_link=True),
                        dbc.DropdownMenuItem("Technology", href="#dos", external_link=True),
                        dbc.DropdownMenuItem("next title", href="#tres", external_link=True),
                    ],
                    nav=True,
                    in_navbar=True,
                    label="Index",
                    className="position-absolute top-0 end-0",
                ) #dropdown
            ]) #col
        ])#logo

        ], #navbar
        sticky="top", #para que se quede siempre arriba, aun haciendo scroll
    ), #fin navbar
        
    
    #colores de fuente: docs: https://dash-bootstrap-components.opensource.faculty.ai/docs/components/alert/
        #text-primary: azul
        #text-secondary: gris
        #text-warning: amarillo 
        #text-success: verde
        #text-info: azul claro
        #imp: estos colores solo son validos para el tema bootstrap. Cian tiene otro esquema, ver docs

    #---------------- CUERPO -----------
    
    dbc.Row([ #contenido
    
        dbc.Row([ #primer enlace a navbar
            dbc.Col(html.H1("Developer Profile", id = "uno", className="text-center"))
            
        ], justify="center",
        style={'color': 'LightBlue'},
        ), #cabecero

        
#         #dropdown que no sirve para nada. Comprobar antes de eliminar.
#         dbc.Row([ #dropdown para el primer grafico
#             dbc.Col([
#                 dcc.Dropdown(id="select_opt",  multi=False, value='2021',
#                              options=[ #el usuario va a ver las label.
#                     {"label": "2021", "value": 2021},
#                     {"label": "2020", "value": 2020}],
#                             ),
#             ]#, xs=5, sm=6, md=7, lg=8, xl=10

#             )
#         ]), #dropdown. 
        
        ## PRIMER GRAFICO
        dbc.Row([
            dbc.Col([

                html.H2('Double bar diagram'), 
                html.P('Comparison of different periods of development.'),
                dbc.Row([ #dropdown para el primer grafico
                    dbc.Col([
                        dcc.Dropdown(id="opt1",  multi=False, value='2021',
                                 options=[ #el usuario va a ver las label.
                                     {"label": "2021", "value": 2021},
                                     {"label": "2020", "value": 2020}],
                                    ),
                    ]#, xs=5, sm=6, md=7, lg=8, xl=10
                    ) 
                ]), #dropdown
                
                dcc.Graph(id='primero', figure={}),
            ]#, xs=5, sm=6, md=7, lg=8, xl=10
            )


        ], justify="center"
        ), #primer grafico

        
        ## SEGUNDO GRAFICO
        dbc.Row([
            dbc.Col([
                html.H2('Pie chart'), 
                html.P('Correlation between with software development and stackoverflow users'),
                dbc.Row([ #dropdown para el primer grafico
                    dbc.Col([
                        dcc.Dropdown(id="opt2",  multi=False, value='2021',
                                 options=[ #el usuario va a ver las label.
                                     {"label": "2021", "value": 2021},
                                     {"label": "2020", "value": 2020}],
                                    ),
                    ]#, xs=5, sm=6, md=7, lg=8, xl=10
                    ) 
                ]), #dropdown
                
                dcc.Graph(id='segundo', figure={}),
            ]#, xs=5, sm=6, md=7, lg=8, xl=10
            )

        ], justify="center"

        ), #segundo grafico

        
        ## TERCER GRAFICO: sunburst
        dbc.Row([
            dbc.Col([
                html.H2('Sunburst'), 
                html.P('Correlation between Education level, employment and main branch.'),
                dbc.Row([ #dropdown para el primer grafico
                    dbc.Col([
                        dcc.Dropdown(id="opt3",  multi=False, value='2021',
                                 options=[ #el usuario va a ver las label.
                                     {"label": "2021", "value": 2021},
                                     {"label": "2020", "value": 2020}],
                                    ),#dropdown
                    ]#, xs=5, sm=6, md=7, lg=8, xl=10
                    )#col 
                ]), #dropdown
                
                dcc.Graph(id='tercero', figure={}),
                
                #nota al pie del grafico
                html.Small('there is more than one level of depth. Click on the outer parts of the graph!'),

            ]#, xs=5, sm=6, md=7, lg=8, xl=10
            )

        ], justify="center"

        ), #tercer grafico
        
        
        ####################### Titulo: TECHNOLOGY ####################
        dbc.Row([
            dbc.Col(html.H1("Technology", id = "dos", className="text-center")) #titulo navbar
        ], justify="center",
        style={'color': 'LightBlue'},
        ), #titulo
        
        
        dbc.Row([ 
            dbc.Col([
                html.H2('Bar charts with Long Format Data'), 
                html.P('Loved Vs Dreaded.'),
                #dcc.Graph(id='tercero', figure={})
            ]#, xs=5, sm=6, md=7, lg=8, xl=10
               #, brand_href="uno",
            )
        ], justify="center",
            
        ), #grafico.
        
        
        ################ Nuevo titulo ############
        #nuevo titulo 
#         dbc.Row([
#             dbc.Col(html.H1("Tercer titulo", id = "tres", className="text-center")) #esto va al navbar
#         ], justify="center",
#         style={'color': 'LightBlue'},
#         ), #titulo
        
        
#         dbc.Row([ # este es el grafico
#             dbc.Col([
#                 html.H2('Nuevo grafico aqui'), 
#                 html.P('Description.'),
#                 #dcc.Graph(id='tercero', figure={})
#             ]#, xs=5, sm=6, md=7, lg=8, xl=10
#                #, brand_href="uno",
#             )
#         ], justify="center",
            
#         ), #grafico.

    ],style=CONTENT_STYLE,
        

    #fluid=True # que el grafico se ajuste al ancho pg

    ), #contenido
    
#---------------- FOOTER-----------
    
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


# # 5. Callback


#diagrama de barras dobles
@app.callback(
    Output(component_id='primero', component_property='figure'),
    Input(component_id='opt1', component_property='value'))
def update_graph(opt1):
    
    fig=make_subplots(specs=[[{"secondary_y":True}]])
    
    if (opt1 == 2020): 
        fig.add_trace(go.Bar(x= df2020["Counts1st"], y= df2020["s1st"], name = "total",
                             orientation = "h", # orientacion "h"/"v"
                             text = df2020["Counts1st"],), secondary_y=True,)
        fig.add_trace(go.Bar(x= df2020["CountPro"], y= df2020["s1st"], name = "professionally",
                             orientation = "h", text = df2020["CountPro"],), secondary_y=True,)

        fig.update_yaxes(autorange="reversed") # reverir el eje y (less than 5 years arriba)
        #fig.update_layout(yaxis={"mirror" : "allticks", 'side': 'left'}) # poner a la izda el eje y

    else: #grafico 2021, vertical
        fig.add_trace(go.Bar(x= df2021["RangoEdad"], y= df2021["Count1st"], 
                             text = df2021["Count1st"], name = "total"), secondary_y=True,)
        fig.add_trace(go.Bar(x= df2021["RangoEdad"], y= df2021["CountPro"],
                             text = df2020["CountPro"], name = "professionally"), secondary_y=True,)

    #nombre de los ejes
    fig.update_yaxes(title_text="Age Range")
    fig.update_yaxes(title_text="# Responses")
    #fig.update_layout(xaxis={"mirror" : "allticks", 'side': 'top'}, yaxis={"mirror" : "allticks", 'side': 'right'})
    
      
    fig.update_layout(title_text="Total of years coding Vs years coding professionally")
    
    #quitar color y grid del grafico
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',}) #fondo transparente
    fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False)) #eliminar grid

    return fig
#fin callback diagrama de barras dobles. 


@app.callback( #diagrama de quesito
    Output(component_id='segundo', component_property='figure'),
    Input(component_id='opt2', component_property='value'))
def update_graph(opt2):
    if (opt2 == 2020): 
        df = branchGraph(df20)
        fig=px.pie( df, names=df['MainBranch'], values = df['size'],hole=.3,)
        fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',})
    else:
        df = branchGraph(df21)
        fig=px.pie(df, names=df['MainBranch'], values = df['size'],hole=.3,)
        fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',})
    
    return fig


@app.callback( #sunburst
    Output(component_id='tercero', component_property='figure'),
    Input(component_id='opt3', component_property='value'))
def update_graph(opt4):
    
    if (opt4 == 2020):
        df=branchEmploymentEd (df20)
        fig = px.sunburst(df, path=['MainBranch', 'Employment', 'EdLevel',], 
                          values='size', maxdepth = 2,)
    else:
        df = branchEmploymentEd (df21)
        fig = px.sunburst(df, path=['MainBranch', 'Employment', 'EdLevel',], 
                          values='size', maxdepth = 2,)
    

    #esconder las etiquetas que son demasiado grandes para entrar en el hueco del grafico
    fig.update_layout(uniformtext=dict(minsize=9, mode='hide'))
    
    fig.update_layout(title_text="Education level - employment - main branch", font_size=12)
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',})              
    fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
    return fig


# # 6. Run

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)




