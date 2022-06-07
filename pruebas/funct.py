

from charset_normalizer import CharsetNormalizerMatches as CnM
import pandas as pd
import os
from re import search

from pandas.errors import EmptyDataError


def existe(directorio):
    try:
        open(directorio,"r")
    except FileNotFoundError:
        return('file not found') # se ha introducido un fichero que no existe
    return True

def vacio (directorio):
    return os.stat(directorio).st_size==0

def encoding_csv(directorio):
    return CnM.from_path(directorio).best().first().encoding

def extension(directorio):
    return directorio[-4:]


def funcion_pandas(directorio):
    try:
        posible_fichero_ok= pd.read_csv(directorio)
        return posible_fichero_ok.columns
    except BaseException as error:
        return format(error)

def archivos_apropiados(directorio):
    try:
        f = pd.read_csv(directorio)
        #columnas nulas
        return f.columns[(f.isnull().sum()/len(f)) ==1].tolist()

    except BaseException as error:
        return format(error)










