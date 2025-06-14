import sys
import os
import shutil
import unittest

# Adiciona a raiz do projeto ao path
sys.path.append(os.path.abspath(".."))

from validacao_votos import criar_pasta

class TestCriarPasta(unittest.TestCase):
    def setUp(self):
        """Preparação antes de cada teste: apaga a pasta se já existir."""
        self.pasta = "./ResultadosFinais"
        if os.path.exists(self.pasta):
            shutil.rmtree(self.pasta)

    def test_criar_pasta(self):
        """Teste se a função cria a pasta corretamente."""
        resultado = criar_pasta()
        self.assertTrue(resultado, "A função criar_pasta deveria retornar True.")
        self.assertTrue(os.path.isdir(self.pasta), "A pasta não foi criada corretamente.")

    def tearDown(self):
        """Limpeza após o teste."""
        if os.path.exists(self.pasta):
            shutil.rmtree(self.pasta)

if __name__ == "__main__":
    unittest.main()
