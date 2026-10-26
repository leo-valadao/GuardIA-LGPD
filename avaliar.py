def calcular_precisao_revocacao(colunas_identificadas, colunas_reais_esperadas):
    """
    Calcula Precisão (Precision) e Revocação (Recall) da detecção.
    """
    identificadas_set = set(colunas_identificadas)
    reais_set = set(colunas_reais_esperadas)
    
    verdadeiros_positivos = len(identificadas_set.intersection(reais_set))
    falsos_positivos = len(identificadas_set - reais_set)
    falsos_negativos = len(reais_set - identificadas_set)
    
    precisao = verdadeiros_positivos / (verdadeiros_positivos + falsos_positivos) if (verdadeiros_positivos + falsos_positivos) > 0 else 0.0
    revocacao = verdadeiros_positivos / (verdadeiros_positivos + falsos_negativos) if (verdadeiros_positivos + falsos_negativos) > 0 else 0.0
        
    return {
        'precisao': round(precisao * 100, 2),
        'revocacao': round(revocacao * 100, 2),
        'falsos_positivos': falsos_positivos,
        'falsos_negativos': falsos_negativos
    }
