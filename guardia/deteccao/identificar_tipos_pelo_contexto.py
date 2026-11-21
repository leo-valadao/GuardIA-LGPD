from guardia.deteccao.padroes import PADROES_DE_DETECCAO # Importa a tabela com as regras de cada tipo de dado pessoal
from guardia.utilitarios.dividir_nome_da_coluna_em_palavras import dividir_nome_da_coluna_em_palavras # Importa a função que separa o nome da coluna em palavras


def identificar_tipos_pelo_contexto(nome_da_coluna): # Define a função, que recebe o nome de uma coluna
    """
    Tipos de dado que o nome da coluna indica (o contexto C da regra).
    Compara o começo de cada palavra do nome: 'telefone_comercial' tem contexto de
    telefone, mas 'cargo' não tem de RG.
    """
    palavras = dividir_nome_da_coluna_em_palavras(nome_da_coluna) # Separa o nome da coluna em palavras

    return { # Devolve um conjunto (grupo sem repetição) com os tipos encontrados
        tipo for tipo, padrao in PADROES_DE_DETECCAO.items() # Passa por cada tipo de dado e pelas suas regras
        if any(palavra.startswith(termo) for palavra in palavras for termo in padrao.termos_de_contexto) # Fica com o tipo se alguma palavra do nome começa com um dos seus termos de contexto
    }
