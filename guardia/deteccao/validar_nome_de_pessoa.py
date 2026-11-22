import re # Importa o módulo re, de expressões regulares (busca de padrões em texto)

from guardia.utilitarios.converter_para_texto import converter_para_texto # Importa a função que transforma qualquer valor em texto


# Nome de pessoa: palavras com inicial maiúscula, aceitando "da", "de", "do", "das", "dos", "e"
_PALAVRA_DE_NOME = r"[A-ZÀ-Ý][a-zà-ÿ]+" # Padrão de uma palavra de nome: uma letra maiúscula seguida de letras minúsculas
_EXPRESSAO_REGULAR_DE_NOME_DE_PESSOA = re.compile(rf"{_PALAVRA_DE_NOME}(?:\s+(?:(?:d[aeo]s?|e)\s+)?{_PALAVRA_DE_NOME})+") # Padrão do nome inteiro: uma palavra de nome e mais uma ou várias, com "da", "de", "do", "das", "dos" ou "e" no meio, se houver


def validar_nome_de_pessoa(valor):
    """True se o valor tem cara de nome de pessoa: 2 ou mais palavras com inicial maiúscula."""
    return bool(_EXPRESSAO_REGULAR_DE_NOME_DE_PESSOA.fullmatch(converter_para_texto(valor))) # Verifica se o nome da pessoa é compatível com a expressão regular de nomes.
