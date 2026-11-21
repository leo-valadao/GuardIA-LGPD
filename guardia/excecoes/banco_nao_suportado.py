from guardia.excecoes.erro_do_guardia import ErroDoGuardia # Importa a exceção-mãe de todos os erros do GuardIA


class BancoNaoSuportado(ErroDoGuardia): # Define o erro como um tipo de ErroDoGuardia
    """A URL de conexão é de um banco que o GuardIA ainda não suporta (só PostgreSQL)."""

    def __init__(self, tipo_do_banco): # Define o que acontece ao criar o erro, que recebe o tipo do banco da URL
        self.tipo_do_banco = tipo_do_banco # Guarda o tipo do banco dentro do erro
        super().__init__(f'Por enquanto o GuardIA só trabalha com PostgreSQL (a URL é de "{tipo_do_banco}").') # Monta a mensagem do erro com o __init__ da exceção-mãe
