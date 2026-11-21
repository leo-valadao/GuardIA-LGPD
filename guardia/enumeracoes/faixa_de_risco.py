from enum import StrEnum # Importa o StrEnum, um tipo de enum em que cada opção também é um texto


class FaixaDeRisco(StrEnum): # Define o enum com as faixas do score de risco
    """Faixa do score de risco R de uma tabela."""
    BAIXO = 'baixo'      # R < 10
    MEDIO = 'médio'      # 10 <= R < 30
    ALTO = 'alto'        # R >= 30
