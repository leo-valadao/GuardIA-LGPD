from enum import StrEnum # Importa o StrEnum, um tipo de enum em que cada opção também é um texto


class TipoDeDadoPessoal(StrEnum):
    """
    Os tipos de dado pessoal que o GuardIA sabe detectar (Quadro 2 do artigo).
    É um StrEnum: cada tipo também é um texto, então pode ser comparado com texto,
    escrito no relatório e usado como chave de dicionário.
    """
    CPF = 'cpf'                                  # Cadastro de Pessoa Física
    RG = 'rg'                                    # Registro Geral (carteira de identidade)
    EMAIL = 'email'                              # Endereço de e-mail
    DATA_DE_NASCIMENTO = 'data_de_nascimento'    # Data em que a pessoa nasceu
    TELEFONE = 'telefone'                        # Número de telefone ou celular
    NOME = 'nome'                                # Nome de pessoa
    CEP = 'cep'                                  # Código de Endereçamento Postal
    TIPO_SANGUINEO = 'tipo_sanguineo'            # Dado pessoal sensível (Art. 5.º, II): saúde
    FILIACAO_SINDICAL = 'filiacao_sindical'      # Dado pessoal sensível (Art. 5.º, II)
