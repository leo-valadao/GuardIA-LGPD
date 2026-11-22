from sqlalchemy import create_engine, text # Importa a função que conecta no banco e a que prepara um comando SQL

from guardia.banco.conexao.constantes import NIVEL_DE_ISOLAMENTO_SEM_TRANSACAO # Importa o nível de isolamento sem transação


def verificar_se_banco_existe(url_de_origem, nome_do_banco):
    """True se já existe um banco com esse nome no servidor da URL de origem."""
    engine_administrativa = create_engine(url_de_origem, isolation_level=NIVEL_DE_ISOLAMENTO_SEM_TRANSACAO) # Prepara a conexão com o servidor, sem transação
    try: # Tenta rodar o bloco abaixo; o finally roda no fim, dando certo ou não
        with engine_administrativa.connect() as conexao: # Abre a conexão com o servidor; ela é fechada sozinha no fim do bloco
            return conexao.execute(text('SELECT 1 FROM pg_database WHERE datname = :nome'), # Pergunta ao servidor se existe um banco com esse nome
                                   {'nome': nome_do_banco}).scalar() is not None # Devolve verdadeiro se o servidor respondeu alguma coisa
    finally: # Roda sempre, mesmo se der erro
        engine_administrativa.dispose() # Fecha todas as conexões com o servidor
