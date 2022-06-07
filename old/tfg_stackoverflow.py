
import pandas as pd

from collections import Counter
from itertools import chain

import plotly.express as px
import plotly.graph_objects as go

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc 

# abreviaturas de los estados de us
from abbr import us_state_to_abbrev


# # 2. Importar los dataframe que van a analizarse 



df21 = pd.read_csv('data/survey_results_public2021.csv', engine="c",
                   usecols=["MainBranch", "Country", "US_State", "EdLevel", "Age", "Employment",
                            "Age1stCode", "LearnCode", "YearsCode", "YearsCodePro", "DevType", "OpSys", "NEWStuck",
                            "ConvertedCompYearly", "LanguageHaveWorkedWith", "LanguageWantToWorkWith",
                            "DatabaseHaveWorkedWith", "DatabaseWantToWorkWith", "PlatformHaveWorkedWith",
                            "PlatformWantToWorkWith", "WebframeHaveWorkedWith", "WebframeWantToWorkWith",
                            "MiscTechHaveWorkedWith", "MiscTechWantToWorkWith", "ToolsTechHaveWorkedWith",
                            "ToolsTechWantToWorkWith", 'NEWCollabToolsHaveWorkedWith', 'NEWCollabToolsWantToWorkWith',
                            "ConvertedCompYearly", "OrgSize"])

df20 = pd.read_csv('data/survey_results_public2020.csv', engine="c", usecols=["MainBranch", "Age", "Age1stCode",
                                                                              "ConvertedComp", "Country", "DevType",
                                                                              "EdLevel", "NEWLearn", "NEWStuck",
                                                                              "OpSys", "YearsCode", "YearsCodePro",
                                                                              "LanguageWorkedWith"])


# # Funciones auxiliares 

def graficosRespuesta(df, col):
    """
    Genera un dataframe con valores unicos de col y su conteo.
    Arguments:
        df: dataframe
        col: una columna de df. Escribir entre comillas
    Returns:
        Dataframe con todos los valores unicos de col y su conteo 
    """
    df = df[[col]].dropna().copy()  # copia df

    df2 = (df.explode(df.columns.tolist())
           .apply(lambda col: col.str.split(';'))
           .explode(col).groupby(col)
           .agg(responses=(col, 'count'))
           .reset_index())

    # eliminar todos los valores que contengan ciertos strings
    # ej: Other (please specify), Something else... 
    df2 = df2[~df2[col].str.contains('|'.join(['please', 'not to say', 'else', 't know']))]

    # eliminar la info dentro de parentesis
    df2[col] = df2[col].str.replace(r"\(.*?\)", "", regex=True)

    # ordenar de mas a menos respuestas
    df2.sort_values(["responses"], ascending=True, inplace=True)

    return df2


# In[4]:


def ageCodePro(df):
    """
    Genera dataframe 
    Arguments:
        df: dataframe
    Returns:
        Dataframe con la mediana de las columnas YearsCode y YearsCodePro agrupadas por edad.
    """
    df1 = df[['Age', 'YearsCode', 'YearsCodePro']].dropna().copy()

    # eliminar valores que no aportan informacion
    df1.drop(df1[df1['YearsCode'].isin(["Less than 1 year", "More than 50 years"])].index, inplace=True)
    df1.drop(df1[df1['YearsCodePro'].isin(["Less than 1 year", "More than 50 years"])].index, inplace=True)
    df1.drop(df1[df1['Age'].isin(["Prefer not to say"])].index, inplace=True)

    # convertir columnas a entero
    df1['YearsCode'] = pd.to_numeric(df1['YearsCode'])
    df1['YearsCodePro'] = pd.to_numeric(df1['YearsCodePro'])

    if df1.dtypes['Age'] == 'float64':  # si es el dataframe del anyo 2020, se lidiara con rangos:
        # etiquetas para la nueva columna
        labels = ["Under 18 years old", "18 - 24 years", "25 - 34 years",
                  "35 - 44 years", "45 - 54 years", "55 - 64 years", "65 - 74 years",
                  "75 - 84 years", "Older than 84 years"]
        bins = [10, 17, 24, 34, 44, 54, 64, 74, 84, 100]  # divisiones de rango

        # eliminar valores de edad extremos.
        df1.drop(df1[(df1.Age < 10.0) | (df1.Age > 100.0)].index, inplace=True)

        # sobreescribir valores de columna usando las etiquetas
        df1['Age'] = pd.cut(df1['Age'], bins=bins, labels=labels)

    # agrupar por edad
    df2 = df1.groupby('Age', as_index=False).agg(median_code=('YearsCode', 'median'),
                                                 median_pro=('YearsCodePro', 'median'),
                                                 respuestas=('Age', 'count'))

    return df2


# In[5]:


def caracteristicasDev(df):
    df4 = df[['DevType', 'YearsCode', 'YearsCodePro', 'LearnCode', 'ConvertedCompYearly']].dropna().copy()

    df4.drop(df4[df4['YearsCodePro'] == "Less than 1 year"].index, inplace=True)
    df4.drop(df4[df4['YearsCodePro'] == "More than 50 years"].index, inplace=True)

    df4.drop(df4[df4['YearsCode'] == "Less than 1 year"].index, inplace=True)
    df4.drop(df4[df4['YearsCode'] == "More than 50 years"].index, inplace=True)

    df5 = df4.assign(DevType=df4['DevType'].str.split(';')).explode('DevType').groupby('DevType').agg(
        median_pro=('YearsCodePro', 'median'),  # nueva columna que calculara la media de yearscodepro
        median_code=('YearsCode', 'median'),
        avg_money=('ConvertedCompYearly', 'mean'),
        respuestas=('DevType', 'count')).reset_index().round(2)  # reiniciar el indice
    
    # eliminar datos irrelevantes
    df5.drop(df5[df5['DevType'] == "Other (please specify):"].index, inplace=True)

    df6 = df4[['DevType', 'LearnCode']].dropna().copy()

    # separar todos los valores de las columnas devtype y LearnCode
    df6 = (df6.explode(df6.columns.tolist())
           .apply(lambda col: col.str.split(';'))
           .explode('DevType')
           .explode('LearnCode'))

    # calcular la moda de learn code por tipo de dev
    # La moda estadística es aquel valor que, dentro de un conjunto de datos, se repite el mayor número de veces.
    mode = df6.groupby('DevType')['LearnCode'].apply(lambda x: x.mode()).reset_index()

    df5['LearnCode'] = mode["LearnCode"]

    return df5


