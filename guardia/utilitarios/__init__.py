"""
Funções de apoio usadas por mais de uma função do GuardIA.
(Em Python, uma função comum de módulo já é o equivalente a um método static.)

Arquivos (um por função pública):
  converter_para_texto.py                converter_para_texto: O valor como texto sem espaços nas pontas; vazio ("") se for None ou NaN.
  dividir_nome_da_coluna_em_palavras.py  dividir_nome_da_coluna_em_palavras: Separa o nome de uma coluna em palavras: 'dataNascimento' / 'data_nascimento' → data, nascimento.
  montar_url_com_senha_do_ambiente.py    montar_url_com_senha_do_ambiente: URL de conexão com a senha lida da variável PGPASSWORD (usada pelas ferramentas da IA).
  normalizar_texto.py                    normalizar_texto: Minúsculas e sem acentos: 'Data de Nascimento' → 'data de nascimento'.
  validar_nome_do_banco.py               validar_nome_do_banco: Lança NomeDeBancoInvalido se o nome não seguir o padrão: minúsculas, números e "_".
  verificar_se_esta_vazio.py             verificar_se_esta_vazio: None ou NaN.
"""
