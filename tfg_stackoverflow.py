#!/usr/bin/env python
# coding: utf-8

# # 1. importar librerias necesarias

# In[1]:


import pandas as pd
import numpy as np 

#tabs
from collections import Counter
from itertools import chain


import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import dash
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc #bootstrap

# dict con las abreviaturas de los estados de us (grafico mapa)
from abbr import us_state_to_abbrev 


# # 2. Importar los dataframe que van a analizarse

# In[2]:


#crear un dataframe con toda la informacion de la encuesta
df21 = pd.read_csv('data/survey_results_public2021.csv', index_col = [0]) # El indice sera la columna con el ID de la respuesta

#crear un dataframe con toda la informacion de la encuesta
df20 = pd.read_csv ('data/survey_results_public2020.csv', index_col = [0]) # El indice sera la columna con el ID de la respuesta


# # 3. Funciones auxiliares: 

# In[3]:


def ageCodePro (df, numero):
    
    df1=df[['Age','YearsCode','YearsCodePro']].dropna().copy()

    #eliminar valores que no aportan informacion
    df1.drop(df1[df1['YearsCode'].isin(["Less than 1 year", "More than 50 years"])].index, inplace=True) 
    df1.drop(df1[df1['YearsCodePro'].isin(["Less than 1 year", "More than 50 years"])].index, inplace=True) 
    df1.drop(df1[df1['Age'].isin(["Prefer not to say"])].index, inplace=True) 

    #convertir columnas a entero
    df1['YearsCode'] = pd.to_numeric(df1['YearsCode'])
    df1['YearsCodePro'] = pd.to_numeric(df1['YearsCodePro'])
    
    if (numero == 20): #si es el dataframe del anyo 2020, se lidiara con rangos:
        # etiquetas para la nueva columna
        labels = ["Under 18 years old", "18 - 24 years", "25 - 34 years",
                   "35 - 44 years", "45 - 54 years", "55 - 64 years", "65 - 74 years", "75 - 84 years", "Older than 84 years"]
        bins = [10, 17, 24, 34, 44, 54, 64, 74, 84, 100] # divisiones de rango
        
        #eliminar valores de edad extremos.
        df1.drop(df1[(df1.Age < 10) | (df1.Age > 100)].index, inplace=True)
        
        #crear una nueva columna usando las etiquetas
        df1['Rango'] = pd.cut(df1['Age'], bins= bins, labels=labels)
        
        #nuevo df agrupado por la nueva columna.
        df2 = df1.groupby('Rango', as_index = False).agg(median_code=('YearsCode', 'median'), 
                      median_pro=('YearsCodePro','median'), #nueva columna que calculara la medina de yearscodepro
                      # contar el numero de respuestas por edad (no se usa en el grafico de momento)                                                                                    
                     respuestas=('Age','count'))
    
    elif (numero == 21): #df del año 2021
        
        #agrupar por edad
        df2 = df1.groupby('Age', as_index = False).agg(median_code=('YearsCode', 'median'), 
                         median_pro=('YearsCodePro','median'), #nueva columna que calculara la medina de yearscodepro
                         # contar el numero de respuestas por edad   (no se usa en el grafico de momento)                                                                                   
                         respuestas=('Age','count')) 

    return df2


# In[4]:


def branchGraph (df):
    
    #normalizar todos los datos.
    df.loc[df["MainBranch"] == "None of these", "MainBranch"] = "Other"

    df= df.groupby(['MainBranch',],as_index=False).size()

    return df


# In[5]:


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


# In[6]:


# copiamos elementos que no sean NaN


def loveHateWant (df, columna1, columna2):
    #copiar solo las columnas que nos interesan. 
    #IMP: eliminar todos los elementos NaN. Se obtendra un nuevo df sin ningún Nan en ninguna columna.
    df2=df[[columna1, columna2]].dropna().copy() 
    
    df3=pd.DataFrame()

    #en el df vacio se crearan 3 columnas. Se evaluara por filas.
    #columna love sera la interseccion de columna1 y columna 2. (solo elementos que esten en ambas col)
    df3['love'] = [set(x[0].split(';')) & set(x[1].split(';')) for x in df2.values]
    
    #columna hate sera la diferencia entre columna1 y columna 2. (solo elementos en col1)
    df3['hate'] = [set(x[0].split(';')) - set(x[1].split(';')) for x in df2.values]
    
    #want sera la diferencia entre columna 2 y columna 1. (solo elementos en col2)
    df3['want'] = [set(x[1].split(';')) - set(x[0].split(';')) for x in df2.values] 

    #dataframe que cuenta cada elemento en las columnas
    df_counts = (pd.DataFrame([Counter(chain.from_iterable(df3[column]))
                    for column in df3.columns],
                    index=['love', 'hate', 'want'])
                    .fillna(0)
                    .T
                    .sort_index()
                )

    
    return df_counts


# In[7]:


def mundoMapa (dataframe):
    #copiar columnas que interesan
    df = dataframe[['Country']].dropna().copy()
    df2 = pd.DataFrame()
    #contar el numero de paises
    df2["count"]=df['Country'].value_counts()
    
    return df2

