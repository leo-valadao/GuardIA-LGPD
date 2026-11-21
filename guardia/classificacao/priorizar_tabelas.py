import statistics # Importa o módulo statistics, que calcula média e desvio padrão


def priorizar_tabelas(scores_por_tabela): # Define a função, que recebe o score de risco de cada tabela
    """
    Marca como prioritárias as tabelas com score maior que a média mais o desvio padrão (R > μ + σ).
    Recebe o score de cada tabela e devolve, para cada uma, True (prioritária) ou False.
    """
    valores = list(scores_por_tabela.values()) # Pega só os scores, numa lista
    if len(valores) < 2: # Com menos de 2 tabelas não dá para comparar uma com as outras
        return {nome_da_tabela: False for nome_da_tabela in scores_por_tabela} # Nenhuma tabela é prioritária
    limite = statistics.mean(valores) + statistics.pstdev(valores) # Calcula o limite: a média dos scores mais o desvio padrão deles
    return {nome_da_tabela: score_da_tabela > limite for nome_da_tabela, score_da_tabela in scores_por_tabela.items()} # Marca como prioritária cada tabela com score acima do limite
