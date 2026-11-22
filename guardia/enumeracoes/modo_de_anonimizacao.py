from enum import StrEnum # Importa o StrEnum, um tipo de enum em que cada opção também é um texto


class ModoDeAnonimizacao(StrEnum):
    """Como os dados pessoais são tratados na cópia do banco."""
    MASCARAR = 'mascarar'        # Censura: o valor é trocado por '*'
    SINTETICO = 'sintetico'      # O valor é trocado por um dado falso e coerente
