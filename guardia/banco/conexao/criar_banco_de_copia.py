from sqlalchemy import create_engine, text # Importa a função que conecta no banco e a que prepara um comando SQL

from guardia.banco.conexao.constantes import NIVEL_DE_ISOLAMENTO_SEM_TRANSACAO # Importa o nível de isolamento sem transação
from guardia.excecoes.banco_ja_existe import BancoJaExiste # Importa o erro lançado quando o banco de cópia já existe
from guardia.excecoes.destino_igual_a_origem import DestinoIgualAOrigem # Importa o erro lançado quando a cópia teria o nome do banco original
from guardia.utilitarios.validar_nome_do_banco import validar_nome_do_banco # Importa a função que confere se o nome do banco é válido


def criar_banco_de_copia(url_de_origem, nome_do_destino, sobrescrever=False): # Define a função, que recebe a URL de origem, o nome da cópia e se pode apagar um banco que já existe
    """
    Cria o banco de destino no mesmo servidor e devolve a URL dele.
    Só apaga um banco existente com sobrescrever=True.
    """
    validar_nome_do_banco(nome_do_destino) # Confere se o nome do banco de cópia é válido
    if nome_do_destino == url_de_origem.database: # Confere se o nome da cópia é igual ao do banco original
        raise DestinoIgualAOrigem(nome_do_destino) # Lança o erro, para o banco original nunca ser apagado

    engine_administrativa = create_engine(url_de_origem, isolation_level=NIVEL_DE_ISOLAMENTO_SEM_TRANSACAO) # Prepara a conexão com o servidor, sem transação
    try: # Tenta rodar o bloco abaixo; o finally roda no fim, dando certo ou não
        with engine_administrativa.connect() as conexao: # Abre a conexão com o servidor; ela é fechada sozinha no fim do bloco
            colocar_entre_aspas = conexao.dialect.identifier_preparer.quote # Pega a função que coloca o nome entre aspas, quando o PostgreSQL precisa
            ja_existe = conexao.execute(text('SELECT 1 FROM pg_database WHERE datname = :nome'), # Pergunta ao servidor se já existe um banco com esse nome
                                     {'nome': nome_do_destino}).scalar() # Passa o nome como parâmetro e pega a resposta (1 ou nada)
            if ja_existe: # Se o banco já existe
                if not sobrescrever: # E não foi autorizado apagá-lo
                    raise BancoJaExiste(nome_do_destino) # Lança o erro de banco que já existe
                conexao.execute(text(f'DROP DATABASE {colocar_entre_aspas(nome_do_destino)} WITH (FORCE)')) # Apaga o banco antigo, mesmo com conexões abertas nele
            codificacao = conexao.execute(text( # Pergunta ao servidor a codificação de texto do banco original
                'SELECT pg_encoding_to_char(encoding) FROM pg_database WHERE datname = current_database()' # Comando SQL que lê a codificação do banco atual
            )).scalar() # Pega a resposta
            conexao.execute(text( # Cria o banco de cópia
                f"CREATE DATABASE {colocar_entre_aspas(nome_do_destino)} TEMPLATE template0 ENCODING '{codificacao}'" # Comando SQL que cria o banco vazio, com a mesma codificação da origem
            ))
    finally: # Roda sempre, mesmo se der erro
        engine_administrativa.dispose() # Fecha todas as conexões com o servidor
    return url_de_origem.set(database=nome_do_destino) # Devolve a URL do banco de cópia
