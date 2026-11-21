import re # Importa o módulo re, de expressões regulares (busca de padrões em texto)

from guardia.excecoes.nome_de_banco_invalido import NomeDeBancoInvalido # Importa o erro lançado quando o nome do banco é inválido


_NOME_DE_BANCO_VALIDO = re.compile(r'^[a-z_][a-z0-9_]{0,62}$') # Padrão de nome válido: começa com letra minúscula ou "_" e tem até 63 letras, números ou "_"


def validar_nome_do_banco(nome_do_banco): # Define a função, que recebe o nome do banco
    """Lança NomeDeBancoInvalido se o nome não seguir o padrão: minúsculas, números e "_"."""
    if not _NOME_DE_BANCO_VALIDO.match(nome_do_banco): # Confere se o nome não segue o padrão
        raise NomeDeBancoInvalido(nome_do_banco) # Lança o erro avisando que o nome é inválido
