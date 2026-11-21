"""
Enumerações do GuardIA: listas fechadas de opções, um arquivo para cada.

Todas são StrEnum: cada opção também é um texto. Assim TipoDeDadoPessoal.CPF == 'cpf'
é verdadeiro, e a opção pode ser escrita no relatório, comparada com o texto que vem
do banco ou da IA e usada como chave de dicionário. A vantagem sobre escrever o texto
direto no código: um nome digitado errado dá erro na hora, em vez de passar calado.

Arquivos (um por enum):
  classificacao_do_dado_pessoal.py  ClassificacaoDoDadoPessoal: Classificação LGPD de um tipo de dado pessoal (Art. 5º, I e II).
  dependencia_da_sequencia.py       DependenciaDaSequencia: Como uma sequence está ligada a uma coluna (coluna deptype da tabela pg_depend do PostgreSQL).
  faixa_de_risco.py                 FaixaDeRisco: Faixa do score de risco R de uma tabela.
  forca_do_padrao.py                ForcaDoPadrao: Força do padrão de um tipo de dado na regra D = F ∨ (W ∧ C) do artigo.
  modo_de_anonimizacao.py           ModoDeAnonimizacao: Como os dados pessoais são tratados na cópia do banco.
  nivel_de_risco.py                 NivelDeRisco: Nível de risco de um tipo de dado pessoal, usado na classificação LGPD.
  opcao_do_menu.py                  OpcaoDoMenu: Opções do menu do modo interativo (main.py): o número que o usuário digita.
  situacao_de_conformidade.py       SituacaoDeConformidade: Situação de um dado pessoal perante a LGPD, equações (2), (3) e (4) do artigo.
  tipo_de_dado_pessoal.py           TipoDeDadoPessoal: Os tipos de dado pessoal que o GuardIA sabe detectar (Quadro 2 do artigo).
"""
