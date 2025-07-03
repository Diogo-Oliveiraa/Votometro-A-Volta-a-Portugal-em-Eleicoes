import unittest
import pandas as pd
from io import StringIO
import sys

# Adiciona a raiz do projeto ao path
sys.path.append(os.path.abspath(".."))

from apresentacao_resultados import normalizar_nome, mostra_resultados

class TestNormalizarNome(unittest.TestCase):
    """Testes unitários para a função normalizar_nome."""

    def test_remove_acentos_e_minusculas(self):
        """Testa remoção de acentos, espaços e conversão para minúsculas."""
        self.assertEqual(normalizar_nome("Árvore "), "arvore")
        self.assertEqual(normalizar_nome("  São João  "), "sao joao")
        self.assertEqual(normalizar_nome("ÓRGÃO"), "orgao")

    def test_string_vazia(self):
        """Testa comportamento com strings vazias ou só espaços."""
        self.assertEqual(normalizar_nome(""), "")
        self.assertEqual(normalizar_nome("   "), "")

    def test_nao_muda_string_sem_acentos(self):
        """Testa strings sem acentos nem espaços."""
        self.assertEqual(normalizar_nome("porto"), "porto")


class TestMostraResultados(unittest.TestCase):
    """Testes unitários para a função mostra_resultados."""

    def setUp(self):
        """Configura um DataFrame simulado para os testes."""
        data_csv = (
            "Distrito,Concelho,Inscritos,VV,VN,VB,Abstencao,PS,PSD,BE,CDU,IL\n"
            "Lisboa,Lisboa,1000,800,790,10,200,300,250,100,80,60\n"
            "Lisboa,Lisboa,1000,800,790,10,200,320,240,90,70,70\n"
        )
        self.df = pd.read_csv(StringIO(data_csv))

    def test_retorna_df_grafico(self):
        """Testa se a função retorna DataFrame com colunas esperadas e votos."""
        df_grafico = mostra_resultados(self.df, "Testando Resultados")
        self.assertIn("Partido", df_grafico.columns)
        self.assertIn("Votos", df_grafico.columns)
        self.assertIn("Percentagem", df_grafico.columns)
        self.assertGreater(df_grafico["Votos"].sum(), 0)

    def test_sem_votos_validos(self):
        """Testa comportamento quando não há votos para nenhum partido."""
        df_zero = self.df.copy()
        for partido in ["PS", "PSD", "BE", "CDU", "IL"]:
            df_zero[partido] = 0
        df_grafico = mostra_resultados(df_zero, "Sem votos")
        self.assertTrue(all(df_grafico["Percentagem"] == 0))


if __name__ == "__main__":
    unittest.main()