from dataclasses import dataclass, field # Importa o @dataclass e o field, que configura um campo da dataclass

from sqlalchemy import MetaData # Importa o MetaData, a classe do SQLAlchemy que guarda a estrutura de um banco


@dataclass # Transforma a classe abaixo numa dataclass: uma classe que só guarda dados
class AnaliseDoBanco:
    """A análise de todas as tabelas do banco, usada para gerar o relatório e a cópia."""
    url:                  str                                            # Endereço do banco analisado, com a senha escondida (é o que aparece no relatório)
    tabelas:              list                                           # A análise de cada tabela do banco: uma AnaliseDaTabela por tabela
    nomes_conhecidos:     set                                            # Todos os nomes de pessoas das colunas de nome, para encontrá-los também dentro dos textos livres
    objetos_nao_copiados: list                                           # Views, functions, triggers e tipos compostos do banco, com o tipo e o nome de cada um: a cópia não os leva
    metadata:             MetaData = field(repr=False, default=None)     # Estrutura do banco lida pelo SQLAlchemy (tabelas, colunas e constraints), usada para criar a cópia
    sequencias:           list = field(repr=False, default_factory=list) # Sequences do banco, com a configuração, o valor atual e a coluna dona de cada uma, para recriá-las na cópia
