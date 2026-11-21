import unittest # Importa o módulo unittest, que roda os testes automáticos
import os # Importa o módulo os, usado para montar o caminho da pasta do projeto
import sys # Importa o módulo sys, que guarda a lista de pastas onde o Python procura os módulos

# Adiciona a raiz do projeto ao sys.path para importar o pacote guardia
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Coloca a pasta do projeto no começo da lista de pastas de módulos

import datetime # Importa o módulo datetime, que trabalha com datas e horas

from guardia.anonimizacao.anonimizar_registro import MASCARA_DE_DADO_SENSIVEL, anonimizar_registro # Importa a máscara de dado sensível e a função que anonimiza uma linha
from guardia.anonimizacao.anonimizar_texto import anonimizar_texto # Importa a função que anonimiza os dados pessoais dentro de um texto
from guardia.anonimizacao.mascarar_valor import mascarar_valor # Importa a função que censura um valor
from guardia.anonimizacao.substituidor import Substituidor # Importa a classe que gera os valores sintéticos
from guardia.avaliacao.calcular_precisao_e_revocacao import calcular_precisao_e_revocacao # Importa a função que calcula a precisão e a revocação
from guardia.banco.conexao.criar_banco_de_copia import criar_banco_de_copia # Importa a função que cria o banco de cópia
from guardia.banco.conexao.montar_url import montar_url # Importa a função que monta a URL de conexão com o banco
from guardia.banco.conexao.converter_texto_em_url import converter_texto_em_url # Importa a função que lê uma URL escrita como texto
from guardia.banco.conexao.sugerir_nome_do_destino import sugerir_nome_do_destino # Importa a função que sugere o nome do banco de cópia
from guardia.banco.copia.gerar_copia import gerar_copia # Importa a função que cria a cópia anonimizada do banco
from guardia.classificacao.calcular_score_de_risco import calcular_score_de_risco # Importa a função que calcula o score de risco
from guardia.classificacao.classificar_tipo_de_dado import classificar_tipo_de_dado # Importa a função que dá a classificação LGPD de um tipo de dado
from guardia.classificacao.calcular_faixa_de_risco import calcular_faixa_de_risco # Importa a função que diz a faixa do score
from guardia.classificacao.priorizar_tabelas import priorizar_tabelas # Importa a função que marca as tabelas prioritárias
from guardia.deteccao.identificar_dado_sensivel import identificar_dado_sensivel # Importa a função que avisa sobre possível dado sensível
from guardia.deteccao.calcular_digitos_verificadores_do_cpf import calcular_digitos_verificadores_do_cpf # Importa a função que calcula os dígitos verificadores do CPF
from guardia.deteccao.classificar_coluna import classificar_coluna # Importa a função que detecta o tipo de dado pessoal de uma coluna
from guardia.deteccao.validar_cpf import validar_cpf # Importa a função que confere se um CPF é válido
from guardia.deteccao.escanear_texto import escanear_texto # Importa a função que acha dados pessoais dentro de um texto
from guardia.deteccao.identificar_tipos_pelo_contexto import identificar_tipos_pelo_contexto # Importa a função que diz quais tipos o nome da coluna indica
from guardia.enumeracoes.faixa_de_risco import FaixaDeRisco # Importa o enum com as faixas de risco
from guardia.enumeracoes.forca_do_padrao import ForcaDoPadrao # Importa o enum com as forças do padrão
from guardia.enumeracoes.modo_de_anonimizacao import ModoDeAnonimizacao # Importa o enum com os modos de anonimização
from guardia.enumeracoes.nivel_de_risco import NivelDeRisco # Importa o enum com os níveis de risco
from guardia.enumeracoes.tipo_de_dado_pessoal import TipoDeDadoPessoal # Importa o enum com os tipos de dado pessoal
from guardia.excecoes.banco_nao_suportado import BancoNaoSuportado # Importa o erro de banco não suportado
from guardia.excecoes.dados_de_conexao_invalidos import DadosDeConexaoInvalidos # Importa o erro de dados de conexão inválidos
from guardia.excecoes.destino_igual_a_origem import DestinoIgualAOrigem # Importa o erro de cópia com o nome do banco original
from guardia.excecoes.erro_do_guardia import ErroDoGuardia # Importa a exceção-mãe de todos os erros do GuardIA
from guardia.excecoes.modo_invalido import ModoInvalido # Importa o erro de modo inválido
from guardia.excecoes.nome_de_banco_invalido import NomeDeBancoInvalido # Importa o erro de nome de banco inválido
from guardia.excecoes.url_invalida import UrlInvalida # Importa o erro de URL inválida
from guardia.modelos.padrao_de_deteccao import PadraoDeDeteccao # Importa a classe que guarda as regras de um tipo de dado