# In[6]:


def loveHateWant(df, columna1, columna2):
    
    # copiar solo las columnas que interesan.
    df2 = df[[columna1, columna2]].dropna().copy()

    df3 = pd.DataFrame()

    # en el df vacio se crearan 3 columnas. Se evaluara por filas.
    # columna love sera la interseccion de columna1 y columna 2. (solo elementos que esten en ambas col)
    df3['love'] = [set(x[0].split(';')) & set(x[1].split(';')) for x in df2.values]

    # columna hate sera la diferencia entre columna1 y columna 2. (solo elementos en col1)
    df3['hate'] = [set(x[0].split(';')) - set(x[1].split(';')) for x in df2.values]

    # want sera la diferencia entre columna 2 y columna 1. (solo elementos en col2)
    df3['want'] = [set(x[1].split(';')) - set(x[0].split(';')) for x in df2.values]

    # dataframe que cuenta cada elemento en las columnas
    df_counts = (pd.DataFrame([Counter(chain.from_iterable(df3[column]))
                               for column in df3.columns],
                              index=['love', 'hate', 'want'])
                 .fillna(0)
                 .T
                 .sort_index()
                 )

    return df_counts


# In[7]:


def mundoMapa(dataframe):
    # copiar columnas que interesan
    df = dataframe[['Country']].dropna().copy()
    df2 = pd.DataFrame()
    # contar el numero de paises
    df2["count"] = df['Country'].value_counts()

    return df2


def usMapa(dataframe):
    # revertir el df
    abbrev_to_us_state = dict(zip(us_state_to_abbrev.values(), us_state_to_abbrev.keys()))

    df = dataframe[['US_State', ]].dropna().copy()
    df = df.drop(df[df.US_State == "I do not reside in the United States"].index)
    df2 = pd.DataFrame()

    df2["count"] = df['US_State'].value_counts()  # contar el numero de paises
    df2["state"] = df2.index

    # sustituir el nombre del estado con la abreviatura (us_state_to_abbrev=dict)
    df2['state'] = df2["state"].replace(us_state_to_abbrev, regex=True)

    # crear nueva columna con el nombre del estado completo
    df2['nombreState'] = df2["state"].replace(abbrev_to_us_state, regex=True)

    return df2


# In[8]:


def salario(df, anyo, opt):
    
    col = ""
    
    # se va a usar la misma funcion para generar 2 graficos. 
    if opt == 0: # opt0, se toma DevType como columna
        col = "DevType"
    elif opt == 1 and anyo == 20:
        col = "LanguageWorkedWith" # en 2020 la columna se llamaba diferente
    elif opt == 1 and anyo == 21:
        col = "LanguageHaveWorkedWith"

    df4 = pd.DataFrame()

    if anyo == 20:
        # copia de df y se eliminan todas las columnas que tengan nan
        df4 = df[[col, 'ConvertedComp', 'YearsCodePro', 'Age1stCode']].dropna().copy()
        # para ponder usar el mismo callback en ambas opciones, hay que renombrar las columnas
        df4.rename(columns={'ConvertedComp': 'ConvertedCompYearly'}, inplace=True)
        df4.rename(columns={'LanguageWorkedWith': 'LanguageHaveWorkedWith'}, inplace=True)

        if opt == 1: col = "LanguageHaveWorkedWith"  # renombrar la variable col tambien.

    elif anyo == 21:  # Age1stCode en el df del 2021 son string en lugar de enteros.
        # copia de df y se eliminan todas las columnas que tengan nan.
        df4 = df[[col, 'ConvertedCompYearly', 'YearsCodePro', 'Age1stCode']].dropna().copy()

        # crear diccionario con los cambios de valores
        edadesTransformadas = {"Younger than 5 years": 4, "5 - 10 years": 7, "11 - 17 years": 18, "18 - 24 years": 21,
                               "25 - 34 years": 30, "35 - 44 years": 40, "45 - 54 years": 50, "55 - 64 years": 60,
                               "Older than 64 years": 70}

        # cambiar los valores.
        df4 = df4.replace({"Age1stCode": edadesTransformadas})

    # resto es igual para ambos df y opciones

    # eliminar filas en anyos que tengan texto. 
    df4.drop(df4[df4['YearsCodePro'] == "Less than 1 year"].index, inplace=True)
    df4.drop(df4[df4['YearsCodePro'] == "More than 50 years"].index, inplace=True)

    df4.drop(df4[df4['Age1stCode'] == "Younger than 5 years"].index, inplace=True)
    df4.drop(df4[df4['Age1stCode'] == "Older than 85"].index, inplace=True)

    # convertir columnas a entero
    df4["Age1stCode"] = pd.to_numeric(df4["Age1stCode"])
    df4["YearsCodePro"] = pd.to_numeric(df4["YearsCodePro"])

    # separar filas con mas de un devtype/lenguaje y despues agruparlas
    # df.assign(**kargs) -> https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.assign.html
    df4 = df4.assign(**{col: df4[col].str.split(';')}).explode(col).groupby(col)        .agg(avg_pro=('YearsCodePro', 'mean'), avg_age=('Age1stCode', 'mean'),
             median_money=('ConvertedCompYearly','median'), respuestas=(col, 'count'))\
        .round(2)\
        .reset_index()  # reiniciar el indice

    if opt == 0: df4.drop(df4[df4['DevType'] == "Student"].index, inplace=True)

    return df4


