from enum import StrEnum # Importa o StrEnum, um tipo de enum em que cada opção também é um texto


class SituacaoDeConformidade(StrEnum): # Define o enum com as situações de conformidade com a LGPD
    """Situação de um dado pessoal perante a LGPD, equações (2), (3) e (4) do artigo."""
    CONFORME = 'Conforme'              # O dado não foi detectado ou está protegido
    ATENCAO = 'Atenção'                # O dado foi detectado, não está protegido, mas não está exposto
    NAO_CONFORME = 'Não conforme'      # O dado foi detectado, não está protegido e está exposto