class TestGuardIALGPD(unittest.TestCase): # Define o grupo de testes gerais do GuardIA

    def test_colunas_com_dados_pessoais(self): # Testa se as colunas com dado pessoal são detectadas
        colunas = { # Cria um dicionário com o nome de cada coluna e os seus valores
            'Nome': ['Ana Silva', 'Carlos Santos'], # Coluna de nomes
            'CPF': ['111.222.333-44', '555.666.777-88'], # Coluna de CPFs
            'E-mail': ['ana@email.com', 'carlos@email.com'], # Coluna de e-mails
            'Idade': [25, 40], # Coluna de idades, que não é dado pessoal detectado
        }
        detectadas = {nome for nome, valores in colunas.items() if classificar_coluna(nome, valores)} # Guarda o nome das colunas em que algum dado pessoal foi detectado
        self.assertEqual(detectadas, {'Nome', 'CPF', 'E-mail'}) # Confere se foram detectadas exatamente essas três colunas

    def test_classificar_tipo_de_dado(self): # Testa a classificação LGPD dos tipos de dado
        self.assertEqual(classificar_tipo_de_dado(TipoDeDadoPessoal.CPF).risco, NivelDeRisco.CRITICO) # Confere se o CPF tem risco crítico
        self.assertEqual(classificar_tipo_de_dado(TipoDeDadoPessoal.NOME).risco, NivelDeRisco.ALTO) # Confere se o nome tem risco alto

    def test_calcular_precisao_e_revocacao(self): # Testa o cálculo da precisão e da revocação
        colunas_identificadas = ['Nome', 'CPF'] # Colunas que o GuardIA achou
        colunas_reais = ['Nome', 'CPF'] # Colunas que de fato têm dado pessoal
        metricas = calcular_precisao_e_revocacao(colunas_identificadas, colunas_reais) # Calcula a precisão e a revocação
        self.assertEqual(metricas['precisao'], 100.0) # Confere se a precisão deu 100%
        self.assertEqual(metricas['revocacao'], 100.0) # Confere se a revocação deu 100%


class TestCPF(unittest.TestCase): # Define o grupo de testes do CPF
    """Equações (5), (6) e (7) do artigo."""

    def test_exemplo_do_artigo(self): # Testa o CPF que o artigo usa de exemplo
        self.assertEqual(calcular_digitos_verificadores_do_cpf('529982247'), (2, 5)) # Confere se os dígitos verificadores calculados são 2 e 5
        self.assertTrue(validar_cpf('529.982.247-25')) # Confere se o CPF com pontuação é válido
        self.assertTrue(validar_cpf('52998224725')) # Confere se o CPF sem pontuação é válido

    def test_invalidos(self): # Testa CPFs inválidos
        self.assertFalse(validar_cpf('111.111.111-11'))   # Dígitos repetidos passam no cálculo
        self.assertFalse(validar_cpf('123.456.789-00')) # Confere se um CPF com dígitos verificadores errados é recusado
        self.assertFalse(validar_cpf('5299822472'))       # 10 dígitos