# In[9]:


def ageTech(df3, col):
    # copiar elementos que no sean NaN
    df = df3[['Age', col]].dropna().copy()
    df2 = df.drop(df[df.Age == 'Prefer not to say'].index)  # eliminar info irrelevante
    
    # transformar cada elemento de una lista en una fila, replicando los valores del índice
    df2 = (df2.explode(df2.columns.tolist())
           .apply(lambda col: col.str.split(';'))
           .explode('Age')
           .explode(col))

    # tabla de frecuencia
    return (pd.crosstab(df2['Age'], df2[col])
            .melt(value_name='count', ignore_index=False)
            .reset_index())


# In[10]:


def edTech(df3, col):
    # copiamos elementos que no sean NaN
    df = df3[['EdLevel', col]].dropna().copy()

    # eliminar info irrelevante
    df.drop(df[df.EdLevel == 'Something else'].index, inplace=True)

    # transformar cada elemento de una lista en una fila, replicando los valores del índice
    df2 = (df.explode(df.columns.tolist())
           .apply(lambda col: col.str.split(';'))
           .explode('EdLevel')
           .explode(col))

    # tabla de frecuencia
    df4 = (pd.crosstab(df2['EdLevel'], df2[col])
           .melt(value_name='count', ignore_index=False)
           .reset_index())

    # eliminar parentesis en educacion
    df4['EdLevel'] = df4['EdLevel'].str.replace(r"\(.*?\)", "", regex=True)

    # Seleccionar solo un top 5 de tecnologias (lenguajes, bases de datos...)
    top = df4[[col, 'count']].groupby(col).sum().sort_values(by='count', ascending=False).index[:5]
    return df4[df4[col].isin(top.tolist())]


# etiquetas unicas de col + EdLevel. (se usa en grafico sankey)
def etiquetas(df, col):
    edLabels = list(df.EdLevel.unique())
    colLabels = list(df[col].unique())
    labels = edLabels + colLabels

    return labels


# # Layout 


# Initializar la app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',  # permite ser responsive en movil
                            'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}]
                )

server = app.server #heroku

CONTENT_STYLE = {
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 2rem",
}

FOOTER_STYLE = {
    "margin-left": "0rem",
    "margin-right": "0rem",
    "margin-bottom": "0rem",
    "margin-top": "0rem",
    "background-color": "#f8f9fa",
}

