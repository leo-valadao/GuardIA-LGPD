from dataclasses import dataclass # Importa o @dataclass, que cria sozinho o __init__ da classe a partir dos campos

from guardia.enumeracoes.faixa_de_risco import FaixaDeRisco # Importa o enum com as faixas de risco (baixo, médio e alto)


@dataclass # Transforma a classe abaixo numa dataclass: uma classe que só guarda dados
class AnaliseDaTabela:
    """O que o GuardIA detectou em uma tabela do banco e o score de risco dela."""
    nome:                         str                 # Nome da tabela no banco
    total_de_linhas:              int                 # Quantidade de linhas da tabela
    total_de_colunas:             int                 # Quantidade de colunas da tabela (o N da equação 8)
    colunas:                      dict                # Colunas em que foi detectado dado pessoal, cada uma com o seu Achado
    colunas_de_texto_livre:       list                # Colunas de texto em que o GuardIA procura dados pessoais escritos no meio do texto
    dados_encontrados_nos_textos: dict                # Quantos dados pessoais de cada tipo foram achados em cada coluna de texto livre
    avisos:                       list                # Colunas com possível dado sensível que o GuardIA não trata (só aparecem no relatório)
    forcar_sintetico:             dict                # Colunas de chave (PK, FK ou UNIQUE) que recebem dado sintético até no modo censura
    score_de_risco:               float = 0.0         # Score de risco R da tabela, de 0 a 100 (equação 8 do artigo)
    faixa_de_risco:               FaixaDeRisco = None # Faixa do score de risco: baixo, médio ou alto
    prioritaria:                  bool = False        # Se a tabela é prioritária: score maior que a média mais o desvio padrão de todas
