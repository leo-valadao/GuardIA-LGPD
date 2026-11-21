"""
Remediação dos dados pessoais: censura (máscara total) ou substituição sintética.

- Censura: texto vira '*' com o mesmo tamanho, número vira 0 e data fica só com o ano
  (1.º de janeiro). Dado sensível recebe a mesma máscara em todas as linhas, inclusive
  nas vazias. Coluna de chave (PK, FK ou UNIQUE) recebe dado sintético, porque a mesma
  máscara repetida em todas as linhas quebraria a chave.
- Sintético: dicionário BIJETOR (Åbrandt, 2026) → o mesmo valor real vira sempre o
  mesmo valor falso, e dois valores reais nunca viram o mesmo falso. Isso preserva as
  relações entre tabelas e a coerência dentro dos textos. O dicionário é descartado no
  fim (descartar_dicionario()): sem ele não há como voltar ao dado real (anonimização, Art. 12),
  e não pseudonimização (Art. 13, § 4.º). Dado sensível não usa o dicionário: é sorteado
  de novo em cada linha.

Atenção: um CPF sintético válido pode coincidir com o de uma pessoa real (risco residual).

Arquivos (um por função pública):
  anonimizar_registro.py  anonimizar_registro: Anonimiza um registro (dict coluna → valor). 'tipos' = {coluna: tipo detectado}.
  anonimizar_texto.py     anonimizar_texto: Troca só os trechos com dado pessoal dentro de um texto livre. Retorna (texto, quantidade_de_trechos).
  constantes.py           CARACTERE_DA_MASCARA: constantes usadas em mais de um arquivo
  mascarar_valor.py       mascarar_valor: Máscara total: texto → '*' no mesmo tamanho; data → 1.º de janeiro do mesmo ano.
  substituidor.py         Substituidor: Gera valores sintéticos coerentes, com dicionário bijetor por tipo.
"""
