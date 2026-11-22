from guardia.excecoes.erro_do_guardia import ErroDoGuardia # Importa a exceção-mãe de todos os erros do GuardIA


class DestinoIgualAOrigem(ErroDoGuardia):
    """O banco de cópia teria o mesmo nome do banco original (ele seria apagado)."""

    def __init__(self, nome_do_banco):
        """Guarda o nome do banco e monta a mensagem do erro."""
        self.nome_do_banco = nome_do_banco # Guarda o nome do banco dentro do erro
        super().__init__(f'O banco de cópia não pode ter o mesmo nome do banco de origem ("{nome_do_banco}").') # Monta a mensagem do erro com o __init__ da exceção-mãe
