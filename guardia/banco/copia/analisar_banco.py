from collections import Counter # Importa o Counter, um dicionário que conta quantas vezes cada coisa aparece

from sqlalchemy import MetaData, String, UniqueConstraint, func, select, text # Importa as peças do SQLAlchemy usadas para ler a estrutura e os dados do banco

from guardia.classificacao.calcular_score_de_risco import calcular_score_de_risco # Importa a função que calcula o score de risco de uma tabela
from guardia.classificacao.calcular_faixa_de_risco import calcular_faixa_de_risco # Importa a função que diz a faixa do score (baixo, médio ou alto)
from guardia.classificacao.priorizar_tabelas import priorizar_tabelas # Importa a função que marca as tabelas prioritárias
from guardia.deteccao.identificar_dado_sensivel import identificar_dado_sensivel # Importa a função que avisa sobre possível dado sensível pelo nome da coluna
from guardia.deteccao.classificar_coluna import classificar_coluna # Importa a função que detecta o tipo de dado pessoal de uma coluna
from guardia.deteccao.escanear_texto import escanear_texto # Importa a função que acha dados pessoais dentro de um texto
from guardia.enumeracoes.tipo_de_dado_pessoal import TipoDeDadoPessoal # Importa o enum com os tipos de dado pessoal
from guardia.modelos.analise_da_tabela import AnaliseDaTabela # Importa a classe que guarda a análise de uma tabela
from guardia.modelos.analise_do_banco import AnaliseDoBanco # Importa a classe que guarda a análise do banco inteiro


TAMANHO_DA_AMOSTRA = 1000 # Quantidade máxima de linhas de cada tabela usadas na detecção

# Comando SQL que lista as sequences do banco, com a configuração, o valor atual e a coluna dona de cada uma.
# Os códigos 'a' e 'i' do deptype estão explicados no enum DependenciaDaSequencia
_SQL_DAS_SEQUENCIAS = text("""
                       SELECT s.sequencename    AS nome,
                              s.data_type::TEXT AS tipo,
                              s.start_value,
                              s.min_value,
                              s.max_value,
                              s.increment_by,
                              s.cycle,
                              s.cache_size,
                              s.last_value,
                              d.deptype,
                              tab.relname       AS tabela,
                              att.attname       AS coluna
                       FROM pg_sequences s
                                JOIN pg_namespace n ON n.nspname = s.schemaname
                                JOIN pg_class seq ON seq.relname = s.sequencename AND seq.relnamespace = n.oid
                                LEFT JOIN pg_depend d ON d.objid = seq.oid
                           AND d.classid = 'pg_class'::REGCLASS
                           AND d.deptype IN ('a', 'i')
                                LEFT JOIN pg_class tab ON tab.oid = d.refobjid
                                LEFT JOIN pg_attribute att ON att.attrelid = d.refobjid AND att.attnum = d.refobjsubid
                       WHERE s.schemaname = CURRENT_SCHEMA()
                       ORDER BY s.sequencename
                       """)
# Comando SQL que lista as views, functions, triggers e tipos compostos do banco, que a cópia não leva
_SQL_DOS_OBJETOS_NAO_COPIADOS = text("""
                         SELECT 'view' AS tipo, c.relname AS nome
                         FROM pg_class c
                                  JOIN pg_namespace n ON n.oid = c.relnamespace
                         WHERE n.nspname = CURRENT_SCHEMA()
                           AND c.relkind IN ('v', 'm')

                         UNION ALL

                         SELECT 'function', p.proname
                         FROM pg_proc p
                                  JOIN pg_namespace n ON n.oid = p.pronamespace
                         WHERE n.nspname = CURRENT_SCHEMA()

                         UNION ALL

                         SELECT 'trigger', t.tgname
                         FROM pg_trigger t
                                  JOIN pg_class c ON c.oid = t.tgrelid
                                  JOIN pg_namespace n ON n.oid = c.relnamespace
                         WHERE n.nspname = CURRENT_SCHEMA()
                           AND NOT t.tgisinternal

                         UNION ALL

                         SELECT 'tipo composto', t.typname
                         FROM pg_type t
                                  JOIN pg_class c ON c.oid = t.typrelid
                                  JOIN pg_namespace n ON n.oid = t.typnamespace
                         WHERE n.nspname = CURRENT_SCHEMA()
                           AND c.relkind = 'c'
                         """)