def usMapa(dataframe):
    df = dataframe[['US_State',]].dropna().copy()
    df = df.drop(df[df.US_State == "I do not reside in the United States"].index)
    df2 = pd.DataFrame()
            #contar el numero de paises
    df2["count"]=df['US_State'].value_counts()
    df2["state"]=df2.index

        #sustituir el nombre del pais con la abreviatura (us_state_to_abbrev=dict)
    df2['state'] = df2["state"].replace(us_state_to_abbrev, regex=True)

    return df2


# In[8]:


def salario (df,anyo):
    
    #para poder reutilizar la columna en el df de 2021 y 2020 sin hacer grandes cambios, hay que renombrar ConvertedComp
    df.rename(columns = {'ConvertedComp':'ConvertedCompYearly'}, inplace = True)
    
    #copia de df y se eliminan todas las columnas que tengan nan: 
    #Solo se seleccionan filas completas y se descartan las demas
    df4=df[['DevType','ConvertedCompYearly', 'YearsCodePro','Age1stCode']].dropna().copy()
    
    if (anyo == 21): #Age1stCode en el df del 2021 son string en lugar de enteros.
        #crear diccionario con los cambios de valores
        edadesTransformadas = {"Younger than 5 years" : 4, "5 - 10 years" : 7, "11 - 17 years": 18, "18 - 24 years" : 21,
        "25 - 34 years" : 30, "35 - 44 years" : 40, "45 - 54 years": 50, "55 - 64 years" : 60, 
        "Older than 64 years": 70}
        
        #cambiar los valores.
        df4=df4.replace({"Age1stCode": edadesTransformadas})
    
    #resto es igual para ambos df.
    
    # eliminar filas en anyos que tengan texto. 
    df4.drop(df4[df4['YearsCodePro'] == "Less than 1 year"].index, inplace = True) 
    df4.drop(df4[df4['YearsCodePro'] == "More than 50 years"].index, inplace = True)
    
    df4.drop(df4[df4['Age1stCode'] == "Younger than 5 years"].index, inplace = True) 
    df4.drop(df4[df4['Age1stCode'] == "Older than 85"].index, inplace = True)
    
    #convertir columnas a entero
    df4["Age1stCode"] = pd.to_numeric(df4["Age1stCode"])
    df4["YearsCodePro"] = pd.to_numeric(df4["YearsCodePro"])
    
    #separar filas con mas de un devtype y despues agruparlas
    df4=df4.assign(DevType=df4['DevType'].str.split(';')).explode('DevType').groupby('DevType').agg(avg_pro=('YearsCodePro', 'mean'), #nueva columna que calculara la media de yearscodepro
                 avg_age=('Age1stCode','mean'), 
                 median_money=('ConvertedCompYearly','median'), #nueva columna con mediana del salario
                 # contar los diferentes tipos de devtype                                                                                    
                 respuestas=('DevType','count')).reset_index() #reiniciar el indice

    #eliminar informacion irrelevante
    df4.drop(df4.index[df4['DevType'] == "Other (please specify):"], inplace=True)
    
    return df4


# In[9]:


# def ageDev (df):
# esto era elsunburst 
#     # copiamos elementos que no sean NaN
#     df2=df[['Age', 'DevType']].dropna().copy() 

#     # Lista de devs
#     leng=[]
#     for l in df2['DevType'].apply(lambda x: x.split(';')):
#         leng=np.unique(np.append(leng, l))

#     # Lista de edades
#     edades=list(df2['Age'].unique())
#     edades.remove('Prefer not to say') # Eliminamos esta categoría son información relevante


#     # Enlaces edades-lenguajes
#     enlaces=list()
#     for e in edades:
#         i1=df2[df2['Age'].str.contains(e)].index
#         for l in leng:
#             i2=df2[df2['DevType'].str.contains(l)].index
#             enlaces.append((e,l,np.intersect1d(i1,i2).shape[0]))

#     return pd.DataFrame(enlaces,columns=['a1','a2','n'])


# In[10]:


def ageTech (df3,col):

    # copiamos elementos que no sean NaN
    df=df3[['Age1stCode', col]].dropna().copy() 
    df2 = df.drop(df[df.Age1stCode == 'Prefer not to say'].index) #eliminar info irrelevante

    df2 = (df.explode(df.columns.tolist())
      .apply(lambda col: col.str.split(';')) 
      .explode('Age1stCode')
      .explode(col))


    return (pd.crosstab(df2['Age1stCode'], df2[col])
       .melt(value_name='count', ignore_index=False)
       .reset_index())


# In[11]:


def edTech (df3,col):

    # copiamos elementos que no sean NaN
    df=df3[['EdLevel', col]].dropna().copy() 
    
    #eliminar info irrelevante
    df.drop(df[df.EdLevel == 'Something else'].index, inplace = True) 

    df2 = (df.explode(df.columns.tolist())
      .apply(lambda col: col.str.split(';')) 
      .explode('EdLevel')
      .explode(col))


    df4= (pd.crosstab(df2['EdLevel'], df2[col])
       .melt(value_name='count', ignore_index=False)
       .reset_index())
    
    #eliminar parentesis en educacion
    df4['EdLevel'] = df4['EdLevel'].str.replace(r"\(.*?\)", "", regex=True) 
    
    # Seleccionar solo un top 5 de tecnologias (lenguajes, bases de datos...)
    top=df4[[col,'count']].groupby(col).sum().sort_values(by='count',ascending=False).index[:5]
    return df4[df4[col].isin(top.tolist())]

