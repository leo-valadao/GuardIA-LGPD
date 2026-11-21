from guardia.excecoes.erro_do_guardia import ErroDoGuardia # Importa a exceção-mãe de todos os erros do GuardIA


class DadosDeConexaoInvalidos(ErroDoGuardia): # Define o erro como um tipo de ErroDoGuardia
    """Faltou informar o banco ou o usuário, ou a porta não é um número."""

    def __init__(self, motivo): # Define o que acontece ao criar o erro, que recebe o motivo
        self.motivo = motivo # Guarda o motivo dentro do erro
        super().__init__(f'Dados de conexão inválidos: {motivo}') # Monta a mensagem do erro com o __init__ da exceção-mãe
