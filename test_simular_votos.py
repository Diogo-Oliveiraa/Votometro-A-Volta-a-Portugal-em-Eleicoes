import unittest
from unittest.mock import patch, MagicMock
import simular_votos
import os

class TestSimularVotos(unittest.TestCase):

    def test_gerar_pesos_tamanho_e_valores(self):
        partidos = ['A', 'B', 'C']
        pesos = simular_votos.gerar_pesos(partidos)
        self.assertEqual(set(pesos.keys()), set(partidos))
        for v in pesos.values():
            self.assertTrue(0.5 <= v <= 6.0)

    def test_simular_votos_total_corresponde(self):
        pesos = {'A': 5.0, 'B': 1.0}
        total_votos = 1000
        resultado = simular_votos.simular_votos(total_votos, pesos)
        self.assertEqual(sum(resultado.values()), total_votos)

    @patch('builtins.input', return_value='s')
    @patch('os.path.exists', return_value=True)
    @patch('os.listdir')
    @patch('os.remove')
    def test_verificar_dados_existentes_remove_files(self, mock_remove, mock_listdir, mock_exists, mock_input):
        mock_listdir.return_value = ['file1.xlsx', 'file2.xlsx']
        result = simular_votos.verificar_dados_existentes('./fakepath', total_esperado=2)
        self.assertTrue(result)
        mock_remove.assert_any_call(os.path.join('./fakepath', 'file1.xlsx'))
        mock_remove.assert_any_call(os.path.join('./fakepath', 'file2.xlsx'))
        self.assertEqual(mock_remove.call_count, 2)

    @patch('builtins.input', return_value='n')
    @patch('os.path.exists', return_value=True)
    @patch('os.listdir')
    @patch('os.remove')
    def test_verificar_dados_existentes_cancel(self, mock_remove, mock_listdir, mock_exists, mock_input):
        mock_listdir.return_value = ['file1.xlsx']
        result = simular_votos.verificar_dados_existentes('./fakepath', total_esperado=1)
        self.assertFalse(result)
        mock_remove.assert_not_called()

if __name__ == '__main__':
    unittest.main()