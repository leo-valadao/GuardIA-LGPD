from dataclasses import dataclass, field # Importa o @dataclass e o field, que configura um campo da dataclass

from guardia.enumeracoes.modo_de_anonimizacao import ModoDeAnonimizacao # Importa o enum com os modos de anonimização


@dataclass # Transforma a classe abaixo numa dataclass: uma classe que só guarda dados
class ResultadoDaCopia:
    """O que foi copiado e alterado na cópia anonimizada do banco."""
    destino:         str                                # Endereço do banco de cópia que foi criado, com a senha escondida
    modo:            ModoDeAnonimizacao                 # Como os dados pessoais foram tratados: censura ou dados sintéticos
    linhas_copiadas: dict = field(default_factory=dict) # Quantas linhas foram copiadas de cada tabela
    alteracoes:      dict = field(default_factory=dict) # Para cada tabela, quantos valores ou trechos de texto foram trocados em cada coluna