class TestRegraDeteccao(unittest.TestCase): # Define o grupo de testes da regra de detecção
    """D = F ∨ (W ∧ C)"""

    def test_cargo_nao_e_rg(self): # Testa se a coluna "cargo" não é confundida com RG
        self.assertNotIn(TipoDeDadoPessoal.RG, identificar_tipos_pelo_contexto('cargo')) # Confere se o nome "cargo" não indica RG
        self.assertIsNone(classificar_coluna('cargo', ['Vendedor', 'Analista'])) # Confere se nenhum dado pessoal é detectado na coluna

    def test_cpf_valido_sem_contexto_e_forte(self): # Testa se um CPF válido é detectado mesmo sem contexto
        achado = classificar_coluna('doc', ['52998224725', '11144477735']) # Detecta a coluna "doc", cujo nome não indica CPF
        self.assertEqual((achado.tipo, achado.forca, achado.tem_contexto), (TipoDeDadoPessoal.CPF, ForcaDoPadrao.FORTE, False)) # Confere se é CPF, por padrão forte e sem contexto

    def test_formato_de_cpf_precisa_de_contexto(self): # Testa se o formato de CPF sozinho precisa de contexto
        self.assertEqual(classificar_coluna('cpf', ['123.456.789-00']).forca, ForcaDoPadrao.FRACO)   # W ∧ C
        self.assertIsNone(classificar_coluna('protocolo', ['123.456.789-00']))                      # W sem C

    def test_data_so_com_contexto(self): # Testa se a data só é detectada quando o nome da coluna indica nascimento
        datas = [datetime.date(1985, 3, 12), datetime.date(1990, 7, 1)] # Cria uma lista com duas datas
        self.assertIsNone(classificar_coluna('data_admissao', datas)) # Confere se a data de admissão não é detectada
        self.assertEqual(classificar_coluna('data_nascimento', datas).tipo, TipoDeDadoPessoal.DATA_DE_NASCIMENTO) # Confere se a data de nascimento é detectada

    def test_nome_exige_cara_de_nome(self): # Testa se só valores com cara de nome são detectados como nome
        self.assertIsNone(classificar_coluna('nome', ['Produto 1', 'Produto 2'])) # Confere se nomes de produto não são detectados
        self.assertIsNone(classificar_coluna('nome', ['Vestuário', 'Calçados'])) # Confere se nomes de categoria não são detectados
        self.assertEqual(classificar_coluna('nome', ['Ana Clara Ribeiro', 'João da Silva']).tipo, # Confere se nomes de pessoa são detectados
                         TipoDeDadoPessoal.NOME) # Como nome de pessoa

    def test_contexto_por_palavras_da_coluna(self): # Testa se o contexto é achado em cada palavra do nome da coluna
        self.assertIn(TipoDeDadoPessoal.TELEFONE, identificar_tipos_pelo_contexto('telefone_comercial')) # Confere se "telefone_comercial" indica telefone
        self.assertIn(TipoDeDadoPessoal.EMAIL, identificar_tipos_pelo_contexto('E-mail')) # Confere se "E-mail" indica e-mail
        self.assertIn(TipoDeDadoPessoal.DATA_DE_NASCIMENTO, identificar_tipos_pelo_contexto('dataNascimento')) # Confere se "dataNascimento" indica data de nascimento

    def test_aviso_de_dado_sensivel(self): # Testa o aviso de possível dado sensível
        self.assertEqual(identificar_dado_sensivel('tipo_sanguineo'), 'saúde') # Confere se "tipo_sanguineo" é dado de saúde
        self.assertEqual(identificar_dado_sensivel('filiacao_sindical'), 'filiação a sindicato') # Confere se "filiacao_sindical" é filiação a sindicato
        self.assertIsNone(identificar_dado_sensivel('cargo')) # Confere se "cargo" não gera aviso


