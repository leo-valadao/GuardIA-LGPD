from guardia.enumeracoes.modo_de_anonimizacao import ModoDeAnonimizacao # Importa o enum com os modos válidos
from guardia.excecoes.erro_do_guardia import ErroDoGuardia # Importa a exceção-mãe de todos os erros do GuardIA


class ModoInvalido(ErroDoGuardia): # Define o erro como um tipo de ErroDoGuardia
    """O modo da cópia não é 'mascarar' (censura) nem 'sintetico' (dados sintéticos)."""

    def __init__(self, modo): # Define o que acontece ao criar o erro, que recebe o modo que foi informado
        self.modo = modo # Guarda o modo informado dentro do erro
        super().__init__(f'Modo inválido: "{modo}". Use "{ModoDeAnonimizacao.MASCARAR}" ' # Monta a mensagem do erro com o __init__ da exceção-mãe
                         f'ou "{ModoDeAnonimizacao.SINTETICO}".') # Continuação da mensagem, com o segundo modo válido
