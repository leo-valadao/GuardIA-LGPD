"""
Classificação dos dados pessoais encontrados e do risco de cada tabela.

- Classificação LGPD de cada tipo de dado: direto, indireto ou sensível, com risco e mitigação.
- Situação de conformidade: conforme, atenção ou não conforme, equações (2), (3) e (4).
- Score de risco R de cada tabela, equação (8), e a faixa dele: baixo, médio ou alto.
- Priorização: tabelas com R > μ + σ são prioritárias.

Arquivos (um por função pública):
  calcular_faixa_de_risco.py   calcular_faixa_de_risco: Faixa do score de risco: 'baixo' (R < 10), 'médio' (10 a 30) ou 'alto' (R >= 30).
  calcular_score_de_risco.py   calcular_score_de_risco: Equação (8): R = 100 · (Σ r_i) / (w_máx · N), com r_i = w_i · c_i.
  classificar_conformidade.py  classificar_conformidade: Equações (2), (3) e (4) do artigo.
  classificar_tipo_de_dado.py  classificar_tipo_de_dado: Classificação LGPD (RegraDeClassificacao) de um tipo de dado pessoal detectado.
  priorizar_tabelas.py         priorizar_tabelas: Marca como prioritárias as tabelas com score maior que a média mais o desvio padrão (R > μ + σ).
"""
