from guardia.enumeracoes.tipo_de_dado_pessoal import TipoDeDadoPessoal # Importa o enum com os tipos de dado pessoal


# Nome de cada tipo de dado pessoal como ele aparece no relatório e no terminal
ROTULOS_DOS_TIPOS = { # Cria o dicionário: cada tipo de dado e o nome dele para mostrar ao usuário
    TipoDeDadoPessoal.CPF: 'CPF', # Nome do tipo CPF
    TipoDeDadoPessoal.RG: 'RG', # Nome do tipo RG
    TipoDeDadoPessoal.EMAIL: 'E-mail', # Nome do tipo e-mail
    TipoDeDadoPessoal.DATA_DE_NASCIMENTO: 'Data de nascimento', # Nome do tipo data de nascimento
    TipoDeDadoPessoal.TELEFONE: 'Telefone', # Nome do tipo telefone
    TipoDeDadoPessoal.NOME: 'Nome', # Nome do tipo nome de pessoa
    TipoDeDadoPessoal.CEP: 'CEP', # Nome do tipo CEP
    TipoDeDadoPessoal.TIPO_SANGUINEO: 'Tipo sanguíneo (sensível)', # Nome do tipo sanguíneo, avisando que é dado sensível
    TipoDeDadoPessoal.FILIACAO_SINDICAL: 'Filiação sindical (sensível)', # Nome da filiação sindical, avisando que é dado sensível
}
