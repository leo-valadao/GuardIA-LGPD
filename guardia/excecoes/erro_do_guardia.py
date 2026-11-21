class ErroDoGuardia(Exception): # Define a exceção-mãe do GuardIA como um tipo de Exception, a exceção-mãe do Python
    """
    Exceção-mãe de todos os erros do GuardIA.

    A mensagem de cada erro já vem pronta para mostrar ao usuário:
        except ErroDoGuardia as erro:
            print(erro)
    """
