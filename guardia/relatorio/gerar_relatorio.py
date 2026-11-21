import datetime # Importa o módulo datetime, usado para escrever a data do relatório

from guardia.classificacao.classificar_tipo_de_dado import classificar_tipo_de_dado # Importa a função que dá a classificação LGPD de um tipo de dado
from guardia.enumeracoes.forca_do_padrao import ForcaDoPadrao # Importa o enum com as forças do padrão (forte ou fraco)
from guardia.enumeracoes.modo_de_anonimizacao import ModoDeAnonimizacao # Importa o enum com os modos de anonimização
from guardia.relatorio.rotulos import ROTULOS_DOS_TIPOS # Importa o nome de cada tipo de dado para mostrar ao usuário


def _descrever_deteccao(achado): # Define a função privada que recebe o Achado de uma coluna
    """Como o dado foi detectado, em texto para o relatório (F ou W ∧ C)."""
    if achado.forca == ForcaDoPadrao.FORTE: # Se o dado foi detectado por padrão forte
        return 'F (padrão forte)' + (' + contexto' if achado.tem_contexto else ', sem contexto') # Devolve o texto do padrão forte, dizendo se também havia contexto
    return 'W ∧ C (padrão fraco + contexto)' # Senão, devolve o texto do padrão fraco com contexto