def etiquetas (df, col):

    edLabels = list(df.EdLevel.unique())
    colLabels = list(df[col].unique())

    labels = edLabels + colLabels

    return labels


# # 4. Layout

# In[12]:


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
                        dbc.DropdownMenuItem("Work", href="#tres", external_link=True),
                        #dbc.DropdownMenuItem("Nuevo titulo", href="#cuatro", external_link=True),
                    ],
                    nav=True,
                    in_navbar=True,
                    label="Index",
                    className="position-absolute top-0 end-0",
                    align_end=True, # menu no mas grande que la pagina
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
                                     style={'width': '45vh'},
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
                                     style={'width': '45vh'},
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
                                     style={'width': '45vh'},
                                     #className="p-2 bg-secondary",
                                    ),#dropdown
                    ]#, xs=5, sm=6, md=7, lg=8, xl=10
                    )#col 
                ]), #dropdown
                html.Small('there are more than one level of depth. Click on the outer parts of the graph!'),
                dcc.Graph(id='tercero', figure={}),

            ]#, xs=5, sm=6, md=7, lg=8, xl=10
            )

        ], justify="center"

        ), #tercer grafico
        
        # # cuatro grafico 
        dbc.Row([
            html.H2('Scatter_geo'), 
            html.P("Map with users' origin."),
            dbc.Tabs([
                dbc.Tab(label='US only', tab_id='us_only', labelClassName="text-primary font-weight-bold", activeLabelClassName="text-info"), 
                dbc.Tab(label='World', tab_id='world',labelClassName="text-primary font-weight-bold", activeLabelClassName="text-info"),
                ],
                id="tab",
                active_tab="us_only",
            ),
        dbc.CardBody(html.P(id="mapa", className="card-text")),
        ]),
        
        
#         dbc.Row([ #sunburst
#             dbc.Col([
#                 html.H2('Sunburst'), 
#                 html.P('Correlation between age and dev type.'),
#                 dcc.Graph(id='age-dev', figure={}, style={'height': '80vh'}),

#             ]#, xs=5, sm=6, md=7, lg=8, xl=10
#             )

#         ], justify="center"

