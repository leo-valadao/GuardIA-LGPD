from guardia.enumeracoes.faixa_de_risco import FaixaDeRisco # Importa o enum com as faixas de risco (baixo, médio e alto)


# Faixas iniciais do score (a calibrar nos testes): (limite de cima, faixa)
FAIXAS_DE_RISCO = ((10, FaixaDeRisco.BAIXO), (30, FaixaDeRisco.MEDIO), (float('inf'), FaixaDeRisco.ALTO)) # Abaixo de 10 é baixo, abaixo de 30 é médio e o resto é alto (inf = infinito)


def calcular_faixa_de_risco(score_de_risco): # Define a função, que recebe o score de risco de uma tabela
    """Faixa do score de risco: 'baixo' (R < 10), 'médio' (10 a 30) ou 'alto' (R >= 30)."""
    for limite, faixa_de_risco in FAIXAS_DE_RISCO: # Passa por cada faixa, da mais baixa para a mais alta
        if score_de_risco < limite: # Confere se o score fica abaixo do limite de cima da faixa
            return faixa_de_risco # Devolve a faixa encontrada
    return FAIXAS_DE_RISCO[-1][1] # Se nenhuma faixa serviu, devolve a última (a faixa alta)