app.layout = html.Div([

    # ---------------- NAVBAR ------------

    dbc.Navbar([

        dbc.Row([  # logo
            dbc.Col(html.A([html.Img(
                src=
  "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Stack_Overflow_icon.svg/512px-Stack_Overflow_icon.svg.png",
                # https://appharbor.com/assets/images/stackoverflow-logo.png
                height="35px", className='text-end ms-2')]
                , href='https://www.stackoverflow.com', target="_blank")), # abrir un hipervinculo en nueva pg
            
            dbc.Col(dbc.NavbarBrand("Dashboard: TFG - GII_O_MA_21.05", className='text-start fw-bolder')),
            

            # dropdown al final del navbar
            dbc.Col([  
                dbc.DropdownMenu(
                    children=[
                        # IMP: para navegar en la misma pagina:
                        # 1: crear etiquetas id en los html (como si se fuesen a unar en el callback.)
                        # 2. en el navbar, anyadir # delante del href pare referenciar esa id.
                        # 3. poner la etiqueta de external_link=true en el navbar para que funcione en la misma pg

                        dbc.DropdownMenuItem("Dev Profile", href="#uno", external_link=True),
                        dbc.DropdownMenuItem("Technology", href="#dos", external_link=True),
                        dbc.DropdownMenuItem("Work", href="#tres", external_link=True),
                    ],
                    nav=True,
                    in_navbar=True,
                    label="Index",
                    className="position-absolute top-0 end-0",
                    align_end=True,  # menu no mas grande que la pagina
                )  # dropdown
            ])  # col
        ])  # logo

    ],  # navbar
        sticky="top",  # para que se quede siempre arriba, aun haciendo scroll
    ),  # fin navbar

    # colores de fuente: docs: https://dash-bootstrap-components.opensource.faculty.ai/docs/components/alert/
    # text-primary: azul
    # text-secondary: gris
    # text-warning: amarillo
    # text-success: verde
    # text-info: azul claro
    # imp: estos colores solo son validos para el tema bootstrap. Cian tiene otro esquema, ver docs

    # ---------------- CUERPO -----------

    dbc.Row([  # contenido

        # ########### TITULO: DEV PROFILE #############

        dbc.Row([
            dbc.Col(html.H1("Developer Profile", id="uno", className="text-center"))

        ], justify="center",
            style={'color': '#10546B'},
        ),  # cabecero

        # #Grafico: Doble barras
        dbc.Row([
            dbc.Col([

                html.H2('Age Vs Years Coding.'),
                # html.P('Age Vs Years Coding.'),
                dbc.Row([  # botones
                    dbc.Col([
                        dbc.RadioItems(
                            id="opt1",
                            className="btn-group ml-auto",
                            inputClassName="btn-check",
                            labelClassName="btn btn-outline-primary",
                            labelCheckedClassName="active",
                            options=[
                                {"label": "2021", "value": 2021},
                                {"label": "2020", "value": 2020}
                            ],
                            value=2021,
                        ),
                    ])
                ]),  # botones
                dcc.Loading([  # spinner
                    dcc.Graph(id='primero', figure={}),
                ]),  # spinner
            ])  # col

        ], justify="center"
        ),

        # # Grafico: sunburst
        dbc.Row([
            dbc.Col([
                html.H2('Formative and work characteristics by DevType'),
                html.P('Education, compensation, years developing and years developing professionally by dev type.'),
                dcc.Loading([  # spinner
                    dcc.Graph(id='sunburst', figure=
                    # si no se interactua, no hay necesidad de un callback.
                    px.sunburst(caracteristicasDev(df21), path=['DevType'], values="avg_money",
                                hover_data=['median_pro', "median_code", "avg_money", "LearnCode", "respuestas"],
                                labels={'median_pro': 'Years Coding Profesionaly (median)',
                                        'median_code': 'Years Coding (median)',
                                        'avg_money': 'Average salary ($)', 'DevType': 'Dev type'},
                                color_discrete_sequence=px.colors.qualitative.Pastel, hover_name="DevType")

                              , style={'height': '80vh'}),  # grafico
                ]),  # spinner
            ])
        ], justify="center"
        ),

        ## 4 mini graficos 

        dbc.Row([  # 2 graficos
            dbc.Col([dcc.Loading([
                dcc.Graph(id='stuck', figure=px.pie(graficosRespuesta(df21, "NEWStuck"),
                                                    values='responses', names="NEWStuck",
                                                    color_discrete_sequence=px.colors.qualitative.Safe,
                                                    labels={"NEWStuck": "Resource", "responses": "# Responses"})
                          .update_layout(title_text="What do you do when you get stuck?", title_x=0.5),
                          ),  # stuck
            ]),  # spinner
            ]),  # col
            dbc.Col([dcc.Loading([  # spinner
                dcc.Graph(id='LearnCode', figure=px.pie(graficosRespuesta(df21, "LearnCode"),
                                                        values='responses', names="LearnCode",
                                                        color_discrete_sequence=px.colors.qualitative.Safe,
                                                        labels={"LearnCode": "Resource", "responses": "# Responses"}
                                                        ).update_layout(title_text="Learning how to code", title_x=0.5),
                          ),  # learn code
            ]),  # spinner
            ])  # col
        ]),  # row

        dbc.Row([  # 2 graficos
            dbc.Col([dcc.Loading([
                dcc.Graph(id='Age1stCode', figure=
                (px.bar(graficosRespuesta(df21, "Age1stCode"), y="Age1stCode", x='responses',
                        orientation="h", text_auto=True,
                        color_discrete_sequence=px.colors.qualitative.Safe,
                        labels={"Age1stCode": "Age start coding", "responses": "# Responses"}))
                          .update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)', })
                          .update_layout(yaxis_title=None)
                          .update_layout(title_text="Writing the first line of code", title_x=0.5),

                          # style={'height': '60vh'}
                          ),  # Age1stCode
            ]),  # spinner
            ]),  # col
            dbc.Col([dcc.Loading([
                dcc.Graph(id='EdLearn', figure=(px.bar(graficosRespuesta(df21, "EdLevel"), y="EdLevel", x='responses',
                                                       orientation="h", text_auto=True,
                                                       color_discrete_sequence=px.colors.qualitative.Safe,
                                                       labels={"EdLevel": "Ed Level", "responses": "# Responses"}))
                          .update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)', })
                          .update_layout(yaxis_title=None)
                          .update_layout(title_text="Ed level", title_x=0.5),

                          # style={'height': '60vh'}
                          ),  # edLearn
            ]),  # spinner
            ]),  # col

        ]),  # row


        # # grafico: mapas
        dbc.Row([
            html.H2('Key territories'),
            # html.P("Map with users' origin."),
            dbc.Tabs([
                dbc.Tab(label='World', tab_id='world', labelClassName="text-primary font-weight-bold",
                        activeLabelClassName="text-info"),
                dbc.Tab(label='US only', tab_id='us_only', labelClassName="text-primary font-weight-bold",
                        activeLabelClassName="text-info"),
            ],
                id="tab",
                active_tab="world",
            ),
            dcc.Loading([  # spinner
                dbc.CardBody(html.P(id="mapa", className="card-text")),
                # html.Small("To zoom in or out, select 'Pan' and scroll the mouse")
            ])  # spinner
        ]),

        # ###################### Titulo: TECHNOLOGY ####################
        dbc.Row([
            dbc.Col(html.H1("Technology", id="dos", className="text-center"))  # titulo navbar
        ], justify="center",
            style={'color': '#10546B'},
        ),  # titulo

        # grafico: staked diagram
        dbc.Row([
            html.H2("Love Vs Hate Vs Want."),
            html.P("Users' tech preferences"),
            dbc.Tabs([
                dbc.Tab(label='Databases', tab_id='db', labelClassName="text-primary font-weight-bold",
                        activeLabelClassName="text-info"),
                dbc.Tab(label='Languages', tab_id='lang', labelClassName="text-primary font-weight-bold",
                        activeLabelClassName="text-info"),
                dbc.Tab(label='Platform', tab_id='plat', labelClassName="text-primary font-weight-bold",
                        activeLabelClassName="text-info"),
                dbc.Tab(label='webframe', tab_id='web', labelClassName="text-primary font-weight-bold",
                        activeLabelClassName="text-info"),
                dbc.Tab(label='Miscelaneous', tab_id='misc', labelClassName="text-primary font-weight-bold",
                        activeLabelClassName="text-info"),
                dbc.Tab(label='Tools', tab_id='tools', labelClassName="text-primary font-weight-bold",
                        activeLabelClassName="text-info"),
                dbc.Tab(label='Collab', tab_id='colab', labelClassName="text-primary font-weight-bold",
                        activeLabelClassName="text-info"),
            ],
                id="stacked",
                active_tab="db",
            ),
            dcc.Loading([  # spinner
                dbc.CardBody(html.P(id="stacked2", className="card-text")),
            ])  # spinner
        ]),

        
        # grafico: treemap (cajitas) edad vs tech
        dbc.Row([
            html.H2("Current tech use by Ed level"),
            # html.P("Tech preferences by age"),
            dbc.Tabs([
                dbc.Tab(label='Databases', tab_id='db1', labelClassName="text-primary font-weight-bold",
                        activeLabelClassName="text-info"),
                dbc.Tab(label='Languages', tab_id='lang1', labelClassName="text-primary font-weight-bold",
                        activeLabelClassName="text-info"),
                dbc.Tab(label='Platform', tab_id='plat1', labelClassName="text-primary font-weight-bold",
                        activeLabelClassName="text-info"),
                dbc.Tab(label='webframe', tab_id='web1', labelClassName="text-primary font-weight-bold",
                        activeLabelClassName="text-info"),
                dbc.Tab(label='Miscelaneous', tab_id='misc1', labelClassName="text-primary font-weight-bold",
                        activeLabelClassName="text-info"),
                dbc.Tab(label='Tools', tab_id='tools1', labelClassName="text-primary font-weight-bold",
                        activeLabelClassName="text-info"),
                dbc.Tab(label='Collab', tab_id='colab1', labelClassName="text-primary font-weight-bold",
                        activeLabelClassName="text-info"),
            ],
                id="treemap",
                active_tab="db1",
            ),
            dcc.Loading([  # spinner
                dbc.CardBody(html.P(id="treemap2", className="card-text")),
            ]),
        ]
        ),  

        # grafico: sankey (filas conectadas) ed level vs tech
        dbc.Row([
            html.H2('Current tech use by age.'),
            # html.P("Tech usage according to age"),
            dbc.Tabs([
                dbc.Tab(label='Databases', tab_id='db2', labelClassName="text-primary font-weight-bold",
                        activeLabelClassName="text-info"),
                dbc.Tab(label='Languages', tab_id='lang2', labelClassName="text-primary font-weight-bold",
                        activeLabelClassName="text-info"),
                dbc.Tab(label='Platform', tab_id='plat2', labelClassName="text-primary font-weight-bold",
                        activeLabelClassName="text-info"),
                dbc.Tab(label='webframe', tab_id='web2', labelClassName="text-primary font-weight-bold",
                        activeLabelClassName="text-info"),
                dbc.Tab(label='Miscelaneous', tab_id='misc2', labelClassName="text-primary font-weight-bold",
                        activeLabelClassName="text-info"),
                dbc.Tab(label='Tools', tab_id='tools2', labelClassName="text-primary font-weight-bold",
                        activeLabelClassName="text-info"),
                dbc.Tab(label='Collab', tab_id='colab2', labelClassName="text-primary font-weight-bold",
                        activeLabelClassName="text-info"),
            ],
                id="sankey",
                active_tab="db2",
            ),
            dcc.Loading([  # spinner
                dbc.CardBody(html.P(id="sankey2", className="card-text")),
            ]),  # spinner
        ]),  # sankey

        # ############### TITULO: WORK ############
        dbc.Row([
            dbc.Col(html.H1("Work", id="tres", className="text-center"))  # esto va al navbar
        ], justify="center",
            style={'color': '#10546B'},
        ),  # titulo

        # # grafico: salarios
        dbc.Row([
            dbc.Col([
                html.H2('Salary and experience by developer type'),
                # html.P('Correlation between Salary, type of developer and years coding.'),
                dbc.Row([
                    dbc.Col([
                        dbc.RadioItems(
                            id="opt4",
                            className="btn-group",
                            inputClassName="btn-check",
                            labelClassName="btn btn-outline-primary",
                            labelCheckedClassName="active",
                            options=[
                                {"label": "2021", "value": 2021},
                                {"label": "2020", "value": 2020}
                            ],
                            value=2021,
                        ),
                    ])  # col
                ]),
                dbc.Row([  # boton
                    dbc.Col([
                        dbc.Button('Button 1', id='hide-show', n_clicks=0, color="light", className="m-3"),
                    ]),
                ]),

                dcc.Loading([  # spinner
                    dcc.Graph(id='salario', figure={}, style={'height': '90vh'}),
                ]),  # spinner
            ])
        ], justify="center",

        ),  # salarios.

        # # 2 mini graficos
        dbc.Row([  # grafico 1
            dbc.Col([dcc.Loading([
                dcc.Graph(id='OrgSize', figure=px.pie(graficosRespuesta(df21, "OrgSize"),
                                                      values='responses', names="OrgSize",
                                                      color_discrete_sequence=px.colors.qualitative.Safe,
                                                      labels={"responses": "# Responses",
                                                              "OrgSize": "Org size"}).update_layout(
                    title_text="Company size", title_x=0.5),
                          # style={'height': '60vh'}
                          ),  # org size
            ]),  # spinner
            ]),  # col
            dbc.Col([dcc.Loading([
                dcc.Graph(id='Employment', figure=(px.bar(graficosRespuesta(df21, "Employment"), y="Employment",
                                                          x='responses', orientation="h", text_auto=True,
                                                          color_discrete_sequence=px.colors.qualitative.Safe,
                                                          labels={"Age1stCode": "Age start coding",
                                                                  "responses": "# Responses"}))
                          .update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)', })
                          .update_layout(yaxis_title=None)
                          .update_layout(title_text="Employment status", title_x=0.5),
                          # style={'height': '60vh'}

                          ),  # Employment
            ]),  # spinner
            ]),  # col
        ]),  # row

        # # grafico: salarios- lenguaje
        dbc.Row([
            dbc.Col([
                html.H2('Salary and experience by language'),
                # html.P('Correlation between Salary, leng and years coding (both profesionaly and non profesionaly).'),
                dbc.Row([  # dropdown para el primer grafico
                    dbc.Col([

                        dbc.RadioItems(
                            id="opt5",
                            className="btn-group",
                            inputClassName="btn-check",
                            labelClassName="btn btn-outline-primary",
                            labelCheckedClassName="active",
                            options=[
                                {"label": "2021", "value": 2021},
                                {"label": "2020", "value": 2020}
                            ],
                            value=2021,
                        ),
                    ])  # col
                ]),  # dropdown
                dbc.Row([  # boton
                    dbc.Col([
                        dbc.Button('Button 2', id='hide-show2', n_clicks=0, color="light", className="m-3"),
                    ]),
                ]),

                dcc.Loading([  # spinner
                    dcc.Graph(id='salario-leng', figure={}, style={'height': '80vh'}),
                ]),  # spinner
            ])
        ], justify="center",

        ),

    ], style=CONTENT_STYLE,  # fin del contenido. Aplicar el estilo.

    ),  #fin  contenido

    # ---------------- FOOTER-----------

    dbc.Row([  # footer

        dbc.Col([
            dbc.Col(html.H4(" ", className="text-center mb-4 d-none d-lg-block")),  # mb: margin bottom
            dbc.Col(
                html.P("Stackoverflow survey data has been used to create this dashboard. See the links for more info",
                       className="ms-5 me-5 d-none d-lg-block")),
        ], className="border-end",
            # "d-flex justify-content-center justify-content-lg-between p-4 border-bottom",
        ),  # sociales

        dbc.Col([  # hecho con...  #ms: margin start
            dbc.Col(html.H4("Made with ", className="text-start mb-3 ms-5 d-none d-lg-block")),
            html.A(  # className='text-center text-primary mb-4'
                dbc.Col(html.P("Dash", className='text-start text-secondary ms-5')),
                href="https://dash.plotly.com/", target="_blank",
                style={"textDecoration": "none"},
            ),  # link github
            html.A(  # className='text-center text-primary mb-4'
                dbc.Col(html.P("Plotly", className='text-start text-secondary ms-5')),
                # dbc.Col(html.Img(src="https://logonoid.com/images/stack-overflow-logo.png", height="30px")),
                href="https://plotly.com/python/", target="_blank",
                style={"textDecoration": "none"},
            ),  # link plotly

        ]),  # Hecho con

        dbc.Col([  # links
            dbc.Col(html.H4("Interesting links", className="text-start mb-3 ms-5 d-none d-lg-block")),
            #
            html.A(  # className='text-center text-primary mb-4'
                dbc.Col(html.P("Stackoverflow dashboard 2021", className='text-start text-secondary ms-5')),
                href="https://insights.stackoverflow.com/survey/2021", target="_blank",
                style={"textDecoration": "none"},
            ),  # link stack
            html.A(  # className='text-center text-primary mb-4'
                dbc.Col(html.P("Stackoverflow survey", className='text-start text-secondary ms-5')),
                # dbc.Col(html.Img(src="https://logonoid.com/images/stack-overflow-logo.png", height="30px")),
                href="https://insights.stackoverflow.com/survey?_ga=2.189292843.1285052511.1645528337-438523718.1645528337",
                target="_blank",
                style={"textDecoration": "none"},
            ),  # link stack

        ]),  # links

        # colores de fuente: docs: https://dash-bootstrap-components.opensource.faculty.ai/docs/components/alert/
        # text-primary: azul
        # text-secondary: gris
        # text-warning: amarillo
        # text-success: verde
        # text-info: azul claro
        # imp: estos colores solo son validos para el tema bootstrap. Cian tiene otro esquema, ver docs

        dbc.Col([  # sociales
            dbc.Col(html.H4("Contact ", className="text-start mb-3 ms-5 d-none d-lg-block")),
            html.A(  # className='text-center text-primary mb-4'
                dbc.Col(html.P("Github", className='text-start text-secondary ms-5')),
                # dbc.Col(html.Img(src="https://logonoid.com/images/stack-overflow-logo.png", height="30px")),
                href="https://github.com/albarrom", target="_blank",
                style={"textDecoration": "none"},
            ),  # link github
            html.A(  # className='text-center text-primary mb-4'
                dbc.Col(html.P("Email", className='text-start text-secondary ms-5')),
                # dbc.Col(html.Img(src="https://logonoid.com/images/stack-overflow-logo.png", height="30px")),
                href="mailto:abr0041@alu.ubu.es", target="_blank",
                style={"textDecoration": "none"},
            ),  # link github

        ]),  # sociales

        html.Hr(),  # barra decorativa

        dbc.Row([  # ultima linea
            dbc.Col(html.P("2022 TFG - GII_O_MA_21.05", className="text-center")),
        ])  # c ultima linea

    ], className="text-secondary",  # hacer el texto gris
        style=FOOTER_STYLE,
    )  # footer

])  # layout