#         ),

        
        
        ####################### Titulo: TECHNOLOGY ####################
        dbc.Row([
            dbc.Col(html.H1("Technology", id = "dos", className="text-center")) #titulo navbar
        ], justify="center",
        style={'color': 'LightBlue'},
        ), #titulo
        
        # love hate (staked diagram) tech vs tech
        dbc.Row([
            html.H2('Stacked bar chart'), 
            html.P("Users' tech preferences"),
            dbc.Tabs([
                dbc.Tab(label='Databases', tab_id='db',labelClassName="text-primary font-weight-bold", activeLabelClassName="text-info"),
                dbc.Tab(label='Languages', tab_id='lang', labelClassName="text-primary font-weight-bold", activeLabelClassName="text-info"), 
                dbc.Tab(label='Platform', tab_id='plat', labelClassName="text-primary font-weight-bold", activeLabelClassName="text-info"), 
                dbc.Tab(label='webframe', tab_id='web', labelClassName="text-primary font-weight-bold", activeLabelClassName="text-info"), 
                dbc.Tab(label='Miscelaneous', tab_id='misc', labelClassName="text-primary font-weight-bold", activeLabelClassName="text-info"), 
                dbc.Tab(label='Tools', tab_id='tools', labelClassName="text-primary font-weight-bold", activeLabelClassName="text-info"), 
                dbc.Tab(label='Collab', tab_id='colab', labelClassName="text-primary font-weight-bold", activeLabelClassName="text-info"),
                ],
                id="tabs",
                active_tab="db",
            ),
        dbc.CardBody(html.P(id="tab-content", className="card-text")),
        ]),
        
        #treemap (cajitas) edad vs tech
        
        dbc.Row([
            html.H2('Treemap'), 
            html.P("Tech usage according to age where developer career started"),
            dbc.Tabs([
                dbc.Tab(label='Databases', tab_id='db1',labelClassName="text-primary font-weight-bold", activeLabelClassName="text-info"),
                dbc.Tab(label='Languages', tab_id='lang1', labelClassName="text-primary font-weight-bold", activeLabelClassName="text-info"), 
                dbc.Tab(label='Platform', tab_id='plat1', labelClassName="text-primary font-weight-bold", activeLabelClassName="text-info"), 
                dbc.Tab(label='webframe', tab_id='web1', labelClassName="text-primary font-weight-bold", activeLabelClassName="text-info"), 
                dbc.Tab(label='Miscelaneous', tab_id='misc1', labelClassName="text-primary font-weight-bold", activeLabelClassName="text-info"), 
                dbc.Tab(label='Tools', tab_id='tools1', labelClassName="text-primary font-weight-bold", activeLabelClassName="text-info"), 
                dbc.Tab(label='Collab', tab_id='colab1', labelClassName="text-primary font-weight-bold", activeLabelClassName="text-info"),
                ],
                id="treemap",
                active_tab="db1",
            ),
            dbc.CardBody(html.P(id="tablas-content", className="card-text")),
        ]
        ), #treemap (cajitas)
        
        #sankey (filas conectadas) ed level vs tech
        dbc.Row([ 
            dbc.Tabs([
                dbc.Tab(label='Databases', tab_id='db2',labelClassName="text-primary font-weight-bold", activeLabelClassName="text-info"),
                dbc.Tab(label='Languages', tab_id='lang2', labelClassName="text-primary font-weight-bold", activeLabelClassName="text-info"), 
                dbc.Tab(label='Platform', tab_id='plat2', labelClassName="text-primary font-weight-bold", activeLabelClassName="text-info"), 
                dbc.Tab(label='webframe', tab_id='web2', labelClassName="text-primary font-weight-bold", activeLabelClassName="text-info"), 
                dbc.Tab(label='Miscelaneous', tab_id='misc2', labelClassName="text-primary font-weight-bold", activeLabelClassName="text-info"), 
                dbc.Tab(label='Tools', tab_id='tools2', labelClassName="text-primary font-weight-bold", activeLabelClassName="text-info"), 
                dbc.Tab(label='Collab', tab_id='colab2', labelClassName="text-primary font-weight-bold", activeLabelClassName="text-info"),
                ],
                id="sankey",
                active_tab="db2",
            ),
        dbc.CardBody(html.P(id="tabu-content", className="card-text")),
        ]), #sankey
        
        
        ################ Nuevo titulo ############
        #nuevo titulo 
        dbc.Row([
            dbc.Col(html.H1("Work", id = "tres", className="text-center")) #esto va al navbar
        ], justify="center",
        style={'color': 'LightBlue'},
        ), #titulo
        
        
        dbc.Row([ # salarios
            dbc.Col([
                html.H2('Scatter plot'), 
                html.P('Correlation between Salary, type of developer and years coding profesionaly.'),
                dbc.Row([ #dropdown para el primer grafico
                    dbc.Col([
                        dcc.Dropdown(id="opt4",  multi=False, value='2021',
                                 options=[ #el usuario va a ver las label.
                                     {"label": "2021", "value": 2021},
                                     {"label": "2020", "value": 2020}],
                                     style={'width': '45vh'},
                                     #className="p-2 bg-secondary",
                                    ),#dropdown
                    ]#, xs=5, sm=6, md=7, lg=8, xl=10
                    )#col 
                ]), #dropdown
                dcc.Graph(id='salario', figure={}, style={'height': '80vh'}), 
            ]#, xs=5, sm=6, md=7, lg=8, xl=10
               #, brand_href="uno",
            )
        ], justify="center",
            
        ), # salarios.
        
        
        
#                 ## TERCER GRAFICO: sunburst
#         dbc.Row([
#             dbc.Col([
#                 html.H2('Sunburst'), 
#                 html.P('Correlation between Education level, employment and main branch.'),
#                 dbc.Row([ #dropdown para el primer grafico
#                     dbc.Col([
#                         dcc.Dropdown(id="opt3",  multi=False, value='2021',
#                                  options=[ #el usuario va a ver las label.
#                                      {"label": "2021", "value": 2021},
#                                      {"label": "2020", "value": 2020}],
#                                      style={'width': '45vh'},
#                                      #className="p-2 bg-secondary",
#                                     ),#dropdown
#                     ]#, xs=5, sm=6, md=7, lg=8, xl=10
#                     )#col 
#                 ]), #dropdown
                
#                 dcc.Graph(id='tercero', figure={}),

#             ]#, xs=5, sm=6, md=7, lg=8, xl=10
#             )

#         ], justify="center"

#         ), #tercer grafico
        
        
        
    
        
        ################ Nuevo titulo ############
        #nuevo titulo 
#         dbc.Row([
#             dbc.Col(html.H1("Cuarto titulo", id = "cuatro", className="text-center")) #esto va al navbar
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


# In[13]:


@app.callback(
    Output(component_id='primero', component_property='figure'),
    Input(component_id='opt1', component_property='value'))
def update_graph(opt1):

    #fig = go.FigureWidget() #grafico vacio. ####PRUEBA
    df = pd.DataFrame()
    
    if (opt1 == 2020):
        df = ageCodePro(df20,20)
        fig = px.bar(df, y="Rango", x= ["median_pro", "median_code"],
                orientation = "h", barmode = 'group', #barras horizontales y agrupadas
                 text_auto= True)
                #colorscale='viridis') #escala colores barras
    else:
        df = ageCodePro(df21,21)
        fig = px.bar(df, y="Age", x= ["median_pro", "median_code"],
                 orientation = "h", barmode = 'group',
                  text_auto= True)
        
    #poner el numero de la barra fuera de la barra y en posicion horizontal.
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig['layout']['yaxis']['autorange'] = "reversed" #valores en orden descendente
    
    #renombrar ejes
    fig.update_xaxes(title_text="# Years")
    fig.update_yaxes(title_text="Age")
    fig.update_layout(title_text="Age Vs total of years development")
    
    #quitar color y grid del grafico
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',}) #fondo transparente
    fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False)) #eliminar grid
   

    return fig