class TestTextoLivre(unittest.TestCase): # Define o grupo de testes dos dados dentro de textos livres

    def test_nome_conhecido_e_cpf(self): # Testa se um nome conhecido e um CPF são achados no texto
        texto = 'Cliente Ana Clara Ribeiro, CPF 529.982.247-25, solicitou troca.' # Texto com um nome e um CPF
        tipos = [trecho.tipo for trecho in escanear_texto(texto, {'Ana Clara Ribeiro'})] # Procura os dados pessoais no texto e guarda o tipo de cada um
        self.assertEqual(tipos, [TipoDeDadoPessoal.NOME, TipoDeDadoPessoal.CPF]) # Confere se foram achados o nome e o CPF, nessa ordem

    def test_padrao_fraco_precisa_de_palavra_antes(self): # Testa se o padrão fraco só é aceito com palavra de contexto antes
        tipos = [trecho.tipo for trecho in escanear_texto('Contato pelo telefone (62) 99999-8888.')] # Procura os dados num texto com a palavra "telefone" antes do número
        self.assertEqual(tipos, [TipoDeDadoPessoal.TELEFONE]) # Confere se o telefone foi achado
        self.assertEqual(escanear_texto('Pedido 12345-678 entregue.'), []) # Confere se um número sem contexto não é confundido com CEP

    def test_mascara_so_o_trecho(self): # Testa se a censura troca só o trecho com dado pessoal
        texto, quantidade = anonimizar_texto('E-mail: ana@x.com.br.', ModoDeAnonimizacao.MASCARAR, Substituidor()) # Censura o texto
        self.assertEqual((texto, quantidade), ('E-mail: ************.', 1)) # Confere se só o e-mail virou asteriscos


class TestSubstituidor(unittest.TestCase): # Define o grupo de testes dos dados sintéticos

    def setUp(self): # Roda antes de cada teste do grupo
        self.substituidor = Substituidor(semente=7) # Cria um Substituidor com semente fixa, para os sorteios se repetirem

    def test_mesmo_real_mesmo_falso(self): # Testa se o mesmo valor real vira sempre o mesmo valor falso
        cpf_sintetico = self.substituidor.substituir(TipoDeDadoPessoal.CPF, '529.982.247-25') # Troca um CPF real por um sintético
        self.assertEqual(cpf_sintetico, self.substituidor.substituir(TipoDeDadoPessoal.CPF, '529.982.247-25')) # Confere se o mesmo CPF vira o mesmo sintético
        self.assertNotEqual(cpf_sintetico, self.substituidor.substituir(TipoDeDadoPessoal.CPF, '111.444.777-35')) # Confere se outro CPF vira outro sintético
        self.assertTrue(validar_cpf(cpf_sintetico)) # Confere se o CPF sintético é válido
        self.assertRegex(cpf_sintetico, r'^\d{3}\.\d{3}\.\d{3}-\d{2}$')    # Mantém o formato do original

    def test_mesmo_numero_com_e_sem_formatacao(self): # Testa se o mesmo número, com ou sem pontuação, vira o mesmo valor falso
        cpf_da_coluna = self.substituidor.substituir(TipoDeDadoPessoal.CPF, '52998224725') # Troca o CPF sem pontuação
        cpf_do_texto = self.substituidor.substituir(TipoDeDadoPessoal.CPF, '529.982.247-25') # Troca o mesmo CPF com pontuação
        self.assertEqual(cpf_do_texto.replace('.', '').replace('-', ''), cpf_da_coluna) # Confere se, tirando a pontuação, os dois são iguais
        self.assertRegex(cpf_do_texto, r'^\d{3}\.\d{3}\.\d{3}-\d{2}$') # Confere se o CPF com pontuação manteve a pontuação
        telefone_da_coluna = self.substituidor.substituir(TipoDeDadoPessoal.TELEFONE, '62981234567') # Troca o telefone sem pontuação
        telefone_do_texto = self.substituidor.substituir(TipoDeDadoPessoal.TELEFONE, '(62) 98123-4567') # Troca o mesmo telefone com pontuação
        self.assertEqual(''.join(caractere for caractere in telefone_do_texto if caractere.isdigit()), telefone_da_coluna) # Confere se, tirando a pontuação, os dois são iguais

    def test_bijetor(self): # Testa se valores reais diferentes nunca viram o mesmo valor falso
        nomes_sinteticos = {self.substituidor.substituir(TipoDeDadoPessoal.NOME, f'Pessoa Numero {numero}') # Troca 300 nomes diferentes por nomes falsos
                            for numero in range(300)} # Os números de 0 a 299 deixam cada nome diferente
        self.assertEqual(len(nomes_sinteticos), 300) # Confere se saíram 300 nomes falsos diferentes

    def test_compatibilidade_ddd_e_cep(self): # Testa se o DDD e o começo do CEP são mantidos
        self.assertTrue(self.substituidor.substituir(TipoDeDadoPessoal.TELEFONE, '62981234567').startswith('629')) # Confere se o telefone falso mantém o DDD e o 9
        self.assertTrue(self.substituidor.substituir(TipoDeDadoPessoal.CEP, '74236-928').startswith('74236-')) # Confere se o CEP falso mantém os 5 primeiros dígitos

    def test_email_feito_do_nome(self): # Testa se o e-mail falso é feito a partir do nome
        email = self.substituidor.substituir(TipoDeDadoPessoal.EMAIL, 'real@empresa.com', nome='Maria Clara Araújo') # Troca o e-mail, informando o nome sintético da pessoa
        self.assertIn('araujo', email.split('@')[0])          # Todos os 7 formatos usam o sobrenome
        self.assertNotIn('empresa.com', email) # Confere se o domínio do e-mail real não aparece

    def test_mesma_semente_mesmos_dados(self): # Testa se a mesma semente gera os mesmos dados
        primeiro_nome_sintetico = Substituidor(1).substituir(TipoDeDadoPessoal.NOME, 'Ana Silva') # Gera um nome falso com a semente 1
        segundo_nome_sintetico = Substituidor(1).substituir(TipoDeDadoPessoal.NOME, 'Ana Silva') # Gera de novo, com outro Substituidor e a mesma semente
        self.assertEqual(primeiro_nome_sintetico, segundo_nome_sintetico) # Confere se os dois nomes são iguais

    def test_descartar_dicionario(self): # Testa se o dicionário de trocas é apagado
        self.substituidor.substituir(TipoDeDadoPessoal.CPF, '52998224725') # Faz uma troca, que fica guardada no dicionário
        self.substituidor.descartar_dicionario() # Apaga o dicionário
        self.assertEqual(self.substituidor._dicionario_de_real_para_sintetico, {}) # Confere se o dicionário ficou vazio