# # Funciones callback 


@app.callback(
    Output(component_id='primero', component_property='figure'),
    Input(component_id='opt1', component_property='value'))
def update_graph(opt1):
    if opt1 == 2020:
        df = ageCodePro(df20)
    else:
        df = ageCodePro(df21)

    fig = px.bar(df, y="Age", x=["median_pro", "median_code"],
                 orientation="h", barmode='group', hover_data=["respuestas"],
                 text_auto=True, labels={'respuestas': '# Responses',
                                         'median_pro': 'Years Coding Profesionaly (average)',
                                         'median_code': 'Years Coding (average)'},
                 color_discrete_sequence=px.colors.qualitative.Safe)

    # cambiar el nombre de las etiquetas en la leyenda
    nuevasEtiquetas = {'median_pro': 'Years Coding Profesionaly (average)',
                       'median_code': 'Years since start coding (average)', }
    fig.for_each_trace(lambda t: t.update(name=nuevasEtiquetas[t.name],
                                          legendgroup=nuevasEtiquetas[t.name],
                                          hovertemplate=t.hovertemplate.replace(t.name, nuevasEtiquetas[t.name])))

    # poner el numero de respuestas fuera de la barra y en posicion horizontal.
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig['layout']['yaxis']['autorange'] = "reversed"  # valores en orden descendente

    # renombrar ejes
    fig.update_xaxes(title_text="# Years")
    fig.update_yaxes(title_text="Age")

    # quitar color y grid del grafico
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)', })  # fondo transparente
    fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))  # eliminar grid

    return fig


