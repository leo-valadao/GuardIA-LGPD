from dataclasses import dataclass # Importa o @dataclass, que cria sozinho o __init__ da classe a partir dos campos

from guardia.enumeracoes.forca_do_padrao import ForcaDoPadrao # Importa o enum com as forças do padrão (forte ou fraco)


@dataclass # Transforma a classe abaixo numa dataclass: uma classe que só guarda dados
class PadraoDeDeteccao: # Define a classe com as regras para reconhecer um tipo de dado pessoal
    """Uma linha do Quadro 2 do artigo: como reconhecer um tipo de dado pessoal."""
    expressao_regular:  str | None    # Formato que o valor precisa ter; None quando o tipo não tem formato próprio
    forca:              ForcaDoPadrao # Forte (F): o valor sozinho já basta; fraco (W): o valor também precisa do contexto
    peso:               int           # Peso do tipo no score de risco: quanto maior, mais grave é deixar esse dado exposto
    termos_de_contexto: tuple         # Começos de palavra que, no nome da coluna, indicam esse tipo de dado (o contexto C)
    sensivel:           bool = False  # Se é dado pessoal sensível (Art. 5º, II), que tem uma proteção maior na LGPD

    def __post_init__(self): # Define o método que o Python chama logo depois do __init__ criado pelo @dataclass
        # Um termo sozinho pode ser escrito como texto: aqui ele vira uma tupla com esse termo.
        # Sem isso, o Python percorreria o texto letra por letra, e cada letra viraria um termo.
        if isinstance(self.termos_de_contexto, str): # Confere se os termos foram escritos como um texto só
            self.termos_de_contexto = (self.termos_de_contexto,) # Troca o texto por uma tupla com ele dentro (a vírgula é o que faz a tupla)
