
import unittest
from funct import *

class TestCsv(unittest.TestCase):



    def test_existe(self):
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

        self.assertRaises("FileNotFoundError(2, 'No such file or directory')", existe, "/data/este_fichero_no_existe")
        self.assertRaises(FileNotFoundError, existe, "/data/este_fichero_tampoco.csv")
        self.assertRaises(FileNotFoundError, existe, "/data/ni_este.txt")


    def test_vacio(self):
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
        self.assertTrue(vacio(vacio_csv))
        self.assertTrue(vacio(vacio_txt))

    def test_encoding_csv(self):
        dos_filas_cabecera_csv = ("data/dos_filas_cabecera.csv")
        dos_filas_cabecera_txt = ("data/dos_filas_cabecera.txt")
        dos_filas_no_cabecera_csv = ("data/dos_filas_no_cabecera.csv")
        df21 = ("data/survey_results_public2021.csv")
        df20 = ("data/survey_results_public2020.csv")
        no_vacio_txt = ("data/no_vacio.txt")
        unicode21_txt = ("data/unicode21.txt")
        vacio_csv = ("data/vacio.csv")
        vacio_txt = ("data/vacio.txt")

        self.assertEqual(encoding_csv(df20), 'utf_8')
        self.assertEqual(encoding_csv(df21), 'utf_8')
        self.assertEqual(encoding_csv(dos_filas_cabecera_csv), 'utf_8')
        self.assertEqual(encoding_csv(dos_filas_cabecera_txt), 'utf_8')
        self.assertEqual(encoding_csv(dos_filas_no_cabecera_csv), 'utf_8')
        self.assertEqual(encoding_csv(no_vacio_txt), 'ascii')
        self.assertEqual(encoding_csv(unicode21_txt), 'utf_16')
        self.assertEqual(encoding_csv(vacio_csv), 'utf_8')
        self.assertEqual(encoding_csv(vacio_txt), 'utf_8')

    def test_extension(self):

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
        self.assertEqual(extension(dos_filas_cabecera_txt), ".txt")
        self.assertEqual(extension(dos_filas_no_cabecera_csv), ".csv")
        self.assertEqual(extension(no_vacio_txt), ".txt")
        self.assertEqual(extension(vacio_txt), ".txt")
        self.assertEqual(extension(unicode21_txt), ".txt")
        self.assertEqual(extension(vacio_csv), ".csv")
        self.assertEqual(extension(df20), ".csv")
        self.assertEqual(extension(df21), ".csv")

    def test_funcion_pandas(self):
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

        self.assertTrue(set(funcion_pandas(dos_filas_cabecera_csv)).issuperset(set(pred21)))
        self.assertFalse(set(funcion_pandas(dos_filas_cabecera_txt)).issuperset(set(pred21)))
        self.assertFalse(set(funcion_pandas(dos_filas_no_cabecera_csv)).issuperset(set(pred21)))
        self.assertTrue(set(funcion_pandas(df21)).issuperset(set(pred21)))
        self.assertFalse(set(funcion_pandas(df20)).issuperset(set(pred21)))
        self.assertFalse(set(funcion_pandas(no_vacio_txt)).issuperset(set(pred21)))

        self.assertRaises(Exception, funcion_pandas, unicode21_txt)
        self.assertRaises(Exception, funcion_pandas, vacio_csv)
        self.assertRaises(Exception, funcion_pandas, vacio_txt)

        self.assertFalse(set(funcion_pandas(dos_filas_cabecera_csv)).issuperset(set(pred20)))
        self.assertFalse(set(funcion_pandas(dos_filas_cabecera_txt)).issuperset(set(pred20)))
        self.assertFalse(set(funcion_pandas(dos_filas_no_cabecera_csv)).issuperset(set(pred20)))
        self.assertFalse(set(funcion_pandas(df21)).issuperset(set(pred20)))
        self.assertTrue(set(funcion_pandas(df20)).issuperset(set(pred20)))
        self.assertFalse(set(funcion_pandas(no_vacio_txt)).issuperset(set(pred20)))

    def test_archivos_apropiados(self):
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


        #si algun archivo tiene columnas enteras vacias que son vitales para el dashboard, el fichero no sera apto
        self.assertEqual(any(item in archivos_apropiados(dos_filas_cabecera_csv) for item in pred21),True)
        self.assertEqual(any(item in archivos_apropiados(dos_filas_cabecera_txt) for item in pred21), True)
        self.assertEqual(any(item in archivos_apropiados(dos_filas_no_cabecera_csv) for item in pred21), False)
        self.assertEqual(any(item in archivos_apropiados(df20) for item in pred21),False)
        self.assertEqual(any(item in archivos_apropiados(no_vacio_txt) for item in pred21), True)

        self.assertRaises(Exception, funcion_pandas, unicode21_txt)
        self.assertRaises(Exception, funcion_pandas, vacio_csv)
        self.assertRaises(Exception, funcion_pandas, vacio_txt)

        self.assertEqual(any(item in archivos_apropiados(dos_filas_cabecera_csv) for item in pred20), False)
        self.assertEqual(any(item in archivos_apropiados(dos_filas_cabecera_txt) for item in pred20), False)
        self.assertEqual(any(item in archivos_apropiados(dos_filas_no_cabecera_csv) for item in pred20), True)
        self.assertEqual(any(item in archivos_apropiados(df21) for item in pred20), False)
        self.assertEqual(any(item in archivos_apropiados(no_vacio_txt) for item in pred20), True)

        self.assertEqual(any(item in archivos_apropiados(df21) for item in pred21), True)
        self.assertEqual(any(item in archivos_apropiados(df20) for item in pred20), True)


        #
        #
        #
        #
        # prediccion20 =
        #
        # columnas20 = df20.columns
        # bool(set(columnas) & set(columnas20))



if __name__ == '__main__':
    unittest.main()