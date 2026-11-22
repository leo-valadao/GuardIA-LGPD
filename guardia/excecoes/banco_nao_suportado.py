from guardia.excecoes.erro_do_guardia import ErroDoGuardia # Importa a exceção-mãe de todos os erros do GuardIA


class BancoNaoSuportado(ErroDoGuardia):
    """A URL de conexão é de um banco que o GuardIA ainda não suporta (só PostgreSQL)."""

    def __init__(self, tipo_do_banco):
        """Guarda o tipo do banco da URL e monta a mensagem do erro."""
        self.tipo_do_banco = tipo_do_banco # Guarda o tipo do banco dentro do erro
        super().__init__(f'Por enquanto o GuardIA só trabalha com PostgreSQL (a URL é de "{tipo_do_banco}").') # Monta a mensagem do erro com o __init__ da exceção-mãe
