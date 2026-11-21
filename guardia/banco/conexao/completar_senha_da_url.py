import os # Importa o módulo os, que dá acesso às variáveis de ambiente do sistema

from guardia.banco.conexao.constantes import VARIAVEL_DE_AMBIENTE_DA_SENHA # Importa o nome da variável de ambiente que guarda a senha
from guardia.banco.conexao.pedir_senha import pedir_senha # Importa a função que pede a senha ao usuário


def completar_senha_da_url(url): # Define a função, que recebe a URL de conexão
    """Pede a senha (ou usa PGPASSWORD) quando a URL não tem senha."""
    if url.password: # Confere se a URL já tem senha
        return url # Devolve a URL como está
    senha = os.environ.get(VARIAVEL_DE_AMBIENTE_DA_SENHA) # Lê a senha da variável de ambiente; se ela não existir, fica None
    if senha is None: # Confere se a variável de ambiente não foi definida
        senha = pedir_senha(f'Senha de {url.username}@{url.host}: ') # Pede a senha ao usuário
    return url.set(password=senha) # Devolve uma cópia da URL com a senha
