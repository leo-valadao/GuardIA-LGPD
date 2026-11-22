from enum import StrEnum # Importa o StrEnum, um tipo de enum em que cada opção também é um texto


class ForcaDoPadrao(StrEnum):
    """Força do padrão de um tipo de dado na regra D = F ∨ (W ∧ C) do artigo."""
    FORTE = 'forte'      # F: só o valor já basta para indicar o dado pessoal
    FRACO = 'fraco'      # W: o valor tem o formato, mas também precisa do contexto (C)
