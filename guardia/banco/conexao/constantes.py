# Driver do PostgreSQL usado pelo SQLAlchemy. O pg8000 é escrito só em Python, sem nenhuma DLL.
# Assim o Controle Inteligente de Aplicativos do Windows não tem o que bloquear.
DRIVER = 'postgresql+pg8000' # Banco PostgreSQL, acessado pelo driver pg8000
HOST_PADRAO = 'localhost' # Endereço padrão do servidor: o próprio computador
PORTA_PADRAO = 5432 # Porta padrão do PostgreSQL

# Variável de ambiente com a senha do banco (a mesma que o psql usa)
VARIAVEL_DE_AMBIENTE_DA_SENHA = 'PGPASSWORD' # Nome da variável de ambiente

# CREATE DATABASE e DROP DATABASE não podem rodar dentro de uma transação
NIVEL_DE_ISOLAMENTO_SEM_TRANSACAO = 'AUTOCOMMIT' # Cada comando é gravado na hora, sem transação