# In[14]:


@app.callback( #diagrama de quesito Revisar
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


# In[15]:


@app.callback( #sunburst. Revisar.
    Output(component_id='tercero', component_property='figure'),
    Input(component_id='opt3', component_property='value'))
def update_graph(opt3):
    
    if (opt3 == 2020):
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


# In[16]:


#tech vs tech. Revisar. 

@app.callback(
    Output("tab-content", "children"), 
    Input("tabs", "active_tab"))
    
def tab_content(active_tab):
    
    df = pd.DataFrame()
    
    if active_tab is not None: #para evitar un error hay que añadir un caso donde active_tab sste vacio
        if active_tab =="db":
            df = loveHateWant(df21, 'DatabaseHaveWorkedWith', 'DatabaseWantToWorkWith')
            fig = px.bar(df, 
                 x = [c for c in df.columns],
                 y = df.index,               
                 #template = 'plotly_dark',
                 color_discrete_sequence = px.colors.qualitative.T10, 
                 title = 'Love Vs Hate Vs Want: Databases',
                 orientation = 'h',
             )
            #nombre de ejes
            fig.update_yaxes(title_text="Databases")
            fig.update_xaxes(title_text="# Responses")
            
            #quitar color y grid del grafico
            fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',}) #fondo transparente
            fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False)) #eliminar grid
            
            return dcc.Graph(figure=fig, style={'height': '90vh'})
        elif active_tab == "lang":
            df = loveHateWant (df21, 'LanguageHaveWorkedWith', 'LanguageWantToWorkWith')
            fig = px.bar(df, 
                 x = [c for c in df.columns],
                 y = df.index,               
                 #template = 'plotly_dark',
                 color_discrete_sequence = px.colors.qualitative.T10, 
                 title = 'Love Vs Hate Vs Want: Languages',
                 orientation = 'h',
             )
            #nombre de ejes
            fig.update_yaxes(title_text="Languages")
            fig.update_xaxes(title_text="# Responses")
            
            #quitar color y grid del grafico
            fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',}) #fondo transparente
            fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False)) #eliminar grid
            
            return dcc.Graph(figure=fig, style={'height': '90vh'})
        elif active_tab == "plat":
            df = loveHateWant (df21, 'PlatformHaveWorkedWith', 'PlatformWantToWorkWith')
            fig = px.bar(df, 
                 x = [c for c in df.columns],
                 y = df.index,               
                 #template = 'plotly_dark',
                 color_discrete_sequence = px.colors.qualitative.T10, 
                 title = 'Love Vs Hate Vs Want: Platforms',
                 orientation = 'h',
             )
            #nombre de ejes
            fig.update_yaxes(title_text="Platforms")
            fig.update_xaxes(title_text="# Responses")
            
            #quitar color y grid del grafico
            fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',}) #fondo transparente
            fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False)) #eliminar grid
            
            return dcc.Graph(figure=fig, style={'height': '90vh'})
        
        elif active_tab == "web":
            df = loveHateWant (df21, 'WebframeHaveWorkedWith', 'WebframeWantToWorkWith')
            fig = px.bar(df, 
                 x = [c for c in df.columns],
                 y = df.index,               
                 #template = 'plotly_dark',
                 color_discrete_sequence = px.colors.qualitative.T10, 
                 title = 'Love Vs Hate Vs Want: Webframes',
                 orientation = 'h',
             )
            #nombre de ejes
            fig.update_yaxes(title_text="WebFrames")
            fig.update_xaxes(title_text="# Responses")
            
            #quitar color y grid del grafico
            fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',}) #fondo transparente
            fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False)) #eliminar grid
            
            return dcc.Graph(figure=fig, style={'height': '90vh'})
        elif active_tab == "misc":
            df = loveHateWant (df21, 'MiscTechHaveWorkedWith', 'MiscTechWantToWorkWith')
            fig = px.bar(df, 
                 x = [c for c in df.columns],
                 y = df.index,               
                 #template = 'plotly_dark',
                 color_discrete_sequence = px.colors.qualitative.T10, 
                 title = 'Love Vs Hate Vs Want: Miscelaneous Tech',
                 orientation = 'h',
             )
            #nombre de ejes
            fig.update_yaxes(title_text="Miscelaneous Tech")
            fig.update_xaxes(title_text="# Responses")
            
            #quitar color y grid del grafico
            fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',}) #fondo transparente
            fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False)) #eliminar grid
            
            return dcc.Graph(figure=fig, style={'height': '90vh'})
        elif active_tab == "tools":
            df = loveHateWant (df21, 'ToolsTechHaveWorkedWith', 'ToolsTechWantToWorkWith')
            fig = px.bar(df, 
                 x = [c for c in df.columns],
                 y = df.index,               
                 #template = 'plotly_dark',
                 color_discrete_sequence = px.colors.qualitative.T10, 
                 title = 'Love Vs Hate Vs Want: Tools',
                 orientation = 'h',
             )
            #nombre de ejes
            fig.update_yaxes(title_text="Languages")
            fig.update_xaxes(title_text="# Responses")
            
            #quitar color y grid del grafico
            fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',}) #fondo transparente
            fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False)) #eliminar grid
            
            return dcc.Graph(figure=fig)
        elif active_tab == "colab":
            df = loveHateWant (df21, 'NEWCollabToolsHaveWorkedWith', 'NEWCollabToolsWantToWorkWith')
            fig = px.bar(df, 
                 x = [c for c in df.columns],
                 y = df.index,               
                 #template = 'plotly_dark',
                 color_discrete_sequence = px.colors.qualitative.T10, 
                 title = 'Love Vs Hate Vs Want: Collab tools',
                 orientation = 'h',
             )
            #nombre de ejes
            fig.update_yaxes(title_text="Languages")
            fig.update_xaxes(title_text="# Responses")
            
            #quitar color y grid del grafico
            fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',}) #fondo transparente
            fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False)) #eliminar grid
            
            return dcc.Graph(figure=fig, style={'height': '90vh'}) 
        
        
    return html.P("This shouldn't ever be displayed...")


# In[17]:


#mundo/us

@app.callback(
    Output("mapa", "children"), 
    Input("tab", "active_tab"))
    
def tab_content2(active_tab):
    
    df = pd.DataFrame()
    
    if active_tab is not None: #para evitar un error hay que añadir un caso donde active_tab sste vacio
        if active_tab =="world":
            
            fig=px.scatter_geo(mundoMapa(df21), locationmode='country names',
                               locations=mundoMapa(df21).index,
                               size='count',color='count',
                               title = 'Users and their location',
                               color_continuous_scale=px.colors.cyclical.IceFire)
            
            #quitar color y grid del grafico
            fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',}) #fondo transparente
            fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False)) #eliminar grid
            
            return dcc.Graph(figure=fig, style={'height': '90vh'})
        elif active_tab == "us_only":
            
            fig=px.scatter_geo(usMapa(df21), locationmode='USA-states',locations=usMapa(df21).state,
                               size='count',color='count',
                               color_continuous_scale=px.colors.cyclical.IceFire)
            
            #hacer que el mapa se enfoque solo en us en vez de en todo el mundo
            fig.update_layout(title = 'Users and their location (US only)',
                              geo = dict(scope='usa',projection_type='albers usa',showland = True,
                                         landcolor = "rgb(250, 250, 250)",
                                         subunitcolor = "rgb(217, 217, 217)",
                                         countrycolor = "rgb(217, 217, 217)",
                                         countrywidth = 0.5,
                                         subunitwidth = 0.5
                                        ),
                             )
            
            #quitar color y grid del grafico
            fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',}) #fondo transparente
            fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False)) #eliminar grid
            
            return dcc.Graph(figure=fig, style={'height': '90vh'})
        
    return html.P("This shouldn't ever be displayed...")


# In[18]:


#salario 

@app.callback(
    Output(component_id='salario', component_property='figure'),
    Input(component_id='opt4', component_property='value'))
def update_graph(opt4):
    
    df = pd.DataFrame()
    anyo = 0

    if (opt4 == 2020): 
        df= df20 
        anyo = 20
    else: 
        df = df21 
        anyo = 21

    fig =  px.scatter(salario (df,anyo), x= "avg_pro", y= "avg_age", size="median_money", 
                      symbol="DevType", color="respuestas", hover_name="DevType")

    #quitar color y grid del grafico
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',}) #fondo transparente
    fig.update_layout(coloraxis_colorbar_x=-0.15) #mover el colorbar para que no tape el grafico
    
    return fig


# In[19]:



# @app.callback( #sunburst
#     Output(component_id='age-dev', component_property='figure'),
#     Input(component_id='opt4', component_property='value'))
# def update_graph(opt3):
    
#     enlaces=ageDev (df21)
    
#     top=enlaces[['a2','n']].groupby('a2').sum().sort_values(by='n',ascending=False).index[:10]
#     e2=enlaces[enlaces['a2'].isin(top.tolist())]
#     fig = px.sunburst(e2, path=['a1', 'a2'], values='n', )

#     #esconder las etiquetas que son demasiado grandes para entrar en el hueco del grafico
#     fig.update_layout(uniformtext=dict(minsize=10, mode='hide'))
    
#     fig.update_layout(title_text="Age Vs Dev type", font_size=12)
#     fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',})              
#     fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
#     return fig


# In[20]:


@app.callback(
    Output("tablas-content", "children"), 
    Input("treemap", "active_tab"))
    
