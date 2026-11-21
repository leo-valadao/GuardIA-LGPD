from guardia.enumeracoes.classificacao_do_dado_pessoal import ClassificacaoDoDadoPessoal # Importa o enum com as classificações de dado pessoal
from guardia.enumeracoes.nivel_de_risco import NivelDeRisco # Importa o enum com os níveis de risco
from guardia.enumeracoes.tipo_de_dado_pessoal import TipoDeDadoPessoal # Importa o enum com os tipos de dado pessoal
from guardia.modelos.regra_de_classificacao import RegraDeClassificacao # Importa a classe que guarda a classificação de um tipo de dado


_MITIGACAO_DE_DADO_SENSIVEL = 'Remover ou anonimizar em todas as linhas' # Mitigação sugerida para os dois tipos de dado sensível

# Classificação LGPD de cada tipo de dado pessoal: classificação, risco e mitigação
REGRAS_DE_CLASSIFICACAO = { # Cria o dicionário: cada tipo de dado pessoal e a sua classificação
    TipoDeDadoPessoal.CPF:                RegraDeClassificacao(ClassificacaoDoDadoPessoal.DIRETO,   NivelDeRisco.CRITICO,        'Mascarar 6 dígitos'), # Classificação do CPF
    TipoDeDadoPessoal.RG:                 RegraDeClassificacao(ClassificacaoDoDadoPessoal.DIRETO,   NivelDeRisco.ALTO,           'Mascarar prefixo/sufixo'), # Classificação do RG
    TipoDeDadoPessoal.NOME:               RegraDeClassificacao(ClassificacaoDoDadoPessoal.DIRETO,   NivelDeRisco.ALTO,           'Ocultar sobrenome'), # Classificação do nome de pessoa
    TipoDeDadoPessoal.EMAIL:              RegraDeClassificacao(ClassificacaoDoDadoPessoal.DIRETO,   NivelDeRisco.ALTO,           'Ocultar prefixo do usuário'), # Classificação do e-mail
    TipoDeDadoPessoal.TELEFONE:           RegraDeClassificacao(ClassificacaoDoDadoPessoal.DIRETO,   NivelDeRisco.ALTO,           'Ocultar os 4 últimos dígitos'), # Classificação do telefone
    TipoDeDadoPessoal.DATA_DE_NASCIMENTO: RegraDeClassificacao(ClassificacaoDoDadoPessoal.INDIRETO, NivelDeRisco.MEDIO,          'Reter apenas o ano'), # Classificação da data de nascimento
    TipoDeDadoPessoal.CEP:                RegraDeClassificacao(ClassificacaoDoDadoPessoal.INDIRETO, NivelDeRisco.BAIXO_OU_MEDIO, 'Ocultar os 3 últimos dígitos'), # Classificação do CEP

    # Dados pessoais sensíveis (Art. 5.º, II)
    TipoDeDadoPessoal.TIPO_SANGUINEO:     RegraDeClassificacao(ClassificacaoDoDadoPessoal.SENSIVEL_DE_SAUDE, # Classificação do tipo sanguíneo: dado sensível de saúde
                                                               NivelDeRisco.CRITICO, _MITIGACAO_DE_DADO_SENSIVEL), # Risco crítico e a mitigação de dado sensível
    TipoDeDadoPessoal.FILIACAO_SINDICAL:  RegraDeClassificacao(ClassificacaoDoDadoPessoal.SENSIVEL_DE_FILIACAO_SINDICAL, # Classificação da filiação sindical: dado sensível
                                                               NivelDeRisco.CRITICO, _MITIGACAO_DE_DADO_SENSIVEL), # Risco crítico e a mitigação de dado sensível
}

# Regra devolvida para um tipo que não está na tabela acima
_REGRA_DE_TIPO_DESCONHECIDO = RegraDeClassificacao(ClassificacaoDoDadoPessoal.REQUER_ANALISE_MANUAL, # O tipo desconhecido precisa de análise manual
                                                   NivelDeRisco.DESCONHECIDO, 'N/A') # O risco é desconhecido e não há mitigação sugerida


def classificar_tipo_de_dado(tipo): # Define a função, que recebe o tipo de dado pessoal
    """Classificação LGPD (RegraDeClassificacao) de um tipo de dado pessoal detectado."""
    return REGRAS_DE_CLASSIFICACAO.get(tipo, _REGRA_DE_TIPO_DESCONHECIDO) # Devolve a regra do tipo; se ele não estiver na tabela, devolve a regra de tipo desconhecido
