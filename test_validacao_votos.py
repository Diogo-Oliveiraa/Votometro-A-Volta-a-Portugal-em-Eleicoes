import unittest
import os
from unittest.mock import patch, MagicMock
import pandas as pd
from validacao_votos import (
    ler_docs,
    criar_pasta,
    ficheiros_por_nome_base,
    validar_distrito,
)

class TestValidacaoVotos(unittest.TestCase):

    @patch("os.path.isfile")
    @patch("os.path.isdir")
    def test_ler_docs_ok(self, mock_isdir, mock_isfile):
        mock_isfile.return_value = True
        mock_isdir.return_value = True
        result = ler_docs()
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

    @patch("os.path.isfile")
    @patch("os.path.isdir")
    def test_ler_docs_faltam_ficheiros(self, mock_isdir, mock_isfile):
        mock_isfile.return_value = False
        mock_isdir.return_value = False
        result = ler_docs()
        self.assertFalse(result)

    def test_criar_pasta(self):
        resultado = criar_pasta()
        self.assertTrue(resultado)
        self.assertTrue(os.path.isdir("./ResultadosFinais"))

    def test_ficheiros_por_nome_base(self):
        ficheiros = ["Lisboa_Oeiras.xlsx", "Lisboa_Cascais.txt", "Porto_Gaia.xlsx"]
        resultado = ficheiros_por_nome_base(ficheiros, "Lisboa_Oeiras")
        self.assertEqual(resultado, ["Lisboa_Oeiras.xlsx"])

    @patch("pandas.read_excel")
    def test_validar_distrito_ok(self, mock_read_excel):
        mock_df = pd.DataFrame({
            "Concelho": ["Oeiras"],
            "Inscritos": [100],
            "ADN": [10],
            "Brancos": [5]
        })
        mock_read_excel.return_value = mock_df
        concelhos_distrito = pd.DataFrame({"Concelho": ["Oeiras"]})
        ficheiros = ["Lisboa_Oeiras.xlsx"]
        with patch("os.path.join", return_value="fake_path.xlsx"):
            distrito_ok, resultados, erros = validar_distrito(
                "Lisboa", concelhos_distrito, ficheiros, "."
            )
        self.assertTrue(distrito_ok)
        self.assertEqual(len(resultados), 1)
        self.assertEqual(erros, [])

if __name__ == "__main__":
    unittest.main()