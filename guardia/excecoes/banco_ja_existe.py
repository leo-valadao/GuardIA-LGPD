from guardia.excecoes.erro_do_guardia import ErroDoGuardia # Importa a exceção-mãe de todos os erros do GuardIA


class BancoJaExiste(ErroDoGuardia):
    """O banco de destino já existe e não foi autorizado sobrescrever."""

    def __init__(self, nome_do_banco):
        """Guarda o nome do banco e monta a mensagem do erro."""
        self.nome_do_banco = nome_do_banco # Guarda o nome do banco dentro do erro
        super().__init__(f'O banco "{nome_do_banco}" já existe.') # Monta a mensagem do erro com o __init__ da exceção-mãe
