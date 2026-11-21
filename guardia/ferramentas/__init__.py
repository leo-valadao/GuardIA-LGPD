"""
Funções de alto nível para agentes de IA (são as ferramentas descritas em tools.json).

A senha do banco NUNCA passa pela IA: estas funções leem a senha da variável de
ambiente PGPASSWORD, que o próprio usuário configura antes de iniciar o agente.
Por segurança, nenhuma delas sobrescreve um banco que já exista.

Arquivos (um por função pública):
  analisar_banco_dados.py     analisar_banco_dados: Analisa o banco (somente leitura) e retorna o relatório de riscos em Markdown.
  gerar_copia_anonimizada.py  gerar_copia_anonimizada: Cria um banco novo no mesmo servidor com os dados censurados ('mascarar') ou sintéticos.
"""
