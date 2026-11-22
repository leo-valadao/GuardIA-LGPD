import os # Importa o módulo os, que dá acesso às variáveis de ambiente do sistema
import sys # Importa o módulo sys, que dá acesso ao sistema operacional e às saídas do programa


PAGINA_DE_CODIGO_UTF8 = 65001 # Número que o Windows usa para identificar a codificação UTF-8

# Variáveis de ambiente que indicam que o terminal já lê o texto em UTF-8
VARIAVEIS_DE_TERMINAL_EM_UTF8 = ( # Cria uma tupla (lista que não muda) com os nomes dessas variáveis
    'PYTHONIOENCODING',     # A codificação já foi escolhida (o IntelliJ faz isso)
    'PYCHARM_HOSTED',       # Console de execução do IntelliJ/PyCharm
    'TERM',                 # Git Bash, MSYS e Cygwin
    'MSYSTEM',              # Git Bash e MSYS
)


def configurar_terminal():
    """
    Ajusta a saída do programa para os acentos aparecerem certos em qualquer terminal.
    Chame no começo do programa, antes de qualquer print.
    """
    # No Linux/macOS e nos terminais da lista acima o texto já sai certo: não há nada a ajustar
    if sys.platform != 'win32' or any(os.environ.get(variavel) for variavel in VARIAVEIS_DE_TERMINAL_EM_UTF8): # Confere se não é Windows ou se alguma das variáveis está preenchida
        return # Sai da função sem mudar nada

    import ctypes # Importa o módulo ctypes, que permite chamar funções do próprio Windows

    pagina_de_codigo = ctypes.windll.kernel32.GetConsoleOutputCP() # Pergunta ao Windows qual codificação o console está usando

    if not pagina_de_codigo or pagina_de_codigo == PAGINA_DE_CODIGO_UTF8: # Confere se não há console ou se ele já usa UTF-8
        return # Sem console, ou o console já está em UTF-8

    for saida in (sys.stdout, sys.stderr): # Passa pelas duas saídas do programa: a normal e a de erros
        if not saida.isatty(): # Confere se a saída vai para um pipe ou arquivo, e não direto para o console
            saida.reconfigure(encoding=f'cp{pagina_de_codigo}', errors='replace') # Passa a escrever na codificação do console; caractere que não existe nela vira '?'
