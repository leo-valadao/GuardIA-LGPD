from sqlalchemy import create_engine # Importa a função do SQLAlchemy que prepara a conexão com o banco


def criar_engine_de_origem(url): # Define a função, que recebe a URL do banco original
    """Engine do banco original, somente leitura."""
    return create_engine( # Prepara e devolve a conexão com o banco original
        url, # Endereço do banco
        # Avisa o PostgreSQL, já ao abrir a conexão, que toda transação dela é só de leitura
        connect_args={'startup_params': {'options': '-c default_transaction_read_only=on'}}, # Opção que deixa a conexão só de leitura
        pool_pre_ping=True, # Testa a conexão antes de usá-la, para não usar uma conexão que caiu
    )
