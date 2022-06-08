
import unittest

import numpy as np

from funct import *

class TestCsv(unittest.TestCase):



    def test_existe(self):
        """
        test: comprobar que el directorio del fichero existe
        """
        dos_filas_cabecera_csv = ("data/dos_filas_cabecera.csv")
        dos_filas_cabecera_txt = ("data/dos_filas_cabecera.txt")
        dos_filas_no_cabecera_csv = ("data/dos_filas_no_cabecera.csv")
        df21 = ("data/survey_results_public2021.csv")
        df20 = ("data/survey_results_public2020.csv")
        no_vacio_txt = ("data/no_vacio.txt")
        unicode21_txt = ("data/unicode21.txt")
        vacio_csv = ("data/vacio.csv")
        vacio_txt = ("data/vacio.txt")

        self.assertTrue(existe(dos_filas_cabecera_csv))
        self.assertTrue(existe(dos_filas_cabecera_txt))
        self.assertTrue(existe(dos_filas_no_cabecera_csv))
        self.assertTrue(existe(df20))
        self.assertTrue(existe(df21))
        self.assertTrue(existe(no_vacio_txt))
        self.assertTrue(existe(unicode21_txt))
        self.assertTrue(existe(vacio_csv))
        self.assertTrue(existe(vacio_txt))

        self.assertFalse(existe("/data/este_fichero_no_existe"))
        self.assertFalse(existe("/data/ni_este.txt"))
        self.assertFalse(existe("/data/este_tampoco.csv"))



    def test_vacio(self):
        """
        test: fichero no vacio
        """
        dos_filas_cabecera_csv = ("data/dos_filas_cabecera.csv")
        dos_filas_cabecera_txt = ("data/dos_filas_cabecera.txt")
        dos_filas_no_cabecera_csv = ("data/dos_filas_no_cabecera.csv")
        df21 = ("data/survey_results_public2021.csv")
        df20 = ("data/survey_results_public2020.csv")
        no_vacio_txt = ("data/no_vacio.txt")
        unicode21_txt = ("data/unicode21.txt")
        vacio_csv = ("data/vacio.csv")
        vacio_txt = ("data/vacio.txt")


        self.assertFalse(vacio(dos_filas_cabecera_csv))
        self.assertFalse(vacio(dos_filas_cabecera_txt))
        self.assertFalse(vacio(dos_filas_no_cabecera_csv))
        self.assertFalse(vacio(df20))
        self.assertFalse(vacio(df21))
        self.assertFalse(vacio(no_vacio_txt))
        self.assertFalse(vacio(unicode21_txt))
        self.assertFalse(vacio("/data/este_fichero_no_existe"))

        self.assertTrue(vacio(vacio_csv))
        self.assertTrue(vacio(vacio_txt))

    def test_encoding_csv(self):
        """
        test: codificacion del fichero
        """
        dos_filas_cabecera_csv = ("data/dos_filas_cabecera.csv")
        dos_filas_cabecera_txt = ("data/dos_filas_cabecera.txt")
        dos_filas_no_cabecera_csv = ("data/dos_filas_no_cabecera.csv")
        df21 = ("data/survey_results_public2021.csv")
        df20 = ("data/survey_results_public2020.csv")
        no_vacio_txt = ("data/no_vacio.txt")
        unicode21_txt = ("data/unicode21.txt")
        vacio_csv = ("data/vacio.csv")
        vacio_txt = ("data/vacio.txt")

        prediccion= 'utf_8'

        self.assertEqual(encoding_csv(df20), prediccion)
        self.assertEqual(encoding_csv(df21), prediccion)
        self.assertEqual(encoding_csv(dos_filas_cabecera_csv), prediccion)
        self.assertEqual(encoding_csv(dos_filas_cabecera_txt), prediccion)
        self.assertEqual(encoding_csv(dos_filas_no_cabecera_csv), prediccion)
        self.assertEqual(encoding_csv(vacio_csv), prediccion)
        self.assertEqual(encoding_csv(vacio_txt), prediccion)
        self.assertEqual(encoding_csv(vacio_txt), prediccion)

        self.assertNotEqual(encoding_csv("no_existe"), prediccion, "error de formato")
        self.assertNotEqual(encoding_csv(no_vacio_txt), prediccion, "error de formato")
        self.assertNotEqual(encoding_csv(unicode21_txt), prediccion, "error de formato")

    def test_extension(self):
        """
        test: extension del fichero.
        """

        dos_filas_cabecera_csv = ("data/dos_filas_cabecera.csv")
        dos_filas_cabecera_txt = ("data/dos_filas_cabecera.txt")
        dos_filas_no_cabecera_csv = ("data/dos_filas_no_cabecera.csv")
        df21 = ("data/survey_results_public2021.csv")
        df20 = ("data/survey_results_public2020.csv")
        no_vacio_txt = ("data/no_vacio.txt")
        unicode21_txt = ("data/unicode21.txt")
        vacio_csv = ("data/vacio.csv")
        vacio_txt = ("data/vacio.txt")


        self.assertEqual(extension(dos_filas_cabecera_csv), ".csv")
        self.assertEqual(extension(dos_filas_cabecera_txt), ".txt", "error de formato")
        self.assertEqual(extension(dos_filas_no_cabecera_csv), ".csv")
        self.assertEqual(extension(no_vacio_txt), ".txt", "error de formato")
        self.assertEqual(extension(vacio_txt), ".txt", "error de formato")
        self.assertEqual(extension(unicode21_txt), ".txt", "error de formato")
        self.assertEqual(extension(vacio_csv), ".csv")
        self.assertEqual(extension(df20), ".csv")
        self.assertEqual(extension(df21), ".csv")

    def test_funcion_pandas(self):
        """
        test: columnas de dataframe coinciden con la prediccion.
        :return:
        """
        dos_filas_cabecera_csv = ("data/dos_filas_cabecera.csv")
        dos_filas_cabecera_txt = ("data/dos_filas_cabecera.txt")
        dos_filas_no_cabecera_csv = ("data/dos_filas_no_cabecera.csv")
        df21 = ("data/survey_results_public2021.csv")
        df20 = ("data/survey_results_public2020.csv")
        no_vacio_txt = ("data/no_vacio.txt")
        unicode21_txt = ("data/unicode21.txt")
        vacio_csv = ("data/vacio.csv")
        vacio_txt = ("data/vacio.txt")

        #columnas que se usan en el dataframe (2021)
        pred21 = ["MainBranch", "Country", "US_State", "EdLevel", "Age", "Employment",
                   "Age1stCode", "LearnCode", "YearsCode", "YearsCodePro", "DevType", "OpSys", "NEWStuck",
                   "ConvertedCompYearly", "LanguageHaveWorkedWith", "LanguageWantToWorkWith",
                   "DatabaseHaveWorkedWith", "DatabaseWantToWorkWith", "PlatformHaveWorkedWith",
                   "PlatformWantToWorkWith", "WebframeHaveWorkedWith", "WebframeWantToWorkWith",
                   "MiscTechHaveWorkedWith", "MiscTechWantToWorkWith", "ToolsTechHaveWorkedWith",
                   "ToolsTechWantToWorkWith", 'NEWCollabToolsHaveWorkedWith', 'NEWCollabToolsWantToWorkWith',
                   "ConvertedCompYearly", "OrgSize"]

        # columnas que se usan en el dataframe (2020)
        pred20 = ["MainBranch", "Age", "Age1stCode", "ConvertedComp", "Country", "DevType","EdLevel", "NEWLearn",
                  "NEWStuck", "OpSys", "YearsCode", "YearsCodePro", "LanguageWorkedWith"]

        #comprueba que todo pred21/pred20 este incluido en los nombres de las columnas de los archivos
        self.assertFalse(set(funcion_pandas(dos_filas_cabecera_txt)).issuperset(set(pred21)))
        self.assertFalse(set(funcion_pandas(dos_filas_no_cabecera_csv)).issuperset(set(pred21)))
        self.assertFalse(set(funcion_pandas(df20)).issuperset(set(pred21)))
        self.assertFalse(set(funcion_pandas(no_vacio_txt)).issuperset(set(pred21)))
        self.assertFalse(set(funcion_pandas(unicode21_txt)).issuperset(set(pred21)))
        self.assertFalse(set(funcion_pandas(vacio_csv)).issuperset(set(pred21)))
        self.assertFalse(set(funcion_pandas(vacio_txt)).issuperset(set(pred21)))

        self.assertFalse(set(funcion_pandas(dos_filas_cabecera_csv)).issuperset(set(pred20)))
        self.assertFalse(set(funcion_pandas(dos_filas_cabecera_txt)).issuperset(set(pred20)))
        self.assertFalse(set(funcion_pandas(dos_filas_no_cabecera_csv)).issuperset(set(pred20)))
        self.assertFalse(set(funcion_pandas(df21)).issuperset(set(pred20)))
        self.assertFalse(set(funcion_pandas(no_vacio_txt)).issuperset(set(pred20)))
        self.assertFalse(set(funcion_pandas(unicode21_txt)).issuperset(set(pred20)))
        self.assertFalse(set(funcion_pandas(vacio_csv)).issuperset(set(pred20)))
        self.assertFalse(set(funcion_pandas(vacio_txt)).issuperset(set(pred20)))

        self.assertTrue(set(funcion_pandas(dos_filas_cabecera_csv)).issuperset(set(pred21)))
        self.assertTrue(set(funcion_pandas(df21)).issuperset(set(pred21)))
        self.assertTrue(set(funcion_pandas(df20)).issuperset(set(pred20)))

    def test_columnas_no_nulas(self):
        dos_filas_cabecera_csv = ("data/dos_filas_cabecera.csv")
        dos_filas_cabecera_txt = ("data/dos_filas_cabecera.txt")
        dos_filas_no_cabecera_csv = ("data/dos_filas_no_cabecera.csv")
        df21 = ("data/survey_results_public2021.csv")
        df20 = ("data/survey_results_public2020.csv")
        no_vacio_txt = ("data/no_vacio.txt")
        unicode21_txt = ("data/unicode21.txt")
        vacio_csv = ("data/vacio.csv")
        vacio_txt = ("data/vacio.txt")

        # columnas que se usan en el dataframe (2021)
        pred21 = ["MainBranch", "Country", "US_State", "EdLevel", "Age", "Employment",
                  "Age1stCode", "LearnCode", "YearsCode", "YearsCodePro", "DevType", "OpSys", "NEWStuck",
                  "ConvertedCompYearly", "LanguageHaveWorkedWith", "LanguageWantToWorkWith",
                  "DatabaseHaveWorkedWith", "DatabaseWantToWorkWith", "PlatformHaveWorkedWith",
                  "PlatformWantToWorkWith", "WebframeHaveWorkedWith", "WebframeWantToWorkWith",
                  "MiscTechHaveWorkedWith", "MiscTechWantToWorkWith", "ToolsTechHaveWorkedWith",
                  "ToolsTechWantToWorkWith", 'NEWCollabToolsHaveWorkedWith', 'NEWCollabToolsWantToWorkWith',
                  "ConvertedCompYearly", "OrgSize"]

        # columnas que se usan en el dataframe (2020)
        pred20 = ["MainBranch", "Age", "Age1stCode", "ConvertedComp", "Country", "DevType", "EdLevel", "NEWLearn",
                  "NEWStuck", "OpSys", "YearsCode", "YearsCodePro", "LanguageWorkedWith"]

        self.assertFalse(columnas_no_nulas(dos_filas_cabecera_csv,pred21))
        self.assertFalse(columnas_no_nulas(dos_filas_no_cabecera_csv, pred21))
        self.assertFalse(columnas_no_nulas(dos_filas_cabecera_txt, pred21))
        self.assertFalse(columnas_no_nulas(df20, pred21))
        self.assertFalse(columnas_no_nulas(no_vacio_txt, pred21))
        self.assertFalse(columnas_no_nulas(unicode21_txt, pred21))
        self.assertFalse(columnas_no_nulas(vacio_csv, pred21))
        self.assertFalse(columnas_no_nulas(vacio_txt, pred21))

        self.assertFalse(columnas_no_nulas(dos_filas_cabecera_csv, pred20))
        self.assertFalse(columnas_no_nulas(dos_filas_no_cabecera_csv, pred20))
        self.assertFalse(columnas_no_nulas(dos_filas_cabecera_txt, pred20))
        self.assertFalse(columnas_no_nulas(no_vacio_txt, pred20))
        self.assertFalse(columnas_no_nulas(unicode21_txt, pred20))
        self.assertFalse(columnas_no_nulas(vacio_csv, pred20))
        self.assertFalse(columnas_no_nulas(vacio_txt, pred20))

        self.assertTrue(columnas_no_nulas(df20, pred20))
        self.assertTrue(columnas_no_nulas(df21, pred21))
if __name__ == '__main__':
    unittest.main()