class TestDadosSensiveis(unittest.TestCase): # Define o grupo de testes dos dados sensíveis
    """Tipo sanguíneo e filiação sindical (Art. 5.º, II)."""

    def setUp(self): # Roda antes de cada teste do grupo
        self.achado_de_tipo_sanguineo = classificar_coluna('tipo_sanguineo', ['A+', 'O-', 'AB+', 'B-']) # Detecta uma coluna de tipo sanguíneo
        self.achado_de_filiacao_sindical = classificar_coluna('filiacao_sindical', # Detecta uma coluna de filiação sindical
                                                              ['Sindicato dos Empregados no Comércio', None, None, None]) # Com 1 valor preenchido em 4

    def test_detectados_como_sensiveis(self): # Testa se os dois tipos são detectados como sensíveis
        self.assertEqual(self.achado_de_tipo_sanguineo.tipo, TipoDeDadoPessoal.TIPO_SANGUINEO) # Confere se foi detectado tipo sanguíneo
        self.assertTrue(self.achado_de_tipo_sanguineo.sensivel) # Confere se ele está marcado como sensível
        self.assertEqual(self.achado_de_filiacao_sindical.tipo, TipoDeDadoPessoal.FILIACAO_SINDICAL) # Confere se foi detectada filiação sindical
        self.assertTrue(self.achado_de_filiacao_sindical.sensivel) # Confere se ela está marcada como sensível
        self.assertEqual(self.achado_de_filiacao_sindical.taxa_de_preenchimento, 0.25) # Confere se 1 em 4 linhas (25%) está preenchida
        self.assertIsNone(classificar_coluna('nota_da_prova', ['A+', 'B-']))     # Sem contexto

    def test_censura_em_todas_as_linhas(self): # Testa se o dado sensível é censurado em todas as linhas, até nas vazias
        tipos = {'filiacao_sindical': TipoDeDadoPessoal.FILIACAO_SINDICAL} # Tipo de dado da coluna
        achados = {'filiacao_sindical': self.achado_de_filiacao_sindical} # Achado da coluna
        for valor in ('Sindicato dos Empregados no Comércio', None):          # Inclusive a vazia
            registro_anonimizado = anonimizar_registro({'filiacao_sindical': valor}, tipos, # Anonimiza uma linha com esse valor
                                                       ModoDeAnonimizacao.MASCARAR, # No modo censura
                                                       Substituidor(), achados=achados) # Com um Substituidor novo e os Achados
            self.assertEqual(registro_anonimizado['filiacao_sindical'], MASCARA_DE_DADO_SENSIVEL) # Confere se o valor virou a máscara de dado sensível

    def test_sintetico_sem_dicionario(self): # Testa se os dados sensíveis sintéticos são sorteados sem dicionário
        substituidor = Substituidor(semente=3) # Cria um Substituidor com semente fixa
        tipos_sorteados = [substituidor.sortear_dado_sensivel(self.achado_de_tipo_sanguineo) for _ in range(2000)] # Sorteia 2000 tipos sanguíneos
        self.assertTrue(set(tipos_sorteados) <= {'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'}) # Confere se só saíram tipos sanguíneos que existem
        self.assertGreater(tipos_sorteados.count('O+'), tipos_sorteados.count('AB-')) # Confere se o O+, mais comum, saiu mais que o AB-, mais raro
        filiados = [substituidor.sortear_dado_sensivel(self.achado_de_filiacao_sindical) for _ in range(2000)] # Sorteia 2000 filiações sindicais
        self.assertAlmostEqual(sum(filiado is not None for filiado in filiados) / 2000, 0.25, delta=0.05) # Confere se cerca de 25% saíram filiados, como na coluna original
        self.assertEqual(substituidor._dicionario_de_real_para_sintetico, {})        # Nada guardado


