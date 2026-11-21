"""
CLI do GuardIA-LGPD.

Gera uma CÓPIA anonimizada do banco no mesmo servidor; o banco original só é lido:
  python cli.py --host localhost --banco guardia --usuario guardia -m sintetico
  python cli.py --url postgresql://guardia@localhost:5432/guardia -m mascarar --destino guardia_censurado
  python cli.py --host localhost --banco guardia --usuario guardia -m apenas_relatorio

A senha nunca vai na linha de comando: use a variável de ambiente PGPASSWORD ou
digite quando ela for pedida (não aparece na tela).
"""
import argparse # Importa o módulo argparse, que lê as opções escritas na linha de comando

from guardia.banco.conexao.verificar_se_banco_existe import verificar_se_banco_existe # Importa a função que diz se um banco já existe
from guardia.banco.conexao.completar_senha_da_url import completar_senha_da_url # Importa a função que acrescenta a senha à URL
from guardia.banco.conexao.constantes import PORTA_PADRAO, VARIAVEL_DE_AMBIENTE_DA_SENHA # Importa a porta padrão e o nome da variável de ambiente da senha
from guardia.banco.conexao.criar_engine_de_origem import criar_engine_de_origem # Importa a função que abre o banco original só para leitura
from guardia.banco.conexao.montar_url import montar_url # Importa a função que monta a URL de conexão com o banco
from guardia.banco.conexao.sugerir_nome_do_destino import sugerir_nome_do_destino # Importa a função que sugere o nome do banco de cópia
from guardia.banco.conexao.converter_texto_em_url import converter_texto_em_url # Importa a função que lê uma URL escrita como texto
from guardia.banco.conexao.ocultar_senha_da_url import ocultar_senha_da_url # Importa a função que esconde a senha da URL
from guardia.banco.copia.analisar_banco import analisar_banco # Importa a função que detecta os dados pessoais do banco
from guardia.banco.copia.gerar_copia import gerar_copia # Importa a função que cria a cópia anonimizada do banco
from guardia.enumeracoes.modo_de_anonimizacao import ModoDeAnonimizacao # Importa o enum com os modos de anonimização
from guardia.excecoes.destino_igual_a_origem import DestinoIgualAOrigem # Importa o erro lançado quando a cópia teria o nome do banco original
from guardia.relatorio.constantes import ARQUIVO_DO_RELATORIO, CODIFICACAO_DO_RELATORIO # Importa o nome padrão do arquivo do relatório e a sua codificação
from guardia.relatorio.gerar_relatorio import gerar_relatorio # Importa a função que monta o relatório em Markdown
from guardia.relatorio.resumir_analise import resumir_analise # Importa a função que monta o resumo curto para o terminal
from guardia.terminal.executar import executar # Importa a função que roda o programa mostrando só mensagens de erro claras


# Modo só da CLI: analisa o banco e gera o relatório, sem criar a cópia
APENAS_RELATORIO = 'apenas_relatorio' # Nome da opção na linha de comando


def _criar_parser(): # Define a função privada que monta o leitor das opções da linha de comando
    parser = argparse.ArgumentParser( # Cria o leitor das opções
        description='GuardIA-LGPD CLI: análise e anonimização de bancos de dados PostgreSQL') # Descrição que aparece na ajuda (--help)
    grupo_de_acesso = parser.add_mutually_exclusive_group(required=True) # Cria um grupo em que só uma das opções pode ser usada, e uma delas é obrigatória
    grupo_de_acesso.add_argument('--url', help='postgresql://usuario@host:porta/banco (sem a senha)') # Opção --url: a URL completa do banco
    grupo_de_acesso.add_argument('--host', help='Endereço do servidor (use com --banco e --usuario)') # Opção --host: o endereço do servidor
    parser.add_argument('--porta', type=int, default=PORTA_PADRAO, help=f'Porta (padrão {PORTA_PADRAO})') # Opção --porta: um número, que por padrão é a porta do PostgreSQL
    parser.add_argument('--banco', help='Nome do banco de origem') # Opção --banco: o nome do banco
    parser.add_argument('--usuario', help='Usuário do banco') # Opção --usuario: o usuário do banco
    parser.add_argument('--modo', '-m', # Opção --modo (ou -m): o que fazer com o banco
                        choices=[ModoDeAnonimizacao.MASCARAR, ModoDeAnonimizacao.SINTETICO, APENAS_RELATORIO], # Só aceita estes três valores
                        default=ModoDeAnonimizacao.SINTETICO, help='Modo de operação') # Por padrão, gera a cópia com dados sintéticos
    parser.add_argument('--arquivo_do_relatorio', '-r', default=ARQUIVO_DO_RELATORIO, # Opção --arquivo_do_relatorio (ou -r): onde salvar o relatório
                        help='Caminho para salvar o relatório Markdown') # Texto que aparece na ajuda
    parser.add_argument('--destino', help='Nome do banco de cópia (padrão: <banco>_censurado ou <banco>_sintetico, conforme o modo)') # Opção --destino: o nome do banco de cópia
    parser.add_argument('--sobrescrever', action='store_true', # Opção --sobrescrever: sem valor; só de aparecer já fica verdadeira
                        help='Apaga o banco de destino se ele já existir (pede confirmação)') # Texto que aparece na ajuda
    parser.add_argument('--semente', type=int, # Opção --semente: um número inteiro
                        help='Mesma semente gera os mesmos dados sintéticos (resultados reprodutíveis)') # Texto que aparece na ajuda
    return parser # Devolve o leitor das opções pronto


