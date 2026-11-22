from guardia.banco.conexao.constantes import VARIAVEL_DE_AMBIENTE_DA_SENHA # Importa o nome da variável de ambiente que guarda a senha
from guardia.excecoes.erro_do_guardia import ErroDoGuardia # Importa a exceção-mãe de todos os erros do GuardIA


class SenhaNaoInformada(ErroDoGuardia):
    """
    A senha do banco não foi definida na variável de ambiente PGPASSWORD.

    Usada pelas ferramentas da IA (pasta ferramentas/): a senha nunca deve ser
    enviada para a IA, então ela precisa vir dessa variável.
    """

    def __init__(self):
        """Monta a mensagem do erro, que não precisa de nenhum valor."""
        super().__init__(f'Defina a variável de ambiente {VARIAVEL_DE_AMBIENTE_DA_SENHA} com a senha do banco antes de usar a ferramenta. A senha não deve ser enviada para a IA.') # Monta a mensagem do erro com o __init__ da exceção-mãe
