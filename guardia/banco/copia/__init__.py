"""
Análise e cópia anonimizada de um banco PostgreSQL.

Fluxo:
  1. analisar_banco(): lê o schema e uma amostra de cada tabela (somente leitura) e
     detecta as colunas e os textos livres com dados pessoais.
  2. gerar_copia(): cria um banco novo no mesmo servidor com a MESMA estrutura
     (sequences, tabelas, PK, FK, UNIQUE, CHECK e índices com os mesmos nomes) e
     copia os dados em lotes, censurados ou sintéticos. O dado real é transformado
     em memória antes de ser gravado: ele nunca é escrito no banco de destino.
     No fim, as sequences continuam do ponto em que estavam na origem, e cada tabela
     é conferida: a cópia precisa ter o mesmo número de linhas da origem.

Se a cópia falhar no meio, ou a conferência der diferença, o banco de destino criado é apagado.

Arquivos (um por função pública):
  analisar_banco.py  analisar_banco: Detecta dados pessoais em todas as tabelas do schema padrão (somente leitura).
  gerar_copia.py     gerar_copia: Cria o banco 'nome_do_destino' com a estrutura da origem e os dados anonimizados.
"""