class TestExcecoes(unittest.TestCase): # Define o grupo de testes dos erros do GuardIA
    """Erros de conexão e de cópia (não precisam de banco rodando)."""

    def test_url(self): # Testa os erros de URL
        self.assertRaises(UrlInvalida, converter_texto_em_url, 'abc') # Confere se um texto que não é URL dá erro de URL inválida
        self.assertRaises(UrlInvalida, converter_texto_em_url, 'postgresql://guardia@localhost:5432') # Confere se uma URL sem o nome do banco dá erro de URL inválida
        self.assertRaises(BancoNaoSuportado, converter_texto_em_url, 'mysql://guardia@localhost/guardia') # Confere se uma URL de MySQL dá erro de banco não suportado

    def test_dados_de_conexao(self): # Testa os erros de dados de conexão
        self.assertRaises(DadosDeConexaoInvalidos, montar_url, 'localhost', '', 'guardia') # Confere se faltar o banco dá erro
        self.assertRaises(DadosDeConexaoInvalidos, montar_url, 'localhost', 'guardia', 'guardia', porta='abc') # Confere se uma porta que não é número dá erro

    def test_nome_do_banco_de_copia(self): # Testa os erros do nome do banco de cópia
        url = montar_url('localhost', 'guardia', 'guardia') # Monta a URL do banco de origem
        self.assertRaises(NomeDeBancoInvalido, criar_banco_de_copia, url, 'Minha Copia') # Confere se um nome com maiúsculas e espaço dá erro
        self.assertRaises(DestinoIgualAOrigem, criar_banco_de_copia, url, 'guardia') # Confere se o nome do banco original dá erro

    def test_nome_sugerido_para_cada_modo(self): # Testa se cada modo sugere um nome diferente para a cópia
        url = montar_url('localhost', 'guardia', 'guardia') # Monta a URL do banco de origem
        self.assertEqual(sugerir_nome_do_destino(url, ModoDeAnonimizacao.MASCARAR), 'guardia_censurado') # Confere o nome sugerido no modo censura
        self.assertEqual(sugerir_nome_do_destino(url, ModoDeAnonimizacao.SINTETICO), 'guardia_sintetico') # Confere o nome sugerido no modo sintético
        self.assertEqual(sugerir_nome_do_destino(url, 'sintetico'), 'guardia_sintetico') # Confere se o modo escrito como texto também funciona
        self.assertRaises(ModoInvalido, sugerir_nome_do_destino, url, 'censurar') # Confere se um modo que não existe dá erro de modo inválido

    def test_todas_herdam_de_erro_do_guardia(self): # Testa se os erros do GuardIA são todos um ErroDoGuardia
        with self.assertRaises(ErroDoGuardia) as contexto: # Espera que o bloco abaixo lance um ErroDoGuardia
            converter_texto_em_url('mysql://guardia@localhost/guardia') # Lança o erro de banco não suportado
        self.assertIn('PostgreSQL', str(contexto.exception)) # Confere se a mensagem do erro fala de PostgreSQL


