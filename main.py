import sys # Importa o módulo sys, usado para encerrar o programa

from guardia.banco.conexao.verificar_se_banco_existe import verificar_se_banco_existe # Importa a função que diz se um banco já existe
from guardia.banco.conexao.criar_engine_de_origem import criar_engine_de_origem # Importa a função que abre o banco original só para leitura
from guardia.banco.conexao.ler_dados_de_conexao import ler_dados_de_conexao # Importa a função que pergunta os dados de acesso ao banco
from guardia.banco.conexao.sugerir_nome_do_destino import sugerir_nome_do_destino # Importa a função que sugere o nome do banco de cópia
from guardia.banco.conexao.ocultar_senha_da_url import ocultar_senha_da_url # Importa a função que esconde a senha da URL
from guardia.banco.copia.analisar_banco import analisar_banco # Importa a função que detecta os dados pessoais do banco
from guardia.banco.copia.gerar_copia import gerar_copia # Importa a função que cria a cópia anonimizada do banco
from guardia.enumeracoes.modo_de_anonimizacao import ModoDeAnonimizacao # Importa o enum com os modos de anonimização
from guardia.enumeracoes.opcao_do_menu import OpcaoDoMenu # Importa o enum com as opções do menu
from guardia.excecoes.destino_igual_a_origem import DestinoIgualAOrigem # Importa o erro lançado quando a cópia teria o nome do banco original
from guardia.relatorio.constantes import ARQUIVO_DO_RELATORIO, CODIFICACAO_DO_RELATORIO # Importa o nome do arquivo do relatório e a sua codificação
from guardia.relatorio.gerar_relatorio import gerar_relatorio # Importa a função que monta o relatório em Markdown
from guardia.relatorio.resumir_analise import resumir_analise # Importa a função que monta o resumo curto para o terminal
from guardia.terminal.executar import executar # Importa a função que roda o programa mostrando só mensagens de erro claras


# Modo de anonimização de cada opção do menu que gera uma cópia do banco
_MODO_DE_CADA_OPCAO = { # Cria o dicionário: cada opção do menu e o modo de anonimização dela
    OpcaoDoMenu.GERAR_COPIA_CENSURADA: ModoDeAnonimizacao.MASCARAR, # A opção 2 gera a cópia censurada
    OpcaoDoMenu.GERAR_COPIA_SINTETICA: ModoDeAnonimizacao.SINTETICO, # A opção 3 gera a cópia com dados sintéticos
}


def _perguntar_tarefa(): # Define a função privada que mostra o menu e pergunta a opção
    print("\n[Passo 2] O que você deseja fazer com esses dados?") # Mostra a pergunta
    print(f"{OpcaoDoMenu.GERAR_RELATORIO} - Gerar Relatório de Riscos (Markdown)") # Mostra a opção 1
    print(f"{OpcaoDoMenu.GERAR_COPIA_CENSURADA} - Gerar cópia do banco com os dados CENSURADOS (substituir por *)") # Mostra a opção 2
    print(f"{OpcaoDoMenu.GERAR_COPIA_SINTETICA} - Gerar cópia do banco com DADOS SINTÉTICOS (dados falsos e coerentes)") # Mostra a opção 3
    print(f"{OpcaoDoMenu.SAIR} - Sair") # Mostra a opção 4
    return input("\nDigite o número da tarefa desejada: ").strip() # Lê a opção digitada, sem espaços nas pontas, e a devolve


def main(): # Define a função principal do modo interativo
    print("=== GuardIA-LGPD (Modo Interativo) ===") # Mostra o título do programa
    url = ler_dados_de_conexao() # Pergunta os dados de acesso ao banco
    engine = criar_engine_de_origem(url) # Abre o banco original só para leitura
    print(f"\n[Passo 1] Analisando {ocultar_senha_da_url(url)} (somente leitura)...") # Avisa que a análise começou
    analise_do_banco = analisar_banco(engine, ocultar_senha_da_url(url)) # Detecta os dados pessoais do banco

    print(resumir_analise(analise_do_banco)) # Mostra o resumo da análise
    if not any(analise_da_tabela.colunas or analise_da_tabela.dados_encontrados_nos_textos # Confere se nenhuma tabela tem dado pessoal
               for analise_da_tabela in analise_do_banco.tabelas): # Passa pela análise de cada tabela
        sys.exit(0) # Sem dados pessoais, não há o que fazer: encerra o programa

    escolha = _perguntar_tarefa() # Mostra o menu e lê a opção escolhida
    resultado = None # Ainda não há cópia
    if escolha in _MODO_DE_CADA_OPCAO: # Se a opção escolhida gera uma cópia do banco
        modo = _MODO_DE_CADA_OPCAO[escolha] # Pega o modo de anonimização da opção
        nome_sugerido = sugerir_nome_do_destino(url) # Sugere o nome do banco de cópia
        destino = input(f"Nome do banco de cópia [{nome_sugerido}]: ").strip() or nome_sugerido # Pergunta o nome da cópia; com Enter, usa o sugerido
        if destino == url.database: # Confere se o nome da cópia é igual ao do banco original
            raise DestinoIgualAOrigem(destino) # Lança o erro, para o banco original nunca ser apagado
        sobrescrever = False # Por padrão, não apaga nenhum banco que já existe
        if verificar_se_banco_existe(url, destino): # Confere se já existe um banco com esse nome
            resposta = input(f'O banco "{destino}" já existe e será APAGADO. Digite o nome dele para confirmar: ') # Pede para o usuário digitar o nome do banco
            if resposta.strip() != destino: # Se o usuário não digitou exatamente o nome do banco
                print("Operação cancelada.") # Avisa que cancelou
                sys.exit(1) # Encerra o programa com o código 1 (não terminou bem)
            sobrescrever = True # O usuário confirmou: pode apagar o banco antigo
        print(f"\nGerando a cópia \"{destino}\"...") # Avisa que a cópia começou
        resultado = gerar_copia(engine, url, analise_do_banco, modo, destino, sobrescrever=sobrescrever) # Cria a cópia anonimizada do banco
        print(f"Cópia criada: {resultado.destino}") # Avisa que a cópia foi criada, com o endereço dela
    elif escolha != OpcaoDoMenu.GERAR_RELATORIO: # Se a opção não é a de gerar o relatório (sair ou opção inválida)
        print("Operação encerrada.") # Avisa que o programa vai encerrar
        return # Sai da função sem gerar o relatório

    with open(ARQUIVO_DO_RELATORIO, "w", encoding=CODIFICACAO_DO_RELATORIO) as arquivo: # Abre o arquivo do relatório para escrita; ele é fechado sozinho no fim do bloco
        arquivo.write(gerar_relatorio(analise_do_banco, resultado)) # Monta o relatório e escreve no arquivo
    print(f"\nRelatório salvo em: {ARQUIVO_DO_RELATORIO} (abra no IntelliJ ou em um visualizador de Markdown)") # Avisa onde o relatório foi salvo


if __name__ == "__main__": # Confere se este arquivo foi executado direto (e não importado por outro)
    executar(main) # Roda a função principal, mostrando só mensagens de erro claras
