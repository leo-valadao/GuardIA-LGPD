from enum import StrEnum # Importa o StrEnum, um tipo de enum em que cada opção também é um texto


class ClassificacaoDoDadoPessoal(StrEnum):
    """Classificação LGPD de um tipo de dado pessoal (Art. 5.º, I e II)."""
    DIRETO = 'Dado Pessoal Direto'                    # Identifica a pessoa sozinho
    INDIRETO = 'Dado Pessoal Indireto'                # Identifica a pessoa junto com outros dados
    SENSIVEL_DE_SAUDE = 'Dado Pessoal Sensível (saúde)'                               # Dado sensível sobre a saúde da pessoa
    SENSIVEL_DE_FILIACAO_SINDICAL = 'Dado Pessoal Sensível (filiação a sindicato)'    # Dado sensível sobre a filiação da pessoa a um sindicato
    REQUER_ANALISE_MANUAL = 'Requer Análise Manual'   # Tipo que o GuardIA não sabe classificar
