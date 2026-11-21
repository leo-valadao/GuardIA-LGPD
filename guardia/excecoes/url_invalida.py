from guardia.excecoes.erro_do_guardia import ErroDoGuardia # Importa a exceção-mãe de todos os erros do GuardIA


class UrlInvalida(ErroDoGuardia): # Define o erro como um tipo de ErroDoGuardia
    """A URL de conexão não está no formato postgresql://usuario@host:porta/banco."""

    def __init__(self, motivo): # Define o que acontece ao criar o erro, que recebe o motivo
        self.motivo = motivo # Guarda o motivo dentro do erro
        super().__init__(f'URL de conexão inválida: {motivo}. Formato esperado: postgresql://usuario@host:porta/banco') # Monta a mensagem do erro com o __init__ da exceção-mãe
