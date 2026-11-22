class ErroDoGuardia(Exception):
    """
    Exceção-mãe de todos os erros do GuardIA.

    A mensagem de cada erro já vem pronta para mostrar ao usuário:
        except ErroDoGuardia as erro:
            print(erro)
    """