# In[13]:


# tech vs tech. 

@app.callback(
    Output("stacked2", "children"),
    Input("stacked", "active_tab"))
def tab_content(active_tab):
    # df = pd.DataFrame()

    nameColumns = ['DatabaseHaveWorkedWith', 'DatabaseWantToWorkWith', 'LanguageHaveWorkedWith',
                   'LanguageWantToWorkWith', 'PlatformHaveWorkedWith', 'PlatformWantToWorkWith', 
                   'WebframeHaveWorkedWith', 'WebframeWantToWorkWith', 'MiscTechHaveWorkedWith', 
                   'MiscTechWantToWorkWith', 'ToolsTechHaveWorkedWith', 'ToolsTechWantToWorkWith',
                   'NEWCollabToolsHaveWorkedWith', 'NEWCollabToolsWantToWorkWith']
    
    # valores para iterar en las posiciones del array namColumns
    col1 = 0
    col2 = 0

    name = "" # nombre del eje y

    if active_tab is not None:  # para evitar un error hay que añadir un caso donde active_tab este vacio
        if active_tab == "db":
            col1 = 0  # posicion de columna en namecolumns : DatabaseHaveWorkedWith
            col2 = 1  # 'DatabaseWantToWorkWith'
            name = "Databases"

        elif active_tab == "lang":
            col1 = 2
            col2 = 3
            name = "Languages"

        elif active_tab == "plat":
            col1 = 4
            col2 = 5
            name = "Platforms"

        elif active_tab == "web":
            col1 = 6
            col2 = 7
            name = "Webframes"

        elif active_tab == "misc":
            col1 = 8
            col2 = 9
            name = "Miscelaneous Tech"

        elif active_tab == "tools":
            col1 = 10
            col2 = 11
            name = "Tools"

        elif active_tab == "colab":
            col1 = 12
            col2 = 13
            name = "Collab tools"

        df = loveHateWant(df21, nameColumns[col1], nameColumns[col2])

        fig = px.bar(df, x=['love', 'hate', 'want'], y=df.index,
                     color_discrete_sequence=px.colors.qualitative.Safe,
                     # color_discrete_sequence = px.colors.qualitative.T10,
                     orientation='h',
                     )

        # nombre de ejes
        fig.update_yaxes(title_text=name)
        fig.update_xaxes(title_text="# Responses")

        # quitar color y grid del grafico
        fig.update_layout(
            {'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)', })  # fondo transparente
        fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))  # eliminar grid

        return dcc.Graph(figure=fig, style={'height': '90vh'})

    return html.P("This shouldn't ever be displayed...")