def _salvar_relatorio(texto, caminho): # Define a função privada que recebe o relatório e o caminho do arquivo
    with open(caminho, 'w', encoding=CODIFICACAO_DO_RELATORIO) as arquivo: # Abre o arquivo para escrita; ele é fechado sozinho no fim do bloco
        arquivo.write(texto) # Escreve o relatório no arquivo
    print(f'Relatório gerado em: {caminho}') # Avisa onde o relatório foi salvo


def _confirmar_sobrescrita(nome_do_banco): # Define a função privada que recebe o nome do banco que seria apagado
    resposta = input(f'O banco "{nome_do_banco}" já existe e será APAGADO. Digite o nome dele para confirmar: ') # Pede para o usuário digitar o nome do banco
    return resposta.strip() == nome_do_banco # Devolve verdadeiro só se o usuário digitou exatamente o nome do banco


def _executar(argumentos, parser): # Define a função privada que recebe as opções lidas e o leitor das opções
    if argumentos.url: # Se o usuário informou a URL completa
        url = converter_texto_em_url(argumentos.url) # Lê a URL
        if url.password: # Confere se a URL tem senha
            parser.error('Não coloque a senha na URL (ela ficaria no histórico do terminal). ' # Mostra o erro e encerra o programa
                         f'Use a variável {VARIAVEL_DE_AMBIENTE_DA_SENHA} ou digite quando for pedida.') # Continuação da mensagem de erro
    else: # Se o usuário informou o host
        if not (argumentos.banco and argumentos.usuario): # Confere se faltou o banco ou o usuário
            parser.error('--host exige --banco e --usuario') # Mostra o erro e encerra o programa
        url = montar_url(argumentos.host, argumentos.banco, argumentos.usuario, argumentos.porta) # Monta a URL com os dados informados
    url = completar_senha_da_url(url) # Acrescenta a senha à URL

    engine = criar_engine_de_origem(url) # Abre o banco original só para leitura
    print(f'Analisando {ocultar_senha_da_url(url)} (somente leitura)...') # Avisa que a análise começou
    analise_do_banco = analisar_banco(engine, ocultar_senha_da_url(url)) # Detecta os dados pessoais do banco
    print(resumir_analise(analise_do_banco)) # Mostra o resumo da análise

    resultado = None # Ainda não há cópia
    if argumentos.modo != APENAS_RELATORIO: # Se o modo pede uma cópia do banco
        destino = argumentos.destino or sugerir_nome_do_destino(url, argumentos.modo) # Usa o nome informado para a cópia ou, se não houver, o nome sugerido para o modo
        if destino == url.database: # Confere se o nome da cópia é igual ao do banco original
            raise DestinoIgualAOrigem(destino) # Lança o erro, para o banco original nunca ser apagado
        if verificar_se_banco_existe(url, destino): # Confere se já existe um banco com esse nome
            if not argumentos.sobrescrever: # Se não foi autorizado apagá-lo
                print(f'O banco "{destino}" já existe. Use --destino com outro nome ou --sobrescrever.') # Explica o que fazer
                return 1 # Encerra com o código 1 (não terminou bem)
            if not _confirmar_sobrescrita(destino): # Pede a confirmação; se o usuário não confirmar
                print('Operação cancelada.') # Avisa que cancelou
                return 1 # Encerra com o código 1 (não terminou bem)
        print(f'Gerando a cópia "{destino}" ({argumentos.modo})...') # Avisa que a cópia começou
        resultado = gerar_copia(engine, url, analise_do_banco, argumentos.modo, destino, # Cria a cópia anonimizada do banco
                                sobrescrever=argumentos.sobrescrever, semente=argumentos.semente) # Informa se pode apagar o banco antigo e a semente
        print(f'Cópia criada: {resultado.destino}') # Avisa que a cópia foi criada, com o endereço dela

    _salvar_relatorio(gerar_relatorio(analise_do_banco, resultado), argumentos.arquivo_do_relatorio) # Monta o relatório e salva no arquivo
    return 0 # Encerra com o código 0 (terminou bem)


def main(lista_de_argumentos=None): # Define a função principal, que pode receber as opções (sem elas, lê da linha de comando)
    parser = _criar_parser() # Monta o leitor das opções
    return _executar(parser.parse_args(lista_de_argumentos), parser) # Lê as opções, roda o programa e devolve o código de saída


if __name__ == '__main__': # Confere se este arquivo foi executado direto (e não importado por outro)
    executar(main) # Roda a função principal, mostrando só mensagens de erro claras