class TestMascaraEScore(unittest.TestCase): # Define o grupo de testes da censura e do score de risco

    def test_mascara_total(self): # Testa a censura de cada tipo de valor
        self.assertEqual(mascarar_valor('52998224725'), '***********') # Confere se o texto virou asteriscos, no mesmo tamanho
        self.assertEqual(mascarar_valor(datetime.date(1985, 3, 12)), datetime.date(1985, 1, 1)) # Confere se a data virou 1.º de janeiro do mesmo ano
        self.assertIsNone(mascarar_valor(None)) # Confere se o valor vazio continuou vazio

    def test_constraint_forca_sintetico(self): # Testa se a coluna de chave recebe dado sintético no modo censura
        registro_anonimizado = anonimizar_registro({'cpf': '52998224725'}, {'cpf': TipoDeDadoPessoal.CPF}, # Anonimiza uma linha com um CPF
                                                   ModoDeAnonimizacao.MASCARAR, Substituidor(), # No modo censura
                                                   forcar_sintetico={'cpf': 'UNIQUE'}) # Avisando que a coluna cpf é UNIQUE
        self.assertTrue(validar_cpf(registro_anonimizado['cpf'])) # Confere se o CPF virou um CPF válido, e não asteriscos

    def test_score_equacao_8(self): # Testa a equação 8 do score de risco
        # CPF (w=3) e nome (w=1) em uma tabela de 4 colunas: 100 · 4 / (3 · 4)
        self.assertEqual(calcular_score_de_risco([[TipoDeDadoPessoal.CPF], [TipoDeDadoPessoal.NOME]], 4), 33.33) # Confere se o score deu 33,33
        self.assertEqual(calcular_faixa_de_risco(33.33), FaixaDeRisco.ALTO) # Confere se esse score fica na faixa alta
        self.assertEqual(priorizar_tabelas({'a': 0, 'b': 0, 'c': 90}), {'a': False, 'b': False, 'c': True}) # Confere se só a tabela com score bem acima das outras é prioritária


class TestEnumeracoes(unittest.TestCase): # Define o grupo de testes dos enums e da tabela de padrões
    """Enums (StrEnum) e a tabela de padrões de detecção."""

    def test_enum_tambem_e_texto(self): # Testa se cada opção do enum também funciona como texto
        self.assertEqual(TipoDeDadoPessoal.CPF, 'cpf') # Confere se o enum é igual ao texto
        self.assertEqual(f'{ModoDeAnonimizacao.MASCARAR}', 'mascarar') # Confere se o enum é escrito como o texto dentro de um f-string
        self.assertIs(TipoDeDadoPessoal('cpf'), TipoDeDadoPessoal.CPF) # Confere se o texto pode ser convertido no enum

    def test_termo_de_contexto_escrito_como_texto(self): # Testa se um termo de contexto escrito como texto funciona
        padrao = PadraoDeDeteccao(None, ForcaDoPadrao.FRACO, 1, 'nome') # Cria um padrão com o termo escrito como texto
        self.assertEqual(padrao.termos_de_contexto, ('nome',)) # Confere se o termo virou uma tupla com ele dentro
        self.assertNotIn(TipoDeDadoPessoal.NOME, identificar_tipos_pelo_contexto('endereco')) # Confere se "endereco" não indica nome de pessoa
        self.assertNotIn(TipoDeDadoPessoal.CPF, identificar_tipos_pelo_contexto('cidade')) # Confere se "cidade" não indica CPF

    def test_modo_invalido(self): # Testa o erro de modo inválido
        self.assertRaises(ModoInvalido, gerar_copia, None, None, None, 'censurar', 'copia') # Confere se um modo que não existe dá erro de modo inválido


if __name__ == '__main__': # Confere se este arquivo foi executado direto (e não importado por outro)
    unittest.main() # Roda todos os testes do arquivo
