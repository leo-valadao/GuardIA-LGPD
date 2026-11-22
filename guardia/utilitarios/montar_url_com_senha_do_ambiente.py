import os # Importa o módulo os, que dá acesso às variáveis de ambiente do sistema

from guardia.banco.conexao.constantes import VARIAVEL_DE_AMBIENTE_DA_SENHA # Importa o nome da variável de ambiente que guarda a senha
from guardia.banco.conexao.montar_url import montar_url # Importa a função que monta a URL de conexão com o banco
from guardia.excecoes.senha_nao_informada import SenhaNaoInformada # Importa o erro lançado quando a senha não foi definida


def montar_url_com_senha_do_ambiente(host, banco, usuario, porta):
    """URL de conexão com a senha lida da variável PGPASSWORD (usada pelas ferramentas da IA)."""
    senha = os.environ.get(VARIAVEL_DE_AMBIENTE_DA_SENHA) # Lê a senha da variável de ambiente; se ela não existir, fica None

    if senha is None: # Confere se a variável de ambiente não foi definida
        raise SenhaNaoInformada() # Lança o erro avisando que falta definir a senha

    return montar_url(host, banco, usuario, porta, senha=senha) # Monta e devolve a URL de conexão com a senha
