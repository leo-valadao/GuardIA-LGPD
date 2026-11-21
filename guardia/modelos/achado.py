from dataclasses import dataclass # Importa o @dataclass, que cria sozinho o __init__ da classe a partir dos campos

from guardia.enumeracoes.forca_do_padrao import ForcaDoPadrao # Importa o enum com as forças do padrão (forte ou fraco)
from guardia.enumeracoes.tipo_de_dado_pessoal import TipoDeDadoPessoal # Importa o enum com os tipos de dado pessoal


@dataclass # Transforma a classe abaixo numa dataclass: uma classe que só guarda dados
class Achado: # Define a classe com o resultado da detecção em uma coluna
    """Dado pessoal detectado em uma coluna (resultado da regra D = F ∨ (W ∧ C))."""
    tipo:                  TipoDeDadoPessoal # Tipo de dado pessoal detectado na coluna
    forca:                 ForcaDoPadrao     # Como foi detectado: forte (F, só pelo valor) ou fraco (W, pelo formato junto com o contexto)
    peso:                  int               # Peso do tipo no score de risco (Quadro 2 do artigo): quanto maior, mais grave
    taxa:                  float             # Parte da amostra, de 0 a 1, cujos valores combinam com o tipo detectado
    tem_contexto:          bool              # Se o nome da coluna indica esse tipo de dado (o C da regra)
    sensivel:              bool = False      # Se é dado pessoal sensível (Art. 5º, II): é tratado em todas as linhas, até nas vazias
    valores_observados:    tuple = ()        # Só para dado sensível: os valores diferentes da amostra, usados no sorteio do dado sintético
    taxa_de_preenchimento: float = 1.0       # Só para dado sensível: parte das linhas, de 0 a 1, que tem valor, usada no sorteio do dado sintético
