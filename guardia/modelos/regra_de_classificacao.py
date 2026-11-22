from dataclasses import dataclass # Importa o @dataclass, que cria sozinho o __init__ da classe a partir dos campos

from guardia.enumeracoes.classificacao_do_dado_pessoal import ClassificacaoDoDadoPessoal # Importa o enum com as classificações de dado pessoal
from guardia.enumeracoes.nivel_de_risco import NivelDeRisco # Importa o enum com os níveis de risco


@dataclass # Transforma a classe abaixo numa dataclass: uma classe que só guarda dados
class RegraDeClassificacao:
    """Classificação LGPD de um tipo de dado pessoal: classificação, risco e mitigação sugerida."""
    classificacao: ClassificacaoDoDadoPessoal # Se o dado é pessoal direto, indireto ou sensível, segundo a LGPD
    risco:         NivelDeRisco               # Quão grave é expor esse dado, do crítico ao baixo
    mitigacao:     str                        # Medida sugerida para reduzir o risco desse dado
