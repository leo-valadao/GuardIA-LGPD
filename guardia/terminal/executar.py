import sys # Importa o módulo sys, usado no fim para encerrar o programa com um código de saída

from guardia.terminal.configurar_terminal import configurar_terminal # Importa a função que acerta os acentos no terminal


def executar(funcao_principal):
    """
    Roda o programa e, se ele for cancelado ou der erro, mostra só uma mensagem clara.
    Assim o usuário não vê o erro técnico (traceback) quando:
      - o usuário aperta Ctrl+C ou fecha a entrada (Ctrl+Z/Ctrl+D, botão Stop do IntelliJ);
      - o GuardIA lança um dos seus erros (pasta guardia/excecoes);
      - o banco recusa algo (senha errada, servidor fora do ar, falta de permissão).
    """
    from sqlalchemy.exc import DBAPIError # Importa o tipo de erro que o SQLAlchemy usa quando o banco recusa algo

    from guardia.excecoes.erro_do_guardia import ErroDoGuardia # Importa a exceção-mãe de todos os erros do GuardIA

    configurar_terminal() # Acerta os acentos do terminal antes de qualquer captura de tela
    try: # Tenta rodar o bloco abaixo; se der erro, cai num dos except
        codigo_de_saida = funcao_principal() # Roda o programa e guarda o código que ele devolve

    except ErroDoGuardia as erro: # Se o GuardIA lançou um dos seus erros
        codigo_de_saida = _mostrar_mensagem_de_falha(f'Erro: {erro}') # Mostra a mensagem do erro e guarda o código 1

    except (KeyboardInterrupt, EOFError): # Se o usuário cancelou (Ctrl+C) ou fechou a entrada
        codigo_de_saida = _mostrar_mensagem_de_falha('\nOperação cancelada.') # Avisa que a operação foi cancelada e guarda o código 1

    except DBAPIError as erro: # Se o banco de dados recusou algo
        codigo_de_saida = _mostrar_mensagem_de_falha(f'Erro no banco de dados: {_extrair_mensagem_do_banco(erro)}') # Mostra só a mensagem do banco e guarda o código 1

    sys.exit(codigo_de_saida or 0) # Encerra o programa; sem código, usa 0, que significa "terminou bem"


def _extrair_mensagem_do_banco(erro):
    """A mensagem de erro do PostgreSQL, sem os detalhes técnicos do driver."""
    detalhes = erro.orig.args[0] if erro.orig.args else erro.orig # Pega os detalhes que o driver guardou dentro do erro
    if isinstance(detalhes, dict): # Confere se os detalhes vieram num dicionário
        # O pg8000 entrega os campos do erro do PostgreSQL num dicionário; 'M' é a mensagem
        return detalhes.get('M', str(detalhes)) # Devolve a mensagem; se ela não existir, devolve o dicionário como texto
    return str(detalhes).strip().splitlines()[0] # Devolve só a primeira linha do texto do erro, sem espaços nas pontas


def _mostrar_mensagem_de_falha(mensagem):
    """Mostra a mensagem e devolve o código de saída 1, que avisa ao sistema que o programa não terminou bem."""
    print(mensagem) # Mostra a mensagem na tela
    return 1 # Devolve o código 1, que avisa ao sistema que o programa não terminou bem
