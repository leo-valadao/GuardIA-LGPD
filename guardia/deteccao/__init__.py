"""
Detecção de dados pessoais (LGPD) pelo nome da coluna e pelo conteúdo.

Regra do artigo, equação (1):   D = F ∨ (W ∧ C)

  F  padrão FORTE: basta o valor para indicar dado pessoal
     (e-mail; CPF com dígitos verificadores válidos pelo módulo 11)
  W  padrão FRACO: o valor tem o formato, mas sozinho não basta
     (formato de CPF com dígitos inválidos, RG, data, telefone, CEP,
     tipo sanguíneo e filiação sindical)
  C  CONTEXTO: uma palavra do nome da coluna começa com um termo do tipo
     ("cpf", "nasc", "tel"...) ou, em texto livre, uma dessas palavras
     aparece logo antes do valor

Os tipos, as expressões regulares, as forças, os pesos e os termos de contexto
estão na tabela PADROES_DE_DETECCAO (padroes.py), que é o Quadro 2 do artigo.

Nome de pessoa não tem padrão de valor (Quadro 2 do artigo): exige contexto
e valores com aparência de nome (2 ou mais palavras com inicial maiúscula), o
que evita tratar "Produto 1" ou "Vestuário" como nome de pessoa.

Arquivos (um por função pública):
  calcular_digitos_verificadores_do_cpf.py  calcular_digitos_verificadores_do_cpf: Dígitos verificadores do CPF, equações (5), (6) e (7) do artigo.
  classificar_coluna.py                     classificar_coluna: Aplica D = F ∨ (W ∧ C) a uma amostra de valores. Retorna um Achado ou None.
  escanear_texto.py                         escanear_texto: Dados pessoais dentro de um texto livre (ex.: atendimentos.descricao).
  identificar_dado_sensivel.py              identificar_dado_sensivel: Categoria de dado sensível sugerida pelo nome da coluna, ou None.
  identificar_tipos_pelo_contexto.py        identificar_tipos_pelo_contexto: Tipos de dado que o nome da coluna indica (o contexto C da regra).
  padroes.py                                PADROES_DE_DETECCAO, PESO_MAXIMO, TIPOS_SENSIVEIS: constantes usadas em mais de um arquivo
  validar_cpf.py                            validar_cpf: CPF com 11 dígitos, não repetidos, e dígitos verificadores corretos.
  validar_nome_de_pessoa.py                 validar_nome_de_pessoa: True se o valor tem cara de nome de pessoa: 2 ou mais palavras com inicial maiúscula.
"""
