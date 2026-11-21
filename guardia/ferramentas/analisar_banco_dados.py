from guardia.banco.conexao.constantes import PORTA_PADRAO # Importa a porta padrão do PostgreSQL
from guardia.banco.conexao.criar_engine_de_origem import criar_engine_de_origem # Importa a função que abre o banco original só para leitura
from guardia.banco.conexao.ocultar_senha_da_url import ocultar_senha_da_url # Importa a função que esconde a senha da URL
from guardia.banco.copia.analisar_banco import analisar_banco # Importa a função que detecta os dados pessoais do banco
from guardia.relatorio.gerar_relatorio import gerar_relatorio # Importa a função que monta o relatório em Markdown
from guardia.utilitarios.montar_url_com_senha_do_ambiente import montar_url_com_senha_do_ambiente # Importa a função que monta a URL com a senha da variável de ambiente


def analisar_banco_dados(host, banco, usuario, porta=PORTA_PADRAO): # Define a ferramenta, que recebe os dados de acesso ao banco
    """Analisa o banco (somente leitura) e retorna o relatório de riscos em Markdown."""
    url = montar_url_com_senha_do_ambiente(host, banco, usuario, porta) # Monta a URL de conexão, com a senha da variável de ambiente
    analise_do_banco = analisar_banco(criar_engine_de_origem(url), ocultar_senha_da_url(url)) # Abre o banco só para leitura e detecta os dados pessoais
    return gerar_relatorio(analise_do_banco) # Monta e devolve o relatório
