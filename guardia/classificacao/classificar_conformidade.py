from guardia.enumeracoes.situacao_de_conformidade import SituacaoDeConformidade # Importa o enum com as situações de conformidade


def classificar_conformidade(detectado, protegido, exposto):
    """Equações (2), (3) e (4) do artigo."""
    if not detectado or protegido: # Confere se o dado não foi detectado ou se está protegido
        return SituacaoDeConformidade.CONFORME # Nesses casos, está conforme
    return SituacaoDeConformidade.NAO_CONFORME if exposto else SituacaoDeConformidade.ATENCAO # Se está exposto, não está conforme; senão, merece atenção
