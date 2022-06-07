
import unittest
from funct import *
from pandas.errors import EmptyDataError
class TestCsv(unittest.TestCase):



    def test_existe(self):
        dos_filas_cabecera_csv = ("data/dos_filas_cabecera.csv")
        dos_filas_cabecera_txt = ("data/dos_filas_cabecera.txt")
        dos_filas_no_cabecera_csv = ("data/dos_filas_no_cabecera.csv")
        df21 = ("data/survey_results_public2020.csv")
        df20 = ("data/survey_results_public2021.csv")
        no_vacio_txt = ("data/no_vacio.txt")
        unicode21_txt = ("data/unicode21.txt")
        vacio_csv = ("data/vacio.csv")
        vacio_txt = ("data/vacio.txt")

        self.assertEqual(existe(dos_filas_cabecera_csv), True)
        self.assertEqual(existe(dos_filas_cabecera_txt), True)
        self.assertEqual(existe(dos_filas_no_cabecera_csv), True)
        self.assertEqual(existe(df20), True)
        self.assertEqual(existe(df21), True)
        self.assertEqual(existe(no_vacio_txt), True)
        self.assertEqual(existe(unicode21_txt), True)
        self.assertEqual(existe(vacio_csv), True)
        self.assertEqual(existe(vacio_txt), True)

        self.assertRaises(FileNotFoundError, existe, "/data/este_fichero_no_existe")
        self.assertRaises(FileNotFoundError, existe, "/data/este_fichero_tampoco.csv")
        self.assertRaises(FileNotFoundError, existe, "/data/ni_este.txt")


    def test_vacio(self):
        dos_filas_cabecera_csv = ("data/dos_filas_cabecera.csv")
        dos_filas_cabecera_txt = ("data/dos_filas_cabecera.txt")
        dos_filas_no_cabecera_csv = ("data/dos_filas_no_cabecera.csv")
        df21 = ("data/survey_results_public2020.csv")
        df20 = ("data/survey_results_public2021.csv")
        no_vacio_txt = ("data/no_vacio.txt")
        unicode21_txt = ("data/unicode21.txt")
        vacio_csv = ("data/vacio.csv")
        vacio_txt = ("data/vacio.txt")


        self.assertEqual(vacio(dos_filas_cabecera_csv), False)
        self.assertEqual(vacio(dos_filas_cabecera_txt), False)
        self.assertEqual(vacio(dos_filas_no_cabecera_csv), False)
        self.assertEqual(vacio(df20), False)
        self.assertEqual(vacio(df21), False)
        self.assertEqual(vacio(no_vacio_txt), False)
        self.assertEqual(vacio(unicode21_txt), False)
        self.assertEqual(vacio(vacio_csv), True)
        self.assertEqual(vacio(vacio_txt), True)

    def test_encoding_csv(self):
        dos_filas_cabecera_csv = ("data/dos_filas_cabecera.csv")
        dos_filas_cabecera_txt = ("data/dos_filas_cabecera.txt")
        dos_filas_no_cabecera_csv = ("data/dos_filas_no_cabecera.csv")
        df21 = ("data/survey_results_public2020.csv")
        df20 = ("data/survey_results_public2021.csv")
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
        df21 = ("data/survey_results_public2020.csv")
        df20 = ("data/survey_results_public2021.csv")
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

    def text_columnas_ok(self):
        dos_filas_cabecera_csv = ("data/dos_filas_cabecera.csv")
        dos_filas_cabecera_txt = ("data/dos_filas_cabecera.txt")
        dos_filas_no_cabecera_csv = ("data/dos_filas_no_cabecera.csv")
        df21 = ("data/survey_results_public2020.csv")
        df20 = ("data/survey_results_public2021.csv")
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

        self.assertTrue(set(columnas_ok(dos_filas_cabecera_csv)).issuperset(set(pred20)))
        self.assertTrue(set(columnas_ok(dos_filas_cabecera_txt)).issuperset(set(pred20)))
        self.assertTrue(set(columnas_ok(dos_filas_no_cabecera_csv)).issuperset(set(pred20)))
        self.assertTrue(set(columnas_ok(df21)).issuperset(set(pred20)))
        self.assertTrue(set(columnas_ok(df20)).issuperset(set(pred20)))
        self.assertTrue(set(columnas_ok(no_vacio_txt)).issuperset(set(pred20)))
        self.assertTrue(set(columnas_ok(unicode21_txt)).issuperset(set(pred20)))
        self.assertTrue(set(columnas_ok(vacio_csv)).issuperset(set(pred20)))
        self.assertTrue(set(columnas_ok(vacio_txt)).issuperset(set(pred20)))


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