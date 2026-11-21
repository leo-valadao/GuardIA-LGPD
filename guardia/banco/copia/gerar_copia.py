from collections import Counter # Importa o Counter, um dicionário que conta quantas vezes cada coisa aparece

from sqlalchemy import create_engine, func, select, text # Importa as peças do SQLAlchemy usadas para conectar, contar, ler e rodar comandos SQL

from guardia.anonimizacao.anonimizar_registro import anonimizar_registro # Importa a função que anonimiza uma linha da tabela
from guardia.anonimizacao.anonimizar_texto import anonimizar_texto # Importa a função que anonimiza os dados pessoais dentro de um texto
from guardia.anonimizacao.substituidor import Substituidor # Importa a classe que gera os valores sintéticos
from guardia.banco.conexao.apagar_banco import apagar_banco # Importa a função que apaga um banco
from guardia.banco.conexao.criar_banco_de_copia import criar_banco_de_copia # Importa a função que cria o banco de cópia vazio
from guardia.banco.conexao.ocultar_senha_da_url import ocultar_senha_da_url # Importa a função que esconde a senha da URL
from guardia.enumeracoes.dependencia_da_sequencia import DependenciaDaSequencia # Importa o enum com os jeitos de uma sequence estar ligada a uma coluna
from guardia.enumeracoes.modo_de_anonimizacao import ModoDeAnonimizacao # Importa o enum com os modos de anonimização
from guardia.excecoes.copia_incompleta import CopiaIncompleta # Importa o erro lançado quando a cópia fica incompleta
from guardia.excecoes.modo_invalido import ModoInvalido # Importa o erro lançado quando o modo é inválido
from guardia.modelos.resultado_da_copia import ResultadoDaCopia # Importa a classe que guarda o resultado da cópia


TAMANHO_DO_LOTE = 5000 # Quantidade de linhas lidas e gravadas de cada vez


def _criar_estrutura_do_banco(engine_de_destino, analise_do_banco): # Define a função privada que recebe a conexão com a cópia e a análise do banco
    """Sequences → tabelas (com PK, FK, UNIQUE, CHECK, índices) → OWNED BY."""
    with engine_de_destino.begin() as conexao_de_destino: # Abre uma transação na cópia; ela é gravada sozinha no fim do bloco
        colocar_entre_aspas = conexao_de_destino.dialect.identifier_preparer.quote # Pega a função que coloca o nome entre aspas, quando o PostgreSQL precisa
        for sequencia in analise_do_banco.sequencias: # Passa por cada sequence do banco original
            if sequencia['deptype'] == DependenciaDaSequencia.CRIADA_PELA_COLUNA_IDENTITY: # Confere se a sequence é de uma coluna IDENTITY
                continue  # Sequence de coluna IDENTITY: criada junto com a tabela
            conexao_de_destino.execute(text( # Cria a sequence na cópia
                f"CREATE SEQUENCE {colocar_entre_aspas(sequencia['nome'])} AS {sequencia['tipo']}" # Nome e tipo da sequence
                f" START WITH {sequencia['start_value']} INCREMENT BY {sequencia['increment_by']}" # Valor inicial e de quanto em quanto ela anda
                f" MINVALUE {sequencia['min_value']} MAXVALUE {sequencia['max_value']}" # Menor e maior valor que ela aceita
                f" CACHE {sequencia['cache_size']} {'CYCLE' if sequencia['cycle'] else 'NO CYCLE'}" # Quantos valores ela reserva e se volta ao início quando chega no máximo
            ))
    # Sem isto o SQLAlchemy cria a coluna como SERIAL (com uma sequence nova "tabela_coluna_seq")
    # em vez de manter o DEFAULT NEXTVAL('sequence_original') da origem.
    for tabela in analise_do_banco.metadata.tables.values(): # Passa por cada tabela da estrutura do banco
        for coluna in tabela.columns: # Passa por cada coluna da tabela
            if coluna.server_default is not None and 'nextval(' in str(coluna.server_default.arg): # Confere se o valor padrão da coluna vem de uma sequence
                coluna.autoincrement = False # Avisa o SQLAlchemy para não criar uma sequence nova para essa coluna

    analise_do_banco.metadata.create_all(engine_de_destino) # Cria na cópia todas as tabelas, com chaves, constraints e índices

    with engine_de_destino.begin() as conexao_de_destino: # Abre uma transação na cópia; ela é gravada sozinha no fim do bloco
        colocar_entre_aspas = conexao_de_destino.dialect.identifier_preparer.quote # Pega a função que coloca o nome entre aspas, quando o PostgreSQL precisa
        for sequencia in analise_do_banco.sequencias: # Passa por cada sequence do banco original
            if sequencia['deptype'] == DependenciaDaSequencia.PERTENCE_A_UMA_COLUNA: # Confere se a sequence pertence a uma coluna
                nome_da_sequencia = colocar_entre_aspas(sequencia['nome']) # Prepara o nome da sequence para o comando SQL
                nome_da_tabela = colocar_entre_aspas(sequencia['tabela']) # Prepara o nome da tabela para o comando SQL
                nome_da_coluna = colocar_entre_aspas(sequencia['coluna']) # Prepara o nome da coluna para o comando SQL
                conexao_de_destino.execute(text( # Liga a sequence à sua coluna na cópia
                    f'ALTER SEQUENCE {nome_da_sequencia} OWNED BY {nome_da_tabela}.{nome_da_coluna}' # Comando SQL que diz a qual coluna a sequence pertence
                ))


