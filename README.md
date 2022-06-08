<h1 align="center">
	Dashboard de visualización del uso y preferencias de los desarrolladores basado en las encuestas anuales de Stack Overflow
	<a href="https://www.codacy.com/gh/albarrom/GII_O_MA_21.05/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=albarrom/GII_O_MA_21.05&amp;utm_campaign=Badge_Grade"><img src="https://app.codacy.com/project/badge/Grade/c76950ce941e42c783f68748c6d639cf"/></a>
</h1>



# Descripción

Esta aplicación ha sido creada para procesar datos recogidos de las [encuestas anuales de Stackoverflow](https://insights.stackoverflow.com/survey?_ga=2.189292843.1285052511.1645528337-438523718.1645528337) y mostrarlos al usuario en forma accesible con gráficos interactivos.

# Lo básico. 

Todo lo que se necesita para continuar ampliando la aplicación se puede encontrar en [`tfg_stackoverflow.ipynb`](https://github.com/albarrom/GII_O_MA_21.05/blob/main/tfg_stackoverflow.ipynb) o en [`tfg_stackoverflow.py`](https://github.com/albarrom/GII_O_MA_21.05/blob/main/tfg_stackoverflow.py). Ambos contienen la misma información, se puede usar el que mejor se adapte a las necesidades particulares del usuario.
* Los ficheros con extensión `*.csv` que contienen los datos de las encuestas de Stackoverflow están en la carpeta `data`
* También se va a necesitar el fichero `abbr.py` para ejecutar uno de los gráficos. 

Se puede obtener más información sobre lo que contienen las demás carpetas leyendo el fichero readme que hay en cada una de ellas.


# Comenzando
Para poder poner en funcionamiento una copia del proyecto se van a necesitar:

[Python 3.10](https://www.python.org/downloads/windows/) y un IDE a elección (se recomienda [PyCharm](https://www.jetbrains.com/pycharm/download/#section=windows)) o [Anaconda](https://www.anaconda.com/).

Si se elige Python se necesitará, además de un IDE, las librerías: pandas, plotly, dash, dash-bootstrap-components y numpy. Para ello se deben ejecutar los siguientes comandos:
	- pip install pandas
	- pip install plotly
	- pip install dash
	- pip install dash-bootstap-components
	- pip install numpy
	 
Si va a usarse Anaconda (opción más recomendada), la lista de librerías a instalar es mas reducida. Bastará con:

	- pip install dash
	- pip install dash-bootstap-components

		
# App

Puedes echar un vistazo al dashboard accediendo a [esta](https://tfg-dashboard.herokuapp.com/) URL. 




# Construido con: 

* [Plotly Python](https://plotly.com/python/). 
* [Dash](https://dash.plotly.com/).
* [Heroku](https://www.heroku.com/developers).
* [Python 3.10](https://www.python.org/downloads/release/python-3100/)