# In[14]:


# mundo/us

@app.callback(
    Output("mapa", "children"),
    Input("tab", "active_tab"))

def tab_content2(active_tab):
    if active_tab is not None:  # para evitar un error hay que añadir un caso donde active_tab este vacio
        if active_tab == "world":

            fig = px.scatter_geo(mundoMapa(df21), locationmode='country names',
                                 locations=mundoMapa(df21).index,
                                 size='count', color='count',
                                 # title = 'Users and their location',
                                 color_continuous_scale=px.colors.cyclical.IceFire,
                                 labels={"locations": "Country", "count": "# Responses"})

            # quitar color y grid del grafico
            fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)', })
            fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))

            # evitar que cambie el zoom del grafico  al hacer scroll encima.
            fig.update_layout(dragmode=False)

            return dcc.Graph(figure=fig, style={'height': '90vh'})
        elif active_tab == "us_only":
            fig = px.scatter_geo(usMapa(df21), locationmode='USA-states', locations=usMapa(df21).state,
                                 size='count', color='count',
                                 color_continuous_scale=px.colors.cyclical.IceFire,
                                 hover_data=["nombreState"],
                                 labels={"count": "# Responses", "nombreState": "State", "locations": "State (abbrev.)"}
                                 )

            # hacer que el mapa se enfoque solo en us en vez de en todo el mundo
            fig.update_layout(geo=dict(scope='usa', projection_type='albers usa', showland=True,
                                       landcolor="rgb(250, 250, 250)", #  cambiar colores en el mapa
                                       subunitcolor="rgb(217, 217, 217)",
                                       countrycolor="rgb(217, 217, 217)",
                                       countrywidth=0.5,
                                       subunitwidth=0.5
                                       )
                              )

            # quitar color y grid del grafico
            fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)', })
            fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))  # eliminar grid

            # evitar que cambie el zoom del grafico  al hacer scroll encima.
            fig.update_layout(dragmode=False)

            return dcc.Graph(figure=fig, style={'height': '90vh'})

    return html.P("This shouldn't ever be displayed...")


# In[15]:


@app.callback(
    [Output(component_id='salario', component_property='figure'),
     Output('hide-show', 'children')],
    [Input(component_id='opt4', component_property='value'),
     Input(component_id='hide-show', component_property='n_clicks')])

