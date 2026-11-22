from dataclasses import dataclass # Importa o @dataclass, que cria sozinho o __init__ da classe a partir dos campos

from guardia.enumeracoes.tipo_de_dado_pessoal import TipoDeDadoPessoal # Importa o enum com os tipos de dado pessoal


@dataclass # Transforma a classe abaixo numa dataclass: uma classe que só guarda dados
class Trecho:
    """Dado pessoal encontrado dentro de um texto livre, com a posição em que ele aparece no texto."""
    inicio: int               # Posição do primeiro caractere do trecho no texto (a contagem começa em 0)
    fim:    int               # Posição logo depois do último caractere do trecho
    tipo:   TipoDeDadoPessoal # Tipo de dado pessoal encontrado no trecho
    valor:  str               # O pedaço do texto que contém o dado pessoal
