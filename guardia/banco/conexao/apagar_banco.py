from sqlalchemy import create_engine, text # Importa a função que conecta no banco e a que prepara um comando SQL

from guardia.banco.conexao.constantes import NIVEL_DE_ISOLAMENTO_SEM_TRANSACAO # Importa o nível de isolamento sem transação
from guardia.utilitarios.validar_nome_do_banco import validar_nome_do_banco # Importa a função que confere se o nome do banco é válido


def apagar_banco(url_de_origem, nome_do_banco):
    """Remove um banco criado pelo GuardIA (usado quando a cópia falha no meio)."""
    validar_nome_do_banco(nome_do_banco) # Confere se o nome do banco é válido antes de usá-lo no comando
    engine_administrativa = create_engine(url_de_origem, isolation_level=NIVEL_DE_ISOLAMENTO_SEM_TRANSACAO) # Prepara a conexão com o servidor, sem transação
    try: # Tenta rodar o bloco abaixo; o finally roda no fim, dando certo ou não
        with engine_administrativa.connect() as conexao: # Abre a conexão com o servidor; ela é fechada sozinha no fim do bloco
            colocar_entre_aspas = conexao.dialect.identifier_preparer.quote # Pega a função que coloca o nome entre aspas, quando o PostgreSQL precisa
            conexao.execute(text(f'DROP DATABASE IF EXISTS {colocar_entre_aspas(nome_do_banco)} WITH (FORCE)')) # Apaga o banco, se ele existir, mesmo com conexões abertas nele
    finally: # Roda sempre, mesmo se der erro
        engine_administrativa.dispose() # Fecha todas as conexões com o servidor
