from guardia.relatorio.rotulos import ROTULOS_DOS_TIPOS # Importa o nome de cada tipo de dado para mostrar ao usuário


def resumir_analise(analise_do_banco):
    """Resumo curto para o terminal: colunas e textos com dados pessoais, por tabela."""
    linhas = [] # Lista que vai guardar as linhas do resumo
    for analise_da_tabela in analise_do_banco.tabelas: # Passa pela análise de cada tabela
        itens = [f'{coluna} ({ROTULOS_DOS_TIPOS.get(achado.tipo, achado.tipo)})' # Monta o texto de cada coluna com dado pessoal: o nome dela e o tipo de dado
                 for coluna, achado in analise_da_tabela.colunas.items()] # Passa por cada coluna com dado pessoal detectado
        itens += [f'{coluna} (texto livre: {", ".join(ROTULOS_DOS_TIPOS.get(tipo, tipo) for tipo in tipos)})' # Monta o texto de cada coluna de texto livre: o nome dela e os tipos achados no texto
                  for coluna, tipos in analise_da_tabela.dados_encontrados_nos_textos.items()] # Passa por cada coluna de texto livre com dados pessoais
        if itens: # Confere se a tabela tem alguma coluna com dado pessoal
            linhas.append(f'  - {analise_da_tabela.nome}: ' + ', '.join(itens)) # Acrescenta a linha da tabela, com as colunas separadas por vírgula
        for coluna, categoria in analise_da_tabela.avisos: # Passa por cada coluna com possível dado sensível não tratado
            linhas.append(f'  ! {analise_da_tabela.nome}.{coluna}: possível dado sensível ({categoria}), não tratado') # Acrescenta a linha de aviso
    if not linhas: # Confere se nenhuma tabela tem dado pessoal
        return 'Nenhum dado pessoal encontrado.' # Devolve o aviso de que nada foi encontrado
    return 'Dados pessoais encontrados:\n' + '\n'.join(linhas) # Devolve o título e as linhas do resumo, uma embaixo da outra
