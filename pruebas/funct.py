import sys
import csv

from charset_normalizer import CharsetNormalizerMatches as CnM

import pandas as pd
from pandas.errors import EmptyDataError
from pathlib import Path
import os




#ficheros correctos.
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

lista_vacia21 = [None] * (len(df21.columns))
lista_vacia20 = [None] * (len(df20.columns))

def existe(directorio):
    try:
        open(directorio,"r")
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFound") # se ha introducido un fichero que no existe
    return True

def vacio (directorio):
    return os.stat(directorio).st_size==0

def encoding_csv(directorio):
    return CnM.from_path(directorio).best().first().encoding

def extension(directorio):
    return directorio[-4:]


def funcion_pandas(directorio):
    try:
        pd.read_csv(directorio)
    return True



def columnas_ok(directorio):
    posible_fichero_ok= pd.read_csv(directorio)
    return posible_fichero_ok.columns




