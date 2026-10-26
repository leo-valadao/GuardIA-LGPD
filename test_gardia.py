import unittest
import os
import sys

# Adiciona o diretório atual ao sys.path para garantir importação dos módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from deteccao import escanear_banco
from classificacao import classificar_dados
from avaliar import calcular_precisao_revocacao
from relatorio import gerar_relatorio

class TestGardIALGPD(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            'Nome': ['Ana Silva', 'Carlos Santos'],
            'CPF': ['111.222.333-44', '555.666.777-88'],
            'E-mail': ['ana@email.com', 'carlos@email.com'],
            'Idade': [25, 40]
        })

    def test_escanear_banco(self):
        colunas = escanear_banco(self.df)
        self.assertIn('Nome', colunas)
        self.assertIn('CPF', colunas)
        self.assertIn('E-mail', colunas)
        self.assertNotIn('Idade', colunas)

    def test_classificar_dados(self):
        colunas = ['Nome', 'CPF']
        res = classificar_dados(colunas)
        self.assertEqual(res['CPF']['risco'], 'Crítico')
        self.assertEqual(res['Nome']['risco'], 'Alto')

    def test_calcular_precisao_revocacao(self):
        identificadas = ['Nome', 'CPF']
        reais = ['Nome', 'CPF']
        metricas = calcular_precisao_revocacao(identificadas, reais)
        self.assertEqual(metricas['precisao'], 100.0)
        self.assertEqual(metricas['revocacao'], 100.0)

if __name__ == '__main__':
    unittest.main()
