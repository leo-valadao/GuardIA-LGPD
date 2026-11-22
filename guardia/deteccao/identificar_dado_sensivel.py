from guardia.utilitarios.dividir_nome_da_coluna_em_palavras import dividir_nome_da_coluna_em_palavras # Importa a função que separa o nome da coluna em palavras


# Dados pessoais SENSÍVEIS (Art. 5.º, II) ficam fora dos 7 tipos do protótipo:
# só geram aviso no relatório, pelo nome da coluna.
TERMOS_DE_DADOS_SENSIVEIS = { # Cria o dicionário: categoria de dado sensível e os começos de palavra que a indicam
    'saúde':                         ('sangu', 'saude', 'doenc', 'diagnost', 'medic', 'alergi'), # Termos de dados de saúde
    'filiação a sindicato':          ('sindic',), # Termo de filiação a sindicato
    'convicção religiosa':           ('religi',), # Termo de religião
    'origem racial ou étnica':       ('etni', 'raca'), # Termos de raça e etnia
    'opinião política':              ('politic', 'partido'), # Termos de política
    'dado genético ou biométrico':   ('biometr', 'genetic', 'dna'), # Termos de dados genéticos e biométricos
    'vida sexual':                   ('sexual' , 'orientacao'), # Termos de vida sexual
}


def identificar_dado_sensivel(nome_da_coluna):
    """Categoria de dado sensível sugerida pelo nome da coluna, ou None."""
    palavras = dividir_nome_da_coluna_em_palavras(nome_da_coluna) # Separa o nome da coluna em palavras

    for categoria, termos in TERMOS_DE_DADOS_SENSIVEIS.items(): # Passa por cada categoria e pelos seus termos
        if any(palavra.startswith(termo) for palavra in palavras for termo in termos): # Confere se alguma palavra do nome começa com algum termo da categoria
            return categoria # Devolve a categoria encontrada

    return None # Nenhuma categoria combinou: devolve None (nada)
