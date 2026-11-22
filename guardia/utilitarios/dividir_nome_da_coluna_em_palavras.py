import re # Importa o módulo re, de expressões regulares (busca de padrões em texto)

from guardia.utilitarios.normalizar_texto import normalizar_texto # Importa a função que deixa o texto em minúsculas e sem acentos


def dividir_nome_da_coluna_em_palavras(nome_da_coluna):
    """Separa o nome de uma coluna em palavras: 'dataNascimento' / 'data_nascimento' → data, nascimento."""
    nome_da_coluna = re.sub(r'([a-z])([A-Z])', r'\1_\2', str(nome_da_coluna)) # Coloca um "_" entre uma minúscula e a maiúscula que vem logo depois
    nome_da_coluna = normalizar_texto(nome_da_coluna) # Deixa o nome em minúsculas e sem acentos
    palavras = [palavra for palavra in re.split(r'[^a-z0-9]+', nome_da_coluna) if palavra] # Corta o nome em tudo que não é letra nem número e guarda os pedaços que não ficaram vazios
    palavras_juntas = ''.join(palavras) # Todas as palavras juntas, sem separador entre elas

    return palavras + [palavras_juntas] # Devolve a lista com as palavras e, no fim, todas elas juntas
