from enum import StrEnum # Importa o StrEnum, um tipo de enum em que cada opção também é um texto


class DependenciaDaSequencia(StrEnum):
    """Como uma sequence está ligada a uma coluna (coluna deptype da tabela pg_depend do PostgreSQL)."""
    PERTENCE_A_UMA_COLUNA = 'a'          # Código 'a' (auto): sequence com OWNED BY, apagada junto com a coluna
    CRIADA_PELA_COLUNA_IDENTITY = 'i'    # Código 'i' (internal): sequence criada pelo próprio PostgreSQL para a coluna IDENTITY
