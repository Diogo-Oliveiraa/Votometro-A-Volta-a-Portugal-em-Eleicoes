import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import apresentacao_resultados as ar  # assume que o ficheiro chama-se apresentacao_resultados.py

class TestApresentacaoResultados(unittest.TestCase):

    def test_normalizar_nome(self):
        self.assertEqual(ar.normalizar_nome("ÁçÊntôs e espaços "), "acentos e espacos")
        self.assertEqual(ar.normalizar_nome("Fóra de Portugal"), "fora de portugal")
        self.assertEqual(ar.normalizar_nome("   Teste "), "teste")

    def test_eh_fora_de_portugal(self):
        self.assertTrue(ar.eh_fora_de_portugal("Fora de Portugal"))
        self.assertTrue(ar.eh_fora_de_portugal("fora portugal"))
        self.assertFalse(ar.eh_fora_de_portugal("Lisboa"))

    @patch("apresentacao_resultados.st")
    @patch("apresentacao_resultados.px")
    def test_mostra_resultados_barras(self, mock_px, mock_st):
        # Preparar DataFrame simples
        df = pd.DataFrame({
            "Distrito": ["D1"],
            "Concelho": ["C1"],
            "Inscritos": [100],
            "VV": [80],
            "VN": [70],
            "VB": [5],
            "Abstencao": [15],
            "PartidoA": [50],
            "PartidoB": [20]
        })

        # Mock do selectbox para escolher "Barras"
        mock_st.selectbox.return_value = "Barras"
        mock_fig = MagicMock()
        mock_px.bar.return_value = mock_fig

        resultado = ar.mostra_resultados(df, "Teste")

        # Verifica se o gráfico foi chamado como esperado
        mock_px.bar.assert_called_once()
        mock_st.plotly_chart.assert_called_once_with(mock_fig, use_container_width=True)

        # Verifica se o DataFrame resultado tem as colunas certas
        self.assertIn("Partido", resultado.columns)
        self.assertIn("Votos", resultado.columns)
        self.assertIn("Percentagem", resultado.columns)
        self.assertEqual(len(resultado), 2)  # 2 partidos

    @patch("apresentacao_resultados.st")
    @patch("apresentacao_resultados.px")
    def test_mostra_resultados_circular(self, mock_px, mock_st):
        df = pd.DataFrame({
            "Distrito": ["D1"],
            "Concelho": ["C1"],
            "Inscritos": [100],
            "VV": [80],
            "VN": [70],
            "VB": [5],
            "Abstencao": [15],
            "PartidoA": [30],
            "PartidoB": [50]
        })
        mock_st.selectbox.return_value = "Circular"
        mock_fig = MagicMock()
        mock_px.pie.return_value = mock_fig

        ar.mostra_resultados(df, "Teste")

        mock_px.pie.assert_called_once()
        mock_st.plotly_chart.assert_called_once_with(mock_fig, use_container_width=True)

    @patch("apresentacao_resultados.st")
    @patch("apresentacao_resultados.px")
    def test_mostra_resultados_linha(self, mock_px, mock_st):
        df = pd.DataFrame({
            "Distrito": ["D1"],
            "Concelho": ["C1"],
            "Inscritos": [100],
            "VV": [80],
            "VN": [70],
            "VB": [5],
            "Abstencao": [15],
            "PartidoA": [30],
            "PartidoB": [50]
        })
        mock_st.selectbox.return_value = "Linha"
        mock_fig = MagicMock()
        mock_px.line.return_value = mock_fig

        ar.mostra_resultados(df, "Teste")

        mock_px.line.assert_called_once()
        mock_st.plotly_chart.assert_called_once_with(mock_fig, use_container_width=True)

if __name__ == "__main__":
    unittest.main()