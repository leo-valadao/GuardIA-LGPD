"""
Conexão com o banco de dados (PostgreSQL).

- A senha nunca é passada por argumento de linha de comando: vem da variável de
  ambiente PGPASSWORD ou é digitada sem aparecer na tela (getpass), quando o
  console permite (veja pedir_senha).
- O banco de ORIGEM é aberto em modo somente leitura (default_transaction_read_only):
  o GuardIA não consegue alterar o banco original, nem por engano.
- A cópia é criada como um banco NOVO no mesmo servidor.

Arquivos (um por função pública):
  apagar_banco.py               apagar_banco: Remove um banco criado pelo GuardIA (usado quando a cópia falha no meio).
  completar_senha_da_url.py     completar_senha_da_url: Pede a senha (ou usa PGPASSWORD) quando a URL não tem senha.
  constantes.py                 DRIVER, HOST_PADRAO, PORTA_PADRAO, VARIAVEL_DE_AMBIENTE_DA_SENHA, NIVEL_DE_ISOLAMENTO_SEM_TRANSACAO: constantes usadas em mais de um arquivo
  converter_texto_em_url.py     converter_texto_em_url: Aceita 'postgresql://usuario@host:5432/banco' (com ou sem senha).
  criar_banco_de_copia.py       criar_banco_de_copia: Cria o banco de destino no mesmo servidor e devolve a URL dele.
  criar_engine_de_origem.py     criar_engine_de_origem: Engine do banco original, somente leitura.
  ler_dados_de_conexao.py       ler_dados_de_conexao: Pergunta os dados de acesso ao banco no terminal.
  montar_url.py                 montar_url: Monta a URL de conexão do PostgreSQL; valida banco, usuário e porta.
  ocultar_senha_da_url.py       ocultar_senha_da_url: URL para exibir em tela e relatório, com a senha oculta.
  pedir_senha.py                pedir_senha: Lê a senha sem mostrá-la na tela (getpass).
  sugerir_nome_do_destino.py    sugerir_nome_do_destino: Nome padrão do banco de cópia: <banco de origem>_anonimizado.
  verificar_se_banco_existe.py  verificar_se_banco_existe: True se já existe um banco com esse nome no servidor da URL de origem.
"""
