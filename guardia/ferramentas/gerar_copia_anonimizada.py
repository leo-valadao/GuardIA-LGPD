from guardia.banco.conexao.verificar_se_banco_existe import verificar_se_banco_existe # Importa a função que diz se um banco já existe
from guardia.banco.conexao.constantes import PORTA_PADRAO # Importa a porta padrão do PostgreSQL
from guardia.banco.conexao.criar_engine_de_origem import criar_engine_de_origem # Importa a função que abre o banco original só para leitura
from guardia.banco.conexao.sugerir_nome_do_destino import sugerir_nome_do_destino # Importa a função que sugere o nome do banco de cópia
from guardia.banco.conexao.ocultar_senha_da_url import ocultar_senha_da_url # Importa a função que esconde a senha da URL
from guardia.banco.copia.analisar_banco import analisar_banco # Importa a função que detecta os dados pessoais do banco
from guardia.banco.copia.gerar_copia import gerar_copia # Importa a função que cria a cópia anonimizada do banco
from guardia.relatorio.gerar_relatorio import gerar_relatorio # Importa a função que monta o relatório em Markdown
from guardia.utilitarios.montar_url_com_senha_do_ambiente import montar_url_com_senha_do_ambiente # Importa a função que monta a URL com a senha da variável de ambiente


def gerar_copia_anonimizada(host, banco, usuario, modo, porta=PORTA_PADRAO, destino=None): # Define a ferramenta, que recebe os dados de acesso, o modo e, se houver, o nome do banco de cópia
    """Cria um banco novo no mesmo servidor com os dados censurados ('mascarar') ou sintéticos."""
    url = montar_url_com_senha_do_ambiente(host, banco, usuario, porta) # Monta a URL de conexão, com a senha da variável de ambiente
    destino = destino or sugerir_nome_do_destino(url, modo) # Usa o nome informado para a cópia ou, se não houver, o nome sugerido para o modo
    if verificar_se_banco_existe(url, destino): # Confere se já existe um banco com esse nome
        return f'O banco "{destino}" já existe. Escolha outro nome em "destino".' # Devolve um aviso, sem apagar o banco que já existe
    engine = criar_engine_de_origem(url) # Abre o banco original só para leitura
    analise_do_banco = analisar_banco(engine, ocultar_senha_da_url(url)) # Detecta os dados pessoais do banco
    resultado = gerar_copia(engine, url, analise_do_banco, modo, destino, ao_progredir=lambda mensagem: None) # Cria a cópia anonimizada, sem mostrar o progresso
    return gerar_relatorio(analise_do_banco, resultado) # Monta e devolve o relatório da análise e da cópia
