# tests
#Alba Bartolome

import unittest

from funct import *

class TestCsv(unittest.TestCase):

    def test_existe(self):
        """
        test: comprobar que el directorio del fichero existe
        """

        self.assertTrue(existe("data/dos_filas_cabecera.csv"))
        self.assertTrue(existe("data/dos_filas_cabecera.txt"))
        self.assertTrue(existe("data/dos_filas_no_cabecera.csv"))
        self.assertTrue(existe("data/survey_results_public2020.csv"))
        self.assertTrue(existe("data/survey_results_public2021.csv"))
        self.assertTrue(existe("data/no_vacio.txt"))
        self.assertTrue(existe("data/unicode21.txt"))
        self.assertTrue(existe("data/vacio.csv"))
        self.assertTrue(existe("data/vacio.txt"))

        self.assertFalse(existe("/data/este_fichero_no_existe"))
        self.assertFalse(existe("/data/ni_este.txt"))
        self.assertFalse(existe("/data/este_tampoco.csv"))



    def test_vacio(self):
        """
        test: fichero no vacio
        """
        
        self.assertFalse(vacio("data/dos_filas_cabecera.csv"))
        self.assertFalse(vacio("data/dos_filas_cabecera.txt"))
        self.assertFalse(vacio("data/dos_filas_no_cabecera.csv"))
        self.assertFalse(vacio("data/survey_results_public2020.csv"))
        self.assertFalse(vacio("data/survey_results_public2021.csv"))
        self.assertFalse(vacio("data/no_vacio.txt"))
        self.assertFalse(vacio("data/unicode21.txt"))
        self.assertFalse(vacio("/data/este_fichero_no_existe"))

        self.assertTrue(vacio("data/vacio.csv"))
        self.assertTrue(vacio("data/vacio.txt"))

    def test_encoding_csv(self):
        """
        test: codificacion del fichero
        """
        
        prediccion= 'utf_8'

        self.assertEqual(encoding_csv("data/survey_results_public2020.csv"), prediccion)
        self.assertEqual(encoding_csv("data/survey_results_public2021.csv"), prediccion)
        self.assertEqual(encoding_csv("data/dos_filas_cabecera.csv"), prediccion)
        self.assertEqual(encoding_csv("data/dos_filas_cabecera.txt"), prediccion)
        self.assertEqual(encoding_csv("data/dos_filas_no_cabecera.csv"), prediccion)

        self.assertEqual(encoding_csv("data/vacio.csv"), "archivo demasiado pequenyo")
        self.assertEqual(encoding_csv("data/vacio.txt"), "archivo demasiado pequenyo")
        self.assertEqual(encoding_csv("data/vacio.txt"), "archivo demasiado pequenyo")

        self.assertNotEqual(encoding_csv("no_existe"), prediccion, "error de formato")
        self.assertNotEqual(encoding_csv("data/no_vacio.txt"), prediccion, "error de formato")
        self.assertNotEqual(encoding_csv("data/unicode21.txt"), prediccion, "error de formato")

    def test_extension(self):
        """
        test: extension del fichero.
        """

        self.assertEqual(extension("data/dos_filas_cabecera.csv"), ".csv")
        self.assertEqual(extension("data/dos_filas_cabecera.txt"), ".txt", "error de formato")
        self.assertEqual(extension("data/dos_filas_no_cabecera.csv"), ".csv")
        self.assertEqual(extension("data/no_vacio.txt"), ".txt", "error de formato")
        self.assertEqual(extension("data/vacio.txt"), ".txt", "error de formato")
        self.assertEqual(extension("data/unicode21.txt"), ".txt", "error de formato")
        self.assertEqual(extension("data/vacio.csv"), ".csv")
        self.assertEqual(extension("data/survey_results_public2020.csv"), ".csv")
        self.assertEqual(extension("data/survey_results_public2021.csv"), ".csv")



    def test_columnas_no_nulas(self):
        
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

        self.assertFalse(columnas_no_nulas("data/dos_filas_cabecera.csv",pred21))
        self.assertFalse(columnas_no_nulas("data/dos_filas_no_cabecera.csv", pred21))
        self.assertFalse(columnas_no_nulas("data/dos_filas_cabecera.txt", pred21))
        self.assertFalse(columnas_no_nulas("data/survey_results_public2020.csv", pred21))
        self.assertFalse(columnas_no_nulas("data/no_vacio.txt", pred21))
        self.assertFalse(columnas_no_nulas("data/unicode21.txt", pred21))
        self.assertFalse(columnas_no_nulas("data/vacio.csv", pred21))
        self.assertFalse(columnas_no_nulas("data/vacio.txt", pred21))

        self.assertFalse(columnas_no_nulas("data/dos_filas_cabecera.csv", pred20))
        self.assertFalse(columnas_no_nulas("data/dos_filas_no_cabecera.csv", pred20))
        self.assertFalse(columnas_no_nulas("data/dos_filas_cabecera.txt", pred20))
        self.assertFalse(columnas_no_nulas("data/no_vacio.txt", pred20))
        self.assertFalse(columnas_no_nulas("data/unicode21.txt", pred20))
        self.assertFalse(columnas_no_nulas("data/vacio.csv", pred20))
        self.assertFalse(columnas_no_nulas("data/vacio.txt", pred20))

        self.assertTrue(columnas_no_nulas("data/survey_results_public2020.csv", pred20))
        self.assertTrue(columnas_no_nulas("data/survey_results_public2021.csv", pred21))
if __name__ == '__main__':
    unittest.main()