def gerar_relatorio(analise_do_banco, resultado=None): # Define a função, que recebe a análise do banco e, se houver, o resultado da cópia
    """Relatório da análise do banco e, se houver, da cópia anonimizada gerada."""
    linhas = [ # Cria a lista com as primeiras linhas do relatório
        '### Relatório de Riscos e Classificação (GuardIA-LGPD)', # Título do relatório
        '', # Linha em branco
        f'* **Banco analisado:** `{analise_do_banco.url}`', # Endereço do banco analisado, com a senha escondida
        f'* **Data:** {datetime.datetime.now():%d/%m/%Y %H:%M}', # Data e hora de agora, no formato dia/mês/ano hora:minuto
        '* Regra de detecção: D = F ∨ (W ∧ C). No banco, todo dado gravado em texto claro é ' # Explicação da regra de detecção
        'considerado exposto, então todo dado detectado é **Não conforme**.', # Continuação da explicação
        '', # Linha em branco
        '#### 1. Resumo por tabela (score de risco, equação 8)', # Título da seção 1
        '', # Linha em branco
        '| Tabela | Linhas | Colunas | Com dados pessoais | Score R | Faixa | Prioritária (R > μ + σ) |', # Cabeçalho da tabela da seção 1
        '|---|---:|---:|---:|---:|---|---|', # Linha que separa o cabeçalho das linhas da tabela, no Markdown
    ]
    tabelas_do_maior_para_o_menor_score = sorted(analise_do_banco.tabelas, # Ordena as tabelas do banco
                                                 key=lambda analise_da_tabela: -analise_da_tabela.score_de_risco) # Pelo score, do maior para o menor (o sinal de menos inverte a ordem)
    for analise_da_tabela in tabelas_do_maior_para_o_menor_score: # Passa por cada tabela, já na ordem do score
        colunas_com_dados_pessoais = (len(analise_da_tabela.colunas) # Conta as colunas com dado pessoal detectado
                                      + len(analise_da_tabela.dados_encontrados_nos_textos)) # E soma as colunas de texto livre com dados pessoais
        prioritaria = '**sim**' if analise_da_tabela.prioritaria else 'não' # Escreve "sim" em negrito se a tabela é prioritária; senão, "não"
        linhas.append(f'| {analise_da_tabela.nome} | {analise_da_tabela.total_de_linhas} ' # Acrescenta a linha da tabela: nome e quantidade de linhas
                      f'| {analise_da_tabela.total_de_colunas} | {colunas_com_dados_pessoais} ' # Quantidade de colunas e de colunas com dados pessoais
                      f'| {analise_da_tabela.score_de_risco} | {analise_da_tabela.faixa_de_risco} | {prioritaria} |') # Score, faixa de risco e se é prioritária

    linhas += ['', '#### 2. Colunas com dados pessoais', '', # Acrescenta o título da seção 2
               '| Tabela | Coluna | Tipo | Detecção | % da amostra | Risco | Classificação |', # Cabeçalho da tabela da seção 2
               '|---|---|---|---|---:|---|---|'] # Linha que separa o cabeçalho das linhas da tabela, no Markdown
    for analise_da_tabela in analise_do_banco.tabelas: # Passa pela análise de cada tabela
        for coluna, achado in analise_da_tabela.colunas.items(): # Passa por cada coluna com dado pessoal detectado
            regra = classificar_tipo_de_dado(achado.tipo) # Pega a classificação LGPD do tipo de dado
            rotulo_do_tipo = ROTULOS_DOS_TIPOS.get(achado.tipo, achado.tipo) # Pega o nome do tipo de dado para mostrar
            linhas.append(f'| {analise_da_tabela.nome} | {coluna} | {rotulo_do_tipo} | {_descrever_deteccao(achado)} | ' # Acrescenta a linha da coluna: tabela, coluna, tipo e como foi detectado
                          f'{achado.taxa:.0%} | {regra.risco} | {regra.classificacao} |') # Porcentagem da amostra, risco e classificação

    colunas_de_texto = [] # Lista que vai guardar as colunas de texto livre com dados pessoais
    for analise_da_tabela in analise_do_banco.tabelas: # Passa pela análise de cada tabela
        for coluna, tipos in analise_da_tabela.dados_encontrados_nos_textos.items(): # Passa por cada coluna de texto livre com dados pessoais
            colunas_de_texto.append((analise_da_tabela.nome, coluna, tipos)) # Guarda a tabela, a coluna e os tipos achados no texto
    if colunas_de_texto: # Confere se alguma coluna de texto livre tem dados pessoais
        linhas += ['', '#### 3. Dados pessoais dentro de textos livres (amostra)', '', # Acrescenta o título da seção 3
                   '| Tabela | Coluna | Encontrados |', '|---|---|---|'] # Cabeçalho da tabela da seção 3 e a linha que o separa
        for tabela, coluna, tipos in colunas_de_texto: # Passa por cada coluna de texto livre com dados pessoais
            dados_encontrados = ', '.join(f'{ROTULOS_DOS_TIPOS.get(tipo, tipo)}: {quantidade}' # Monta o texto com cada tipo e quantas vezes ele apareceu
                                          for tipo, quantidade in tipos.most_common()) # Do tipo que mais apareceu para o que menos apareceu
            linhas.append(f'| {tabela} | {coluna} | {dados_encontrados} |') # Acrescenta a linha da coluna

    avisos = [] # Lista que vai guardar as colunas com possível dado sensível não tratado
    for analise_da_tabela in analise_do_banco.tabelas: # Passa pela análise de cada tabela
        for coluna, categoria in analise_da_tabela.avisos: # Passa por cada aviso da tabela
            avisos.append((analise_da_tabela.nome, coluna, categoria)) # Guarda a tabela, a coluna e a categoria do dado sensível
    if avisos: # Confere se há algum aviso
        linhas += ['', '#### 4. Atenção: possíveis dados pessoais SENSÍVEIS (Art. 5º, II)', '', # Acrescenta o título da seção 4
                   'Estas colunas estão fora dos 7 tipos tratados pelo protótipo e **não foram ' # Explicação da seção 4
                   'alteradas**. Revise manualmente.', '', # Continuação da explicação
                   '| Tabela | Coluna | Categoria |', '|---|---|---|'] # Cabeçalho da tabela da seção 4 e a linha que o separa
        linhas += [f'| {tabela} | {coluna} | {categoria} |' for tabela, coluna, categoria in avisos] # Acrescenta uma linha para cada aviso

    if resultado: # Confere se foi gerada uma cópia do banco
        descricao_do_modo = ('Censura (máscara total)' if resultado.modo == ModoDeAnonimizacao.MASCARAR # Descreve o modo: censura
                             else 'Dados sintéticos') # Ou dados sintéticos
        linhas += ['', '#### 5. Cópia anonimizada gerada', '', # Acrescenta o título da seção 5
                   f'* **Banco criado:** `{resultado.destino}`', # Endereço do banco de cópia, com a senha escondida
                   f'* **Modo:** {descricao_do_modo}', '', # Modo usado na cópia
                   '| Tabela | Linhas copiadas | Valores/trechos alterados |', '|---|---:|---|'] # Cabeçalho da tabela da seção 5 e a linha que o separa
        for tabela, linhas_copiadas in resultado.linhas_copiadas.items(): # Passa por cada tabela copiada
            alteracoes_da_tabela = resultado.alteracoes.get(tabela) or {} # Pega as alterações da tabela; se não houver, usa um dicionário vazio
            descricao_das_alteracoes = ', '.join(f'{coluna}: {quantidade}' # Monta o texto com cada coluna e quantos valores foram trocados nela
                                                 for coluna, quantidade in alteracoes_da_tabela.items() if quantidade) # Só das colunas em que algo foi trocado
            linhas.append(f'| {tabela} | {linhas_copiadas} | {descricao_das_alteracoes or "-"} |') # Acrescenta a linha da tabela; sem alterações, escreve "-"

        colunas_forcadas_a_sintetico = [] # Lista que vai guardar as colunas de chave que receberam dado sintético
        for analise_da_tabela in analise_do_banco.tabelas: # Passa pela análise de cada tabela
            for coluna, motivo in analise_da_tabela.forcar_sintetico.items(): # Passa por cada coluna de chave com dado pessoal
                colunas_forcadas_a_sintetico.append((analise_da_tabela.nome, coluna, motivo)) # Guarda a tabela, a coluna e o motivo
        if colunas_forcadas_a_sintetico and resultado.modo == ModoDeAnonimizacao.MASCARAR: # Esse aviso só faz sentido no modo censura
            linhas += ['', 'Colunas que viraram **sintéticas** mesmo no modo censura, para não violar ' # Acrescenta a explicação
                       'a constraint (valores "****" repetidos quebrariam a chave):', ''] # Continuação da explicação
            linhas += [f'* {tabela}.{coluna} ({motivo})' for tabela, coluna, motivo in colunas_forcadas_a_sintetico] # Acrescenta uma linha para cada coluna

        colunas_sensiveis = [] # Lista que vai guardar as colunas com dado sensível
        for analise_da_tabela in analise_do_banco.tabelas: # Passa pela análise de cada tabela
            for coluna, achado in analise_da_tabela.colunas.items(): # Passa por cada coluna com dado pessoal detectado
                if achado.sensivel: # Confere se o dado da coluna é sensível
                    colunas_sensiveis.append(f'{analise_da_tabela.nome}.{coluna}') # Guarda o nome da coluna junto com o da tabela
        if colunas_sensiveis: # Confere se há alguma coluna com dado sensível
            if resultado.modo == ModoDeAnonimizacao.MASCARAR: # Se o modo foi censura
                como_foram_tratados = 'receberam a mesma máscara em todas as linhas, inclusive nas vazias' # Explica como os dados sensíveis foram censurados
            else: # Se o modo foi dado sintético
                como_foram_tratados = ('foram sorteados de novo em todas as linhas, sem ligação com o valor real ' # Explica como os dados sensíveis foram sorteados
                                       '(podem não combinar com outras colunas, como o cargo)') # Continuação da explicação
            linhas += ['', f'* Dados sensíveis ({", ".join(colunas_sensiveis)}) {como_foram_tratados}.'] # Acrescenta a linha sobre os dados sensíveis

        if resultado.modo == ModoDeAnonimizacao.SINTETICO: # Se o modo foi dado sintético
            linhas += ['', '* O dicionário real → sintético foi descartado: a cópia não pode ser ' # Acrescenta o aviso de que a cópia não pode ser revertida
                       'revertida para os dados reais (anonimização, Art. 12).', # Continuação do aviso
                       '* Risco residual: um CPF sintético válido pode coincidir com o de uma pessoa real.'] # Aviso do risco que sobra

    linhas += ['', '#### Limitações', '', # Acrescenta o título da seção de limitações
               f'* As colunas são classificadas por uma amostra de até 1000 linhas por tabela; ' # Primeira limitação: o tamanho da amostra
               'na cópia, os textos livres são varridos por inteiro.', # Continuação da primeira limitação
               '* Só o schema padrão é copiado: sequences, tabelas, PK, FK, UNIQUE, CHECK e índices.'] # Segunda limitação: o que a cópia leva
    if analise_do_banco.objetos_nao_copiados: # Confere se o banco tem objetos que a cópia não leva
        nomes_por_tipo = {} # Dicionário que vai juntar os nomes dos objetos por tipo
        for tipo, nome_do_objeto in analise_do_banco.objetos_nao_copiados: # Passa por cada objeto não copiado
            nomes_por_tipo.setdefault(tipo, []).append(nome_do_objeto) # Guarda o nome do objeto na lista do seu tipo (cria a lista se ainda não existir)
        for tipo, nomes_dos_objetos in nomes_por_tipo.items(): # Passa por cada tipo de objeto
            linhas.append(f'* Não copiado ({tipo}): {", ".join(sorted(nomes_dos_objetos))}') # Acrescenta a linha com os nomes do tipo, em ordem alfabética
    linhas.append('* O GuardIA é uma ferramenta de apoio e não substitui a análise jurídica.') # Acrescenta o aviso final
    return '\n'.join(linhas) + '\n' # Junta todas as linhas, uma embaixo da outra, e devolve o relatório
