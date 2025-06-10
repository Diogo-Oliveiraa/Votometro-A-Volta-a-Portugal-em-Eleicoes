"""Modulos para verificacao de ficheiros"""
import shutil
import unittest
import os
from simular_votos import criar_pastas

class TestCriarPastas(unittest.TestCase):
    """Testa a criação das pastas"""

    def setUp(self):
        self.base_path = "./ResultadoEleicoesDistritos"
        if os.path.exists(self.base_path):
            shutil.rmtree(self.base_path)

    def tearDown(self):
        if os.path.exists(self.base_path):
            shutil.rmtree(self.base_path)

    def test_criar_pastas_sucesso(self):
        """Testa se a função cria as pastas e retorna True"""
        resultado = criar_pastas()
        self.assertTrue(resultado)
        self.assertTrue(os.path.exists(os.path.join(self.base_path, "JSON")))
        self.assertTrue(os.path.exists(os.path.join(self.base_path, "XLSX")))

    def test_pastas_ja_existente(self):
        os.makedirs(os.path.join(self.base_path, "XLSX"))
        os.makedirs(os.path.join(self.base_path, "JSON"))
        resultado = criar_pastas()
        self.assertTrue(resultado)

class TestLerPastas(unittest.TestCase):
    """ Testa a leitura dos documentos na pasta Docs"""

    def test_partidos_existe(self):
        """Este teste PASSA se o ficheiro Partidos.xlsx existir na pasta Docs"""
        self.assertTrue(os.path.exists("./Docs/Partidos.xlsx"))

    def test_distritos_concelhos_existe(self):
        """Este teste PASSA se o ficheiro Distritos_Concelhos.xlsx existir na pasta Docs"""
        self.assertTrue(os.path.exists("./Docs/Distritos_Concelhos.xlsx"))

if __name__ == "__main__":

    unittest.main()
