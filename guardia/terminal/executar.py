import sys # Importa o módulo sys, usado no fim para encerrar o programa com um código de saída

from guardia.terminal.configurar_terminal import configurar_terminal # Importa a função que acerta os acentos no terminal


def _extrair_mensagem_do_banco(erro): # Define a função privada que recebe o erro do banco
    """A mensagem de erro do PostgreSQL, sem os detalhes técnicos do driver."""
    detalhes = erro.orig.args[0] if erro.orig.args else erro.orig # Pega os detalhes que o driver guardou dentro do erro
    if isinstance(detalhes, dict): # Confere se os detalhes vieram num dicionário
        # O pg8000 entrega os campos do erro do PostgreSQL num dicionário; 'M' é a mensagem
        return detalhes.get('M', str(detalhes)) # Devolve a mensagem; se ela não existir, devolve o dicionário como texto
    return str(detalhes).strip().splitlines()[0] # Devolve só a primeira linha do texto do erro, sem espaços nas pontas


def executar(funcao_principal): # Define a função, que recebe a função principal do programa (o main)
    """
    Roda o programa e, se ele for cancelado ou der erro, mostra só uma mensagem clara.
    Assim o usuário não vê o erro técnico (traceback) quando:
      - o usuário aperta Ctrl+C ou fecha a entrada (Ctrl+Z/Ctrl+D, botão Stop do IntelliJ);
      - o GuardIA lança um dos seus erros (pasta guardia/excecoes);
      - o banco recusa algo (senha errada, servidor fora do ar, falta de permissão).
    """
    from sqlalchemy.exc import DBAPIError # Importa o tipo de erro que o SQLAlchemy usa quando o banco recusa algo

    from guardia.excecoes.erro_do_guardia import ErroDoGuardia # Importa a exceção-mãe de todos os erros do GuardIA

    configurar_terminal() # Acerta os acentos do terminal antes de qualquer print
    try: # Tenta rodar o bloco abaixo; se der erro, cai num dos except
        codigo_de_saida = funcao_principal() # Roda o programa e guarda o código que ele devolve
    except (KeyboardInterrupt, EOFError): # Se o usuário cancelou (Ctrl+C) ou fechou a entrada
        print('\nOperação cancelada.') # Avisa que a operação foi cancelada
        codigo_de_saida = 1 # O código 1 avisa ao sistema que o programa não terminou bem
    except ErroDoGuardia as erro: # Se o GuardIA lançou um dos seus erros
        print(f'Erro: {erro}') # Mostra a mensagem do erro
        codigo_de_saida = 1 # O código 1 avisa ao sistema que o programa não terminou bem
    except DBAPIError as erro: # Se o banco de dados recusou algo
        print(f'Erro no banco de dados: {_extrair_mensagem_do_banco(erro)}') # Mostra só a mensagem do banco
        codigo_de_saida = 1 # O código 1 avisa ao sistema que o programa não terminou bem
    sys.exit(codigo_de_saida or 0) # Encerra o programa; sem código, usa 0, que significa "terminou bem"