def _ajustar_sequencias(engine_de_destino, analise_do_banco): # Define a função privada que recebe a conexão com a cópia e a análise do banco
    """Continua as sequences do ponto em que estão na origem."""
    with engine_de_destino.begin() as conexao_de_destino: # Abre uma transação na cópia; ela é gravada sozinha no fim do bloco
        colocar_entre_aspas = conexao_de_destino.dialect.identifier_preparer.quote # Pega a função que coloca o nome entre aspas, quando o PostgreSQL precisa
        for sequencia in analise_do_banco.sequencias: # Passa por cada sequence do banco original
            if sequencia['deptype'] == DependenciaDaSequencia.CRIADA_PELA_COLUNA_IDENTITY: # Se a sequence é de uma coluna IDENTITY
                comando_sql = text('SELECT SETVAL(PG_GET_SERIAL_SEQUENCE(:tabela, :coluna), :valor, :chamado)') # Comando que acha a sequence pela coluna e muda o valor dela
                parametros = {'tabela': colocar_entre_aspas(sequencia['tabela']), 'coluna': sequencia['coluna']} # Informa a tabela e a coluna da sequence
            else: # Se a sequence tem nome próprio
                comando_sql = text('SELECT SETVAL(CAST(:sequencia AS REGCLASS), :valor, :chamado)') # Comando que muda o valor da sequence pelo nome
                parametros = {'sequencia': colocar_entre_aspas(sequencia['nome'])} # Informa o nome da sequence
            if sequencia['last_value'] is None: # Se a sequence nunca foi usada na origem
                parametros.update(valor=sequencia['start_value'], chamado=False) # Volta ao valor inicial, sem marcá-lo como já usado
            else: # Se a sequence já foi usada na origem
                parametros.update(valor=sequencia['last_value'], chamado=True) # Continua do último valor usado na origem
            conexao_de_destino.execute(comando_sql, parametros) # Roda o comando na cópia


def _cortar_no_tamanho_da_coluna(valor, coluna): # Define a função privada que recebe um valor e a coluna onde ele vai ser gravado
    """Valor sintético maior que o VARCHAR(n) da coluna é cortado no tamanho."""
    tamanho_maximo = getattr(coluna.type, 'length', None) # Pega o tamanho máximo da coluna; se ela não tiver, fica None
    if tamanho_maximo and isinstance(valor, str) and len(valor) > tamanho_maximo: # Confere se o valor é um texto maior do que a coluna aceita
        return valor[:tamanho_maximo] # Devolve só o começo do texto, no tamanho da coluna
    return valor # Devolve o valor como está