def treemap(active_tab): #edad vs tech
    
    #df = pd.DataFrame()
    nameColumns= ['DatabaseHaveWorkedWith','LanguageHaveWorkedWith', 'PlatformHaveWorkedWith',  
                  'WebframeHaveWorkedWith', 'MiscTechHaveWorkedWith', 'ToolsTechHaveWorkedWith', 
                  'NEWCollabToolsHaveWorkedWith', ]
    
    name = ["Databases", "Languages", "Platforms", "Webframes", "Miscelaneous Tech", "Tools", "Collab tools"]
    categoria = ""
    if active_tab is not None: #para evitar un error hay que añadir un caso donde active_tab sste vacio
        if active_tab =="db1":
            df = ageTech(df21,nameColumns[0])
            categoria = name[0]
            fig = px.treemap(df, path=['Age1stCode', nameColumns[0]],values='count',
                            title = 'Age of first coding experience and current '+categoria+' used',)
            
        elif active_tab == "lang1":
            df = ageTech(df21,nameColumns[1])
            categoria = name[1]
            fig = px.treemap(df, path=['Age1stCode', nameColumns[1]],values='count',
                            title = 'Age of first coding experience and current '+categoria+' used',)
            
        elif active_tab == "plat1":
            df = ageTech(df21,nameColumns[2])
            categoria = name[2]
            fig = px.treemap(df, path=['Age1stCode', nameColumns[2]],values='count',
                            title = 'Age of first coding experience and current '+categoria+' used',)
            
        elif active_tab == "web1":
            df = ageTech(df21,nameColumns[3])
            categoria = name[3]
            fig = px.treemap(df, path=['Age1stCode', nameColumns[3]],values='count',
                            title = 'Age of first coding experience and current '+categoria+' used',)
            
        elif active_tab == "misc1":
            df = ageTech(df21,nameColumns[4])
            categoria = name[4]
            fig = px.treemap(df, path=['Age1stCode', nameColumns[4]],values='count',
                            title = 'Age of first coding experience and current '+categoria+' used',)
            
        elif active_tab == "tools1":
            categoria = name[5]
            df = ageTech(df21,nameColumns[5])
            fig = px.treemap(df, path=['Age1stCode', nameColumns[5]],values='count',
                            title = 'Age of first coding experience and current '+categoria+' used',)
            
        elif active_tab == "colab1":
            categoria = name[6]
            df = ageTech(df21,nameColumns[6])
            fig = px.treemap(df, path=['Age1stCode', nameColumns[6]],values='count',
                            title = 'Age of first coding experience and current '+categoria+' used',)
            
        return dcc.Graph(figure=fig, style={'height': '90vh'}) 
        
        
    return html.P("This shouldn't ever be displayed...")


# In[21]:


@app.callback(
    Output("tabu-content", "children"), 
    Input("sankey", "active_tab"))
    
