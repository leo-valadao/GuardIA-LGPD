import getpass # Importa o módulo getpass, que lê a senha sem mostrá-la na tela
import sys # Importa o módulo sys, que dá acesso à entrada do programa

from guardia.banco.conexao.constantes import VARIAVEL_DE_AMBIENTE_DA_SENHA # Importa o nome da variável de ambiente que guarda a senha


def pedir_senha(pergunta):
    """
    Lê a senha sem mostrá-la na tela (getpass).

    O getpass só funciona num terminal de verdade (PowerShell, cmd, terminal do
    IntelliJ). No console de execução/debug do IntelliJ ele não mostra a pergunta
    nem lê o que é digitado, e o programa fica parado esperando. Nesse caso a senha
    é lida normalmente, com um aviso de que ela vai aparecer na tela.
    """
    if sys.stdin.isatty(): # Confere se o programa está num terminal de verdade
        return getpass.getpass(pergunta) # Pede a senha sem mostrar o que é digitado e a devolve
    print('Atenção: este console não consegue esconder a senha; ela vai aparecer na tela.') # Avisa que a senha vai aparecer
    print(f'Para escondê-la, rode no terminal ou defina a variável de ambiente {VARIAVEL_DE_AMBIENTE_DA_SENHA}.') # Diz como evitar que a senha apareça
    return input(pergunta) # Pede a senha do jeito normal e a devolve