def gerar_copia(engine_de_origem, url_de_origem, analise_do_banco, modo, nome_do_destino, # Define a função, que recebe a conexão e a URL de origem, a análise, o modo e o nome da cópia
                sobrescrever=False, semente=None, ao_progredir=print): # E, se houver, se pode apagar um banco que já existe, a semente e a função que mostra o progresso
    """Cria o banco 'nome_do_destino' com a estrutura da origem e os dados anonimizados."""
    # Aceita o texto ('mascarar' ou 'sintetico', que vem da CLI e da IA) ou o próprio enum
    try: # Tenta converter o modo no enum; se não der, cai no except
        modo = ModoDeAnonimizacao(modo) # Converte o modo no enum ModoDeAnonimizacao
    except ValueError: # Se o modo não é um dos modos válidos
        raise ModoInvalido(modo) from None # Lança o erro de modo inválido, sem mostrar o erro técnico

    url_de_destino = criar_banco_de_copia(url_de_origem, nome_do_destino, sobrescrever) # Cria o banco de cópia vazio e pega a URL dele
    engine_de_destino = create_engine(url_de_destino) # Prepara a conexão com o banco de cópia
    substituidor = Substituidor(semente) # Cria o gerador de valores sintéticos
    resultado = ResultadoDaCopia(destino=ocultar_senha_da_url(url_de_destino), modo=modo) # Começa o resultado da cópia, com a URL sem senha e o modo
    analises_por_nome = {analise_da_tabela.nome: analise_da_tabela # Monta o dicionário com a análise de cada tabela, pelo nome dela
                         for analise_da_tabela in analise_do_banco.tabelas} # Passa pela análise de cada tabela

    try: # Tenta copiar o banco; se der erro, o except apaga a cópia pela metade
        _criar_estrutura_do_banco(engine_de_destino, analise_do_banco) # Cria na cópia as sequences, as tabelas e as constraints
        with engine_de_origem.connect() as conexao_de_origem: # Abre a conexão com o banco original; ela é fechada sozinha no fim do bloco
            for tabela in analise_do_banco.metadata.sorted_tables: # Passa por cada tabela, na ordem certa para as chaves estrangeiras
                analise_da_tabela = analises_por_nome[tabela.name] # Pega a análise da tabela
                tipos = {coluna: achado.tipo for coluna, achado in analise_da_tabela.colunas.items()} # Monta o dicionário com o tipo de dado de cada coluna
                alteracoes = Counter() # Contador de valores trocados em cada coluna
                linhas_copiadas = 0 # Ainda nenhuma linha foi copiada
                colunas_de_ordenacao = list(tabela.primary_key.columns) or list(tabela.columns) # Ordena pela chave primária ou, se não houver, por todas as colunas
                # Lê a tabela inteira em pedaços (lotes), sem carregar tudo na memória de uma vez
                cursor = conexao_de_origem.execution_options(stream_results=True, yield_per=TAMANHO_DO_LOTE) \
                    .execute(select(tabela).order_by(*colunas_de_ordenacao)) # Roda a leitura da tabela, já ordenada
                for lote in cursor.mappings().partitions(): # Passa por cada lote de linhas lidas
                    linhas_do_lote = [] # Lista que vai guardar as linhas anonimizadas do lote
                    for linha in lote: # Passa por cada linha do lote
                        linha = dict(linha) # Transforma a linha num dicionário comum (coluna e valor)
                        linha_anonimizada = anonimizar_registro(linha, tipos, modo, substituidor, # Anonimiza as colunas com dado pessoal da linha
                                                                analise_da_tabela.forcar_sintetico, # Informa as colunas de chave, que recebem dado sintético
                                                                analise_da_tabela.colunas) # Informa os Achados, usados nos dados sensíveis
                        for coluna in analise_da_tabela.colunas_de_texto_livre: # Passa por cada coluna de texto livre
                            texto_anonimizado, quantidade_de_trechos = anonimizar_texto( # Anonimiza os dados pessoais dentro do texto
                                linha[coluna], modo, substituidor, analise_do_banco.nomes_conhecidos) # Texto da coluna, modo, substituidor e nomes de pessoas conhecidos
                            linha_anonimizada[coluna] = texto_anonimizado # Guarda o texto anonimizado na linha
                            alteracoes[coluna] += quantidade_de_trechos # Soma os trechos trocados no contador da coluna
                        for coluna in tipos: # Passa por cada coluna com dado pessoal
                            if linha_anonimizada[coluna] != linha[coluna]: # Confere se o valor mudou
                                alteracoes[coluna] += 1 # Soma 1 no contador da coluna
                        for coluna in list(tipos) + analise_da_tabela.colunas_de_texto_livre: # Passa por todas as colunas que podem ter mudado
                            linha_anonimizada[coluna] = _cortar_no_tamanho_da_coluna(linha_anonimizada[coluna], # Corta o valor novo, se ele passar do tamanho da coluna
                                                                                     tabela.c[coluna]) # Informa a coluna, para saber o tamanho máximo
                        linhas_do_lote.append(linha_anonimizada) # Guarda a linha anonimizada no lote
                    with engine_de_destino.begin() as conexao_de_destino: # Abre uma transação na cópia; ela é gravada sozinha no fim do bloco
                        conexao_de_destino.execute(tabela.insert(), linhas_do_lote) # Grava todas as linhas do lote na cópia
                    linhas_copiadas += len(linhas_do_lote) # Soma as linhas do lote no total copiado
                resultado.linhas_copiadas[tabela.name] = linhas_copiadas # Guarda no resultado quantas linhas da tabela foram copiadas
                resultado.alteracoes[tabela.name] = alteracoes # Guarda no resultado quantos valores foram trocados em cada coluna
                ao_progredir(f'   {tabela.name}: {linhas_copiadas} linhas copiadas') # Mostra o progresso da cópia

        _ajustar_sequencias(engine_de_destino, analise_do_banco) # Faz as sequences da cópia continuarem do ponto da origem

        with engine_de_destino.connect() as conexao_de_destino: # Abre a conexão com a cópia; ela é fechada sozinha no fim do bloco
            for tabela in analise_do_banco.metadata.sorted_tables: # Passa por cada tabela da cópia
                linhas_no_destino = conexao_de_destino.execute(select(func.count()).select_from(tabela)).scalar() # Conta quantas linhas a tabela tem na cópia
                if linhas_no_destino != resultado.linhas_copiadas[tabela.name]: # Confere se a contagem é diferente do que foi copiado
                    raise CopiaIncompleta(tabela.name, resultado.linhas_copiadas[tabela.name], linhas_no_destino) # Lança o erro de cópia incompleta

    except Exception: # Se deu qualquer erro durante a cópia
        engine_de_destino.dispose() # Fecha as conexões com a cópia
        apagar_banco(url_de_origem, nome_do_destino) # Apaga a cópia, para nada ficar pela metade
        raise # Lança o erro de novo, para quem chamou saber que deu errado

    finally: # Roda sempre, mesmo se der erro
        substituidor.descartar_dicionario()  # Sem o dicionário, não há como voltar ao dado real
        engine_de_destino.dispose() # Fecha as conexões com a cópia

    return resultado # Devolve o resultado da cópia