def update_graph(opt4, n_clicks): # 2 argumentos. Uno por input
    
    if opt4 == 2020:
        df = df20
        anyo = 20
    else:
        df = df21
        anyo = 21
    # opcion 0 es para el tipo de Dev.
    fig = px.scatter(salario(df, anyo, 0), x="avg_pro", y="median_money", size="respuestas",
                     color="DevType", hover_name="DevType", text="DevType", hover_data=["avg_age"],
                     labels={'avg_pro': 'Years Coding Profesionaly (average)',
                             'avg_age': 'Age start coding (average)',
                             'respuestas': '# responses', 'median_money': 'Median salary ($)',
                             'DevType': 'Dev type'},
                     color_discrete_sequence=px.colors.qualitative.Safe)
                    # color_discrete_sequence=px.colors.qualitative.Pastel)

    # centrar el texto encima de cada representacion de dato
    fig.update_traces(textposition='top center')

    # quitar fondo de grafico
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)', })

    # color al grid, para poder ver mejor las divisiones
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(183, 216, 236, 0.41)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(183, 216, 236, 0.41)')

    bool_disabled = n_clicks % 2
    if bool_disabled:
        return fig, "Hide Leyend" 
    else:
        # ocultar leyenda
        fig.update_layout(showlegend=False)
        return fig, "Show Leyend"


# In[16]:


@app.callback(
    Output("treemap2", "children"),
    Input("treemap", "active_tab"))
def treemap(active_tab):  # edad vs tech

    nameColumns = ['DatabaseHaveWorkedWith', 'LanguageHaveWorkedWith', 'PlatformHaveWorkedWith',
                   'WebframeHaveWorkedWith', 'MiscTechHaveWorkedWith', 'ToolsTechHaveWorkedWith',
                   'NEWCollabToolsHaveWorkedWith']
    orden = 0

    if active_tab is not None:  # para evitar un error hay que añadir un caso donde active_tab este vacio
        if active_tab == "db1":
            orden = 0

        elif active_tab == "lang1":
            orden = 1

        elif active_tab == "plat1":
            orden = 2

        elif active_tab == "web1":
            orden = 3

        elif active_tab == "misc1":
            orden = 4

        elif active_tab == "tools1":
            orden = 5

        elif active_tab == "colab1":
            orden = 6

        df = ageTech(df21, nameColumns[orden])
        fig = px.treemap(df, path=['Age', nameColumns[orden]], values='count',
                         labels={"count": "# Responses"},
                         color_discrete_sequence=px.colors.qualitative.Safe)

        return dcc.Graph(figure=fig, style={'height': '90vh'})

    return html.P("This shouldn't ever be displayed...")


# In[17]:


@app.callback(
    Output("sankey2", "children"),
    Input("sankey", "active_tab"))

def tab_content(active_tab):
    nameColumns = ['DatabaseHaveWorkedWith', 'LanguageHaveWorkedWith', 'PlatformHaveWorkedWith',
                   'WebframeHaveWorkedWith', 'MiscTechHaveWorkedWith', 'ToolsTechHaveWorkedWith',
                   'NEWCollabToolsHaveWorkedWith']
    orden = 0

    if active_tab is not None:  # para evitar un error hay que añadir un caso donde active_tab este vacio
        if active_tab == "db2":
            orden = 0  # posicion en nameColumns

        elif active_tab == "lang2":
            orden = 1

        elif active_tab == "plat2":
            orden = 2

        elif active_tab == "web2":
            orden = 3

        elif active_tab == "misc2":
            orden = 4

        elif active_tab == "tools2":
            orden = 5

        elif active_tab == "colab2":
            orden = 6


        df = edTech(df21, nameColumns[orden])

        # etiquetas
        labels = etiquetas(df, nameColumns[orden])
        # Origen de los enlaces (índices a la lista de etiquetas)
        source = df[nameColumns[orden]].apply(lambda x: labels.index(x)).tolist()
        # Destino de los enlaces (índices a la lista de etiquetas)
        target = df['EdLevel'].apply(lambda x: labels.index(x)).tolist()

        fig = go.Figure(data=[go.Sankey(node=dict(pad=15, thickness=20,
                                                  line=dict(color="black", width=0.5),
                                                  label=labels,
                                                  ),
                                        link=dict(
                                            source=source,
                                            target=target,
                                            value=df['count']
                                        ))], )
        return dcc.Graph(figure=fig, style={'height': '70vh'})

    return html.P("This shouldn't ever be displayed...")


# In[18]:


@app.callback(
    [Output(component_id='salario-leng', component_property='figure'),
     Output('hide-show2', 'children')],
    [Input(component_id='opt5', component_property='value'),
     Input(component_id='hide-show2', component_property='n_clicks')])
def update_graph(opt5, n_clicks):  # se pasan los dos input.

    if opt5 == 2020:
        df = df20
        anyo = 20
    else:
        df = df21
        anyo = 21

    fig = px.scatter(salario(df, anyo, 1), x="avg_pro", y="median_money", size="respuestas",
                     color="LanguageHaveWorkedWith", hover_name="LanguageHaveWorkedWith",
                     text="LanguageHaveWorkedWith", hover_data=["avg_age"],
                     labels={'avg_pro': 'Years Coding Profesionaly (average)',
                             'avg_age': 'Age start coding (average)',
                             'respuestas': '# responses', 'median_money': 'Median salary ($)',
                             'LanguageHaveWorkedWith': 'Language'},
                     color_discrete_sequence=px.colors.qualitative.Pastel, )

    fig.update_traces(textposition='top center')  # centrar texto que va encima de los puntos del grafico

    # quitar color y grid del grafico
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)', })  # fondo transparente

    # color al grid, para poder ver mejor las divisiones
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(183, 216, 236, 0.41)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(183, 216, 236, 0.41)')

    bool_disabled = n_clicks % 2
    if bool_disabled:
        return fig, "Hide Leyend"  # se devuelven los dos output
    else:
        fig.update_layout(showlegend=False)
        return fig, "Show Leyend"


# # Run 


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