def analisar_banco(engine_de_origem, url_para_exibicao=''):
    """Detecta dados pessoais em todas as tabelas do schema padrão (somente leitura)."""
    metadata = MetaData() # Cria o objeto que vai guardar a estrutura do banco
    metadata.reflect(bind=engine_de_origem) # Lê do banco a estrutura de todas as tabelas
    analises_das_tabelas = [] # Lista que vai guardar a análise de cada tabela

    with engine_de_origem.connect() as conexao_de_origem: # Abre a conexão com o banco; ela é fechada sozinha no fim do bloco
        amostras = {} # Dicionário que vai guardar a amostra de cada tabela

        for tabela in metadata.sorted_tables: # Passa por cada tabela do banco
            total_de_linhas = conexao_de_origem.execute(select(func.count()).select_from(tabela)).scalar() # Conta quantas linhas a tabela tem
            amostra = conexao_de_origem.execute(select(tabela).limit(TAMANHO_DA_AMOSTRA)).mappings().all() # Lê até 1000 linhas da tabela
            amostras[tabela.name] = amostra # Guarda a amostra, para usar depois na busca nos textos

            colunas = {} # Dicionário que vai guardar as colunas com dado pessoal e o Achado de cada uma

            for coluna in tabela.columns: # Passa por cada coluna da tabela
                achado = classificar_coluna(coluna.name, [linha[coluna.name] for linha in amostra]) # Detecta se a coluna tem dado pessoal, olhando os valores da amostra
                if achado: # Se foi detectado um dado pessoal
                    colunas[coluna.name] = achado # Guarda a coluna com o seu Achado

            chaves = _identificar_colunas_de_chave(tabela, metadata) # Descobre as colunas de chave da tabela
            colunas_de_texto = [ # Monta a lista das colunas de texto livre
                coluna.name for coluna in tabela.columns # Passa por cada coluna da tabela
                if isinstance(coluna.type, String) and coluna.name not in colunas and coluna.name not in chaves # Fica com as colunas de texto que não têm tipo detectado e não são chave
            ]

            avisos = [(coluna.name, categoria) for coluna in tabela.columns # Monta a lista de avisos com a coluna e a categoria de dado sensível
                      if coluna.name not in colunas and (categoria := identificar_dado_sensivel(coluna.name))] # Só das colunas sem tipo detectado cujo nome sugere dado sensível

            analises_das_tabelas.append(AnaliseDaTabela( # Guarda a análise da tabela
                nome=tabela.name, total_de_linhas=total_de_linhas, total_de_colunas=len(tabela.columns), # Nome da tabela, quantidade de linhas e de colunas
                colunas=colunas, colunas_de_texto_livre=colunas_de_texto, dados_encontrados_nos_textos={}, # Colunas com dado pessoal, colunas de texto livre e o resultado da busca nos textos, ainda vazio
                avisos=avisos, forcar_sintetico={coluna: chaves[coluna] for coluna in colunas if coluna in chaves}, # Avisos e as colunas com dado pessoal que são chave, com o motivo
            ))

        # Pré-passada: todos os nomes de pessoas, para achá-los também dentro dos textos
        nomes_de_pessoas = set() # Conjunto (grupo sem repetição) que vai guardar os nomes de pessoas
        for analise_da_tabela in analises_das_tabelas: # Passa pela análise de cada tabela
            tabela = metadata.tables[analise_da_tabela.nome] # Pega a tabela na estrutura do banco
            for coluna, achado in analise_da_tabela.colunas.items(): # Passa por cada coluna com dado pessoal
                if achado.tipo == TipoDeDadoPessoal.NOME: # Confere se a coluna é de nome de pessoa
                    valores = conexao_de_origem.execute(select(tabela.c[coluna]).distinct()).scalars() # Lê todos os nomes diferentes da coluna
                    nomes_de_pessoas.update(str(valor).strip() for valor in valores if valor) # Guarda os nomes preenchidos, sem espaços nas pontas

        for analise_da_tabela in analises_das_tabelas: # Passa pela análise de cada tabela
            for coluna in analise_da_tabela.colunas_de_texto_livre: # Passa por cada coluna de texto livre
                tipos = Counter( # Conta quantos dados de cada tipo aparecem nos textos da coluna
                    trecho.tipo for linha in amostras[analise_da_tabela.nome] # Passa pelos dados achados em cada linha da amostra
                    for trecho in escanear_texto(linha[coluna], nomes_de_pessoas) # Procura os dados pessoais dentro do texto da linha
                )
                if tipos: # Confere se algum dado pessoal foi achado nos textos
                    analise_da_tabela.dados_encontrados_nos_textos[coluna] = tipos # Guarda a contagem na análise da tabela

        sequencias = conexao_de_origem.execute(_SQL_DAS_SEQUENCIAS).mappings().all() # Lê as sequences do banco
        objetos_nao_copiados = [tuple(linha_do_resultado) # Transforma cada linha do resultado numa tupla (tipo, nome)
                                for linha_do_resultado in conexao_de_origem.execute(_SQL_DOS_OBJETOS_NAO_COPIADOS)] # Lê os objetos que a cópia não leva

    # Score de risco, equação (8), e priorização R > μ + σ
    for analise_da_tabela in analises_das_tabelas: # Passa pela análise de cada tabela
        campos = [[achado.tipo] for achado in analise_da_tabela.colunas.values()] # Monta a lista de tipos de cada coluna com dado pessoal
        campos += [list(tipos) for tipos in analise_da_tabela.dados_encontrados_nos_textos.values()] # Acrescenta os tipos achados em cada coluna de texto livre
        analise_da_tabela.score_de_risco = calcular_score_de_risco(campos, analise_da_tabela.total_de_colunas) # Calcula o score de risco da tabela
        analise_da_tabela.faixa_de_risco = calcular_faixa_de_risco(analise_da_tabela.score_de_risco) # Descobre a faixa do score
    score_por_tabela = {analise_da_tabela.nome: analise_da_tabela.score_de_risco # Monta o dicionário com o score de cada tabela
                        for analise_da_tabela in analises_das_tabelas} # Passa pela análise de cada tabela
    prioridade_por_tabela = priorizar_tabelas(score_por_tabela) # Descobre quais tabelas são prioritárias

    for analise_da_tabela in analises_das_tabelas: # Passa pela análise de cada tabela
        analise_da_tabela.prioritaria = prioridade_por_tabela[analise_da_tabela.nome] # Guarda se a tabela é prioritária

    return AnaliseDoBanco(url=url_para_exibicao, tabelas=analises_das_tabelas, nomes_conhecidos=nomes_de_pessoas, # Devolve a análise do banco: URL, análise das tabelas e nomes de pessoas
                          objetos_nao_copiados=objetos_nao_copiados, metadata=metadata, sequencias=list(sequencias)) # Objetos não copiados, estrutura do banco e sequences


