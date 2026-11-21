"""
Exceções do GuardIA: um arquivo para cada erro que o próprio GuardIA lança.

Todas herdam de ErroDoGuardia, então quem usa o GuardIA pode tratar qualquer
uma delas com um único "except ErroDoGuardia" e mostrar a mensagem ao usuário.

  erro_do_guardia.py               ErroDoGuardia: a exceção-mãe de todas as outras

  Conexão com o banco
  banco_nao_suportado.py           BancoNaoSuportado: a URL não é de um PostgreSQL
  url_invalida.py                  UrlInvalida: a URL de conexão está mal escrita
  dados_de_conexao_invalidos.py    DadosDeConexaoInvalidos: faltou banco/usuário ou a porta não é número
  senha_nao_informada.py           SenhaNaoInformada: a variável PGPASSWORD não foi definida

  Cópia do banco
  nome_de_banco_invalido.py        NomeDeBancoInvalido: nome do banco de cópia fora do padrão
  destino_igual_a_origem.py        DestinoIgualAOrigem: a cópia teria o mesmo nome do banco original
  banco_ja_existe.py               BancoJaExiste: o banco de cópia já existe
  modo_invalido.py                 ModoInvalido: o modo não é 'mascarar' nem 'sintetico'
  copia_incompleta.py              CopiaIncompleta: a cópia ficou com um número de linhas diferente da origem
"""
