from guardia.excecoes.erro_do_guardia import ErroDoGuardia # Importa a exceção-mãe de todos os erros do GuardIA


class NomeDeBancoInvalido(ErroDoGuardia): # Define o erro como um tipo de ErroDoGuardia
    """O nome do banco de cópia não segue o padrão aceito pelo GuardIA."""

    def __init__(self, nome_do_banco): # Define o que acontece ao criar o erro, que recebe o nome do banco
        self.nome_do_banco = nome_do_banco # Guarda o nome do banco dentro do erro
        super().__init__(f'Nome de banco inválido: "{nome_do_banco}". Use letras minúsculas, números e "_" (começando por letra ou "_", até 63 caracteres).') # Monta a mensagem do erro com o __init__ da exceção-mãe