def tab_content(active_tab):
    
    
    #df = pd.DataFrame()
    nameColumns= ['DatabaseHaveWorkedWith','LanguageHaveWorkedWith', 'PlatformHaveWorkedWith',  
                  'WebframeHaveWorkedWith', 'MiscTechHaveWorkedWith', 'ToolsTechHaveWorkedWith', 
                  'NEWCollabToolsHaveWorkedWith']

    name = ["Databases", "Languages", "Platforms", "Webframes", "Miscelaneous Tech", "Tools", "Collab tools"]
    categoria = ""

    if active_tab is not None: #para evitar un error hay que añadir un caso donde active_tab sste vacio
        if active_tab =="db2":
            
            df = edTech(df21,nameColumns[0])
            categoria = name[0]
            
            #etiquetas
            labels = etiquetas (df, nameColumns[0])
            # Origen de los enlaces (índices a la lista de etiquetas)
            source=df['EdLevel'].apply(lambda x: labels.index(x)).tolist()
            # Destino de los enlaces (índices a la lista de etiquetas)
            target=df[nameColumns[0]].apply(lambda x: labels.index(x)).tolist()

            fig = go.Figure(data=[go.Sankey(node = dict(pad = 15, thickness = 20,
                                                        line = dict(color = "black", width = 0.5),
                                                        label = labels,
                                                       ),
                                            link = dict(
                                                source = source, 
                                                target = target,
                                                value = df['count'] 
                                                  ))])
            fig.update_layout(title_text="Education level and top 5 of most used "+categoria, font_size=12)
            return dcc.Graph(figure=fig, style={'height': '90vh'})         
            
            
        elif active_tab == "lang2":
            df = edTech(df21,nameColumns[1])
            categoria = name[1]
            
            #etiquetas
            labels = etiquetas (df, nameColumns[1])
            # Origen de los enlaces (índices a la lista de etiquetas)
            source=df['EdLevel'].apply(lambda x: labels.index(x)).tolist()
            # Destino de los enlaces (índices a la lista de etiquetas)
            target=df[nameColumns[1]].apply(lambda x: labels.index(x)).tolist()

            fig = go.Figure(data=[go.Sankey(node = dict(pad = 15, thickness = 20,
                                                        line = dict(color = "black", width = 0.5),
                                                        label = labels,
                                                       ),
                                            link = dict(
                                                source = source, 
                                                target = target,
                                                value = df['count'] 
                                                  ))])
            fig.update_layout(title_text="Education level and top 5 of most used "+categoria, font_size=12)
            return dcc.Graph(figure=fig, style={'height': '90vh'}) 
            
        elif active_tab == "plat2":
            df = edTech(df21,nameColumns[2])
            categoria = name[2]
            
            #etiquetas
            labels = etiquetas (df, nameColumns[2])
            # Origen de los enlaces (índices a la lista de etiquetas)
            source=df['EdLevel'].apply(lambda x: labels.index(x)).tolist()
            # Destino de los enlaces (índices a la lista de etiquetas)
            target=df[nameColumns[2]].apply(lambda x: labels.index(x)).tolist()

            fig = go.Figure(data=[go.Sankey(node = dict(pad = 15, thickness = 20,
                                                        line = dict(color = "black", width = 0.5),
                                                        label = labels,
                                                       ),
                                            link = dict(
                                                source = source, 
                                                target = target,
                                                value = df['count'] 
                                                  ))])
            fig.update_layout(title_text="Education level and top 5 of most used "+categoria, font_size=12)
            return dcc.Graph(figure=fig, style={'height': '90vh'}) 
            
        elif active_tab == "web2":
            df = edTech(df21,nameColumns[3])
            categoria = name[3]
            
            #etiquetas
            labels = etiquetas (df, nameColumns[3])
            # Origen de los enlaces (índices a la lista de etiquetas)
            source=df['EdLevel'].apply(lambda x: labels.index(x)).tolist()
            # Destino de los enlaces (índices a la lista de etiquetas)
            target=df[nameColumns[3]].apply(lambda x: labels.index(x)).tolist()

            fig = go.Figure(data=[go.Sankey(node = dict(pad = 15, thickness = 20,
                                                        line = dict(color = "black", width = 0.5),
                                                        label = labels,
                                                       ),
                                            link = dict(
                                                source = source, 
                                                target = target,
                                                value = df['count'] 
                                                  ))]) 
            fig.update_layout(title_text="Education level and top 5 of most used "+categoria, font_size=12)
            return dcc.Graph(figure=fig, style={'height': '90vh'}) 
            
        elif active_tab == "misc2":
            df = edTech(df21,nameColumns[4])
            categoria = name[4]
            
            #etiquetas
            labels = etiquetas (df, nameColumns[4])
            # Origen de los enlaces (índices a la lista de etiquetas)
            source=df['EdLevel'].apply(lambda x: labels.index(x)).tolist()
            # Destino de los enlaces (índices a la lista de etiquetas)
            target=df[nameColumns[4]].apply(lambda x: labels.index(x)).tolist()

            fig = go.Figure(data=[go.Sankey(node = dict(pad = 15, thickness = 20,
                                                        line = dict(color = "black", width = 0.5),
                                                        label = labels,
                                                       ),
                                            link = dict(
                                                source = source, 
                                                target = target,
                                                value = df['count'] 
                                                  ))])
            fig.update_layout(title_text="Education level and top 5 of most used "+categoria, font_size=12)
            return dcc.Graph(figure=fig, style={'height': '90vh'}) 
            
        elif active_tab == "tools2":
            categoria = name[5]
            df = edTech(df21,nameColumns[5])
            
            #etiquetas
            labels = etiquetas (df, nameColumns[5])
            # Origen de los enlaces (índices a la lista de etiquetas)
            source=df['EdLevel'].apply(lambda x: labels.index(x)).tolist()
            # Destino de los enlaces (índices a la lista de etiquetas)
            target=df[nameColumns[5]].apply(lambda x: labels.index(x)).tolist()

            fig = go.Figure(data=[go.Sankey(node = dict(pad = 15, thickness = 20,
                                                        line = dict(color = "black", width = 0.5),
                                                        label = labels,
                                                       ),
                                            link = dict(
                                                source = source, 
                                                target = target,
                                                value = df['count'] 
                                                  ))])
            fig.update_layout(title_text="Education level and top 5 of most used "+categoria, font_size=12)
            return dcc.Graph(figure=fig, style={'height': '90vh'}) 
            
        elif active_tab == "colab2":
            categoria = name[6]
            df = edTech(df21,nameColumns[6])
            
            #etiquetas
            labels = etiquetas (df, nameColumns[6])
            # Origen de los enlaces (índices a la lista de etiquetas)
            source=df['EdLevel'].apply(lambda x: labels.index(x)).tolist()
            # Destino de los enlaces (índices a la lista de etiquetas)
            target=df[nameColumns[6]].apply(lambda x: labels.index(x)).tolist()

            fig = go.Figure(data=[go.Sankey(node = dict(pad = 15, thickness = 20,
                                                        line = dict(color = "black", width = 0.5),
                                                        label = labels,
                                                       ),
                                            link = dict(
                                                source = source, 
                                                target = target,
                                                value = df['count'] 
                                                  ))])
            fig.update_layout(title_text="Education level and top 5 of most used "+categoria, font_size=12)
            
            return dcc.Graph(figure=fig, style={'height': '90vh'}) 
        
        return html.P("tabs: This shouldn't ever be displayed...")
        
        
    return html.P("This shouldn't ever be displayed...")


# # 6. Run

# In[ ]:


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




