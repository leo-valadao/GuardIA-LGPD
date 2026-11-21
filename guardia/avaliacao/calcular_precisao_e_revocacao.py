def calcular_precisao_e_revocacao(colunas_identificadas, colunas_reais_esperadas): # Define a função, que recebe as colunas que o GuardIA achou e as que de fato têm dado pessoal
    """
    Calcula Precisão (Precision) e Revocação (Recall) da detecção.
    """
    conjunto_das_colunas_identificadas = set(colunas_identificadas) # Transforma a lista num conjunto (grupo sem repetição), que permite comparar
    conjunto_das_colunas_reais = set(colunas_reais_esperadas) # Transforma a lista num conjunto (grupo sem repetição), que permite comparar

    verdadeiros_positivos = len(conjunto_das_colunas_identificadas.intersection(conjunto_das_colunas_reais)) # Conta as colunas que o GuardIA achou e que de fato têm dado pessoal
    falsos_positivos = len(conjunto_das_colunas_identificadas - conjunto_das_colunas_reais) # Conta as colunas que o GuardIA achou, mas que não têm dado pessoal
    falsos_negativos = len(conjunto_das_colunas_reais - conjunto_das_colunas_identificadas) # Conta as colunas com dado pessoal que o GuardIA não achou

    precisao = verdadeiros_positivos / (verdadeiros_positivos + falsos_positivos) if (verdadeiros_positivos + falsos_positivos) > 0 else 0.0 # Precisão: dos que o GuardIA achou, quantos estavam certos (evita dividir por zero)
    revocacao = verdadeiros_positivos / (verdadeiros_positivos + falsos_negativos) if (verdadeiros_positivos + falsos_negativos) > 0 else 0.0 # Revocação: dos que existiam, quantos o GuardIA achou (evita dividir por zero)

    return { # Devolve um dicionário com os resultados
        'precisao': round(precisao * 100, 2), # Precisão em porcentagem, com 2 casas decimais
        'revocacao': round(revocacao * 100, 2), # Revocação em porcentagem, com 2 casas decimais
        'falsos_positivos': falsos_positivos, # Quantidade de falsos positivos
        'falsos_negativos': falsos_negativos # Quantidade de falsos negativos
    }
