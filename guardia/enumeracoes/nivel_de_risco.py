from enum import StrEnum # Importa o StrEnum, um tipo de enum em que cada opção também é um texto


class NivelDeRisco(StrEnum):
    """Nível de risco de um tipo de dado pessoal, usado na classificação LGPD."""
    CRITICO = 'Crítico'                # O risco mais grave: o dado sozinho expõe a pessoa
    ALTO = 'Alto'                      # Risco alto
    MEDIO = 'Médio'                    # Risco médio
    BAIXO_OU_MEDIO = 'Baixo/Médio'     # Risco entre baixo e médio
    DESCONHECIDO = 'Desconhecido'      # Tipo que o GuardIA não sabe classificar