def _identificar_colunas_de_chave(tabela, metadata):
    """Colunas em PK, FK, UNIQUE ou referenciadas por FK de outra tabela."""
    chaves = {} # Dicionário que vai guardar cada coluna de chave e o motivo
    for coluna in tabela.primary_key.columns: # Passa pelas colunas da chave primária
        chaves[coluna.name] = 'PRIMARY KEY' # Guarda a coluna com o motivo "PRIMARY KEY"

    for constraint in tabela.constraints: # Passa pelas constraints da tabela
        if isinstance(constraint, UniqueConstraint): # Confere se a constraint é do tipo UNIQUE
            for coluna in constraint.columns: # Passa pelas colunas dessa constraint
                chaves.setdefault(coluna.name, 'UNIQUE') # Guarda a coluna com o motivo "UNIQUE", se ela ainda não estiver guardada

    for indice in tabela.indexes: # Passa pelos índices da tabela
        if indice.unique: # Confere se o índice não aceita valores repetidos
            for coluna in indice.columns: # Passa pelas colunas desse índice
                chaves.setdefault(coluna.name, 'UNIQUE INDEX') # Guarda a coluna com o motivo "UNIQUE INDEX", se ela ainda não estiver guardada

    for chave_estrangeira in tabela.foreign_keys: # Passa pelas chaves estrangeiras da tabela
        chaves.setdefault(chave_estrangeira.parent.name, 'FOREIGN KEY') # Guarda a coluna com o motivo "FOREIGN KEY", se ela ainda não estiver guardada

    for outra_tabela in metadata.tables.values(): # Passa por todas as tabelas do banco
        for chave_estrangeira in outra_tabela.foreign_keys: # Passa pelas chaves estrangeiras de cada uma
            if chave_estrangeira.column.table is tabela: # Confere se a chave estrangeira aponta para a tabela que está sendo analisada
                chaves.setdefault(chave_estrangeira.column.name, f'referenciada por {outra_tabela.name}') # Guarda a coluna apontada, com o nome da tabela que aponta para ela

    return chaves # Devolve as colunas de chave e os motivos
