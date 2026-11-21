"""
Modelos de dados do GuardIA: classes que só guardam informação (dataclasses),
um arquivo para cada. Quem cria e preenche esses objetos são as etapas do GuardIA.

  Detecção (pasta deteccao/)
  padrao_de_deteccao.py      PadraoDeDeteccao: como reconhecer um tipo de dado pessoal (linha do Quadro 2)
  achado.py                  Achado: dado pessoal detectado em uma coluna
  trecho.py                  Trecho: dado pessoal encontrado dentro de um texto livre

  Classificação (pasta classificacao/)
  regra_de_classificacao.py  RegraDeClassificacao: classificação LGPD, risco e mitigação de um tipo de dado

  Banco de dados (pasta banco/copia/)
  analise_da_tabela.py       AnaliseDaTabela: o que foi detectado em uma tabela e o score dela
  analise_do_banco.py        AnaliseDoBanco: a análise de todas as tabelas do banco
  resultado_da_copia.py      ResultadoDaCopia: o que foi copiado e alterado na cópia anonimizada
"""
