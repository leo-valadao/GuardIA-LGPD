from guardia.banco.conexao.completar_senha_da_url import completar_senha_da_url # Importa a função que acrescenta a senha à URL
from guardia.banco.conexao.constantes import HOST_PADRAO, PORTA_PADRAO # Importa o endereço e a porta padrão do servidor
from guardia.banco.conexao.montar_url import montar_url # Importa a função que monta a URL de conexão com o banco
from guardia.banco.conexao.converter_texto_em_url import converter_texto_em_url # Importa a função que lê uma URL escrita como texto


def ler_dados_de_conexao():
    """Pergunta os dados de acesso ao banco no terminal."""
    print('Informe o acesso ao banco de dados (Enter aceita o valor entre colchetes).') # Explica como responder às perguntas
    url_digitada = input('URL completa (opcional, ex.: postgresql://usuario@localhost:5432/banco): ').strip() # Pergunta a URL completa e tira os espaços das pontas
    if url_digitada: # Confere se o usuário digitou uma URL
        return completar_senha_da_url(converter_texto_em_url(url_digitada)) # Lê a URL, acrescenta a senha e devolve
    host = input(f'Host [{HOST_PADRAO}]: ').strip() or HOST_PADRAO # Pergunta o endereço do servidor; com Enter, usa o padrão
    porta = input(f'Porta [{PORTA_PADRAO}]: ').strip() or PORTA_PADRAO # Pergunta a porta; com Enter, usa a padrão
    banco = input('Banco: ').strip() # Pergunta o nome do banco
    usuario = input('Usuário: ').strip() # Pergunta o usuário do banco
    return completar_senha_da_url(montar_url(host, banco, usuario, porta)) # Monta a URL, acrescenta a senha e devolve
