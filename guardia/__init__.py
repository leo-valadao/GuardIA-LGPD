"""
GuardIA-LGPD: auditoria e anonimização de dados pessoais (LGPD).

Cada pasta tem um arquivo por função pública, com o mesmo nome da função
(ex.: deteccao/classificar_coluna.py → def classificar_coluna). Nas pastas
excecoes/, modelos/ e enumeracoes/ é um arquivo por classe. As funções
privadas (_nome) ficam no arquivo da função que as usa. O __init__.py de cada
pasta tem o mapa dos seus arquivos.

As etapas seguem a ordem do artigo:
  1. deteccao/       encontra os dados pessoais (regra D = F ∨ (W ∧ C))
  2. classificacao/  classifica o risco e calcula o score de cada tabela
  3. anonimizacao/   censura ou troca os dados por dados sintéticos
  4. avaliacao/      calcula precisão e revocação da detecção
  5. relatorio/      monta o relatório em Markdown

banco/        acesso ao PostgreSQL (conexao/) e cópia anonimizada do banco (copia/)
ferramentas/  funções chamadas pela IA (descritas no tools.json)
terminal/     texto certo em qualquer terminal e mensagens de erro sem traceback
utilitarios/  funções de apoio usadas por mais de uma função
excecoes/     os erros do GuardIA, um arquivo para cada (todos herdam de ErroDoGuardia)
modelos/      as classes que só guardam dados (dataclasses), um arquivo para cada
enumeracoes/  as listas fechadas de opções (enums), um arquivo para cada

Os valores usados em mais de um arquivo ficam num arquivo só deles, dentro da pasta:
constantes.py (anonimizacao/, relatorio/ e banco/conexao/), padroes.py (deteccao/)
e rotulos.py (relatorio/).
"""
