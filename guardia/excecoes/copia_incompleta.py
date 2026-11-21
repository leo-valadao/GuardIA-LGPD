from guardia.excecoes.erro_do_guardia import ErroDoGuardia # Importa a exceção-mãe de todos os erros do GuardIA


class CopiaIncompleta(ErroDoGuardia): # Define o erro como um tipo de ErroDoGuardia
    """
    A cópia de uma tabela ficou com uma quantidade de linhas diferente da origem.
    Quando isso acontece, o banco de cópia é apagado (nada fica pela metade).
    """

    def __init__(self, tabela, linhas_copiadas, linhas_no_destino): # Define o que acontece ao criar o erro, que recebe a tabela e as duas contagens de linhas
        self.tabela = tabela # Guarda o nome da tabela dentro do erro
        self.linhas_copiadas = linhas_copiadas # Guarda quantas linhas foram copiadas
        self.linhas_no_destino = linhas_no_destino # Guarda quantas linhas ficaram no banco de cópia
        super().__init__(f'A cópia da tabela "{tabela}" ficou incompleta: {linhas_copiadas} linhas copiadas, {linhas_no_destino} no banco de cópia. O banco de cópia foi apagado.') # Monta a mensagem do erro com o __init__ da exceção-mãe
