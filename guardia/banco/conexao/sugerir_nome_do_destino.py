from guardia.enumeracoes.modo_de_anonimizacao import ModoDeAnonimizacao # Importa o enum com os modos de anonimização
from guardia.excecoes.modo_invalido import ModoInvalido # Importa o erro lançado quando o modo é inválido


# Final do nome do banco de cópia em cada modo: assim a cópia censurada e a sintética podem existir juntas
SUFIXO_DE_CADA_MODO = { # Cria o dicionário: cada modo e o final que ele acrescenta ao nome do banco
    ModoDeAnonimizacao.MASCARAR: '_censurado', # Cópia com os dados censurados por '*'
    ModoDeAnonimizacao.SINTETICO: '_sintetico', # Cópia com os dados sintéticos
}


def sugerir_nome_do_destino(url_de_origem, modo):
    """Nome padrão do banco de cópia: <banco de origem>_censurado ou <banco de origem>_sintetico, conforme o modo."""
    sufixo = SUFIXO_DE_CADA_MODO.get(modo) # Pega o final do nome do modo; aceita o enum ou o texto do modo
    if sufixo is None: # Confere se o modo não é um dos modos válidos
        raise ModoInvalido(modo) # Lança o erro de modo inválido
    return f'{url_de_origem.database}{sufixo}' # Devolve o nome do banco de origem com o final do modo
