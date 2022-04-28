#!/usr/bin/env python
# coding: utf-8

# # [Histogram](https://plotly.com/python/histograms/)
# 
# ## 1. importar las librerías + csv con los datos de la encuesta. 

# In[1]:


# importar librerias

import pandas as pd
import plotly.express as px  
from dash import Dash, dcc, html, Input, Output


#crear un dataframe con toda la informacion de la encuesta
df_csv = pd.read_csv ('survey/survey_results_public2021.csv', index_col = [0]) # El indice sera la columna con el ID de la respuesta
df_csv #mostrar df ()


# ## 2. Preprocesar datos.
# 
# Tratar las columnas/conjunto de datos para comenzar a crear los gráficos. En este caso Age1stcode

# In[2]:


df_csv['Age1stCode'].value_counts() 


# Para lidiar con rangos de edades, algunos de los cuales tienen texto, se va a calcular una nueva columna con la media de todos ellos. 
# 

# In[3]:


#se hace una copia del df.
df= df_csv.copy()

#normalizar todos los datos.

df = df[df['Age1stCode'].notna()] #eliminar los nulos


df.loc[df["Age1stCode"] == "Younger than 5 years", "Age1stCode"] = "04 - 04 years" #ya hay un 05 anyos en el df. 
df.loc[df["Age1stCode"] == "Older than 64 years", "Age1stCode"] = "65 - 65 years"
df.loc[df["Age1stCode"] == "5 - 10 years", "Age1stCode"] = "05 - 10 years"

#primero se seleccionan los digitos del string (la columna del df es string) y el resultado se convierte a entero
df['min'] = df.Age1stCode.astype(str).str[:2].astype(int) #la edad minima del rango es el primer numero
df['max'] = df.Age1stCode.astype(str).str[5:7].astype(int) # el maximo es el segundo numero

#una vez ya se tiene la edad minima y la maxima, se calcula la media de ambas columnas.
df['media'] = df[['min', 'max']].mean(axis=1)


# ## 3. Grafico. 
# 
# En este caso, un diagrama de barras.

# In[4]:


app = Dash(__name__)
server = app.server #heroku
app.layout = html.Div([

    html.H1("Tipo de desarrollador", style={'text-align': 'center'}), #cabecero h1. Header
    
    #primera mini prueba con un menu desplegable.
    dcc.Dropdown(id="select_opt",  
                 options=[ #el usuario va a ver las label.
                     {"label": "#", "value": "numero"},
                     {"label": "%", "value": "porcentaje"}],
                 multi=False,
                 value="numero",
                 style={'width': "40%"}
                 ),

    dcc.Graph(id='my_survey', figure={}) # graph container

])


# In[5]:


@app.callback(
    Output(component_id='my_survey', component_property='figure'),
    Input(component_id='select_opt', component_property='value'))
def update_graph(option_slctd):
    #filtered_df = df[df.year == selected_year]
    fig = px.histogram(df, x="media",
                      title='Histograma de edad',
                      labels={'media':'media', 'count':'total'}, # can specify one label per df column
                      opacity=0.8,
                      color_discrete_sequence=['indianred'] # color of histogram bars
                   )
        # no implementado la opcion con el porcentaje
    
    return fig


# ## 4. run server

# In[6]:

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)


# In[ ]:




