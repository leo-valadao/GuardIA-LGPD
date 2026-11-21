"""
Testes unitários do GuardIA (unittest). Nenhum deles precisa do banco de dados rodando.

Como rodar, na raiz do projeto:
  python -m unittest discover testes

Arquivos:
  test_guardia.py  Todos os testes, separados em classes por assunto:
    TestGuardIALGPD     Detecção de colunas com dados pessoais, classificação LGPD e precisão/revocação
    TestCPF             Dígitos verificadores do CPF, equações (5), (6) e (7) do artigo
    TestRegraDeteccao   Regra de detecção D = F ∨ (W ∧ C) e contexto pelo nome da coluna
    TestTextoLivre      Dados pessoais escritos dentro de textos livres
    TestSubstituidor    Dados sintéticos: dicionário bijetor, formato, DDD, CEP e e-mail feito do nome
    TestDadosSensiveis  Tipo sanguíneo e filiação sindical (Art. 5º, II)
    TestExcecoes        Erros de conexão e de cópia do banco
    TestMascaraEScore   Máscara total, chaves que viram sintéticas e score de risco (equação 8)
    TestEnumeracoes     Enums (StrEnum) e a tabela de padrões de detecção
"""
