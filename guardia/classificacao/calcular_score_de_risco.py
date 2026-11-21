from guardia.deteccao.padroes import PADROES_DE_DETECCAO, PESO_MAXIMO # Importa a tabela de regras de cada tipo e o maior peso entre os tipos
from guardia.enumeracoes.situacao_de_conformidade import SituacaoDeConformidade # Importa o enum com as situações de conformidade


# Fator c_i do artigo: 1 = Não conforme, 0,5 = Atenção, 0 = Conforme
FATOR_DE_CONFORMIDADE = { # Cria o dicionário: cada situação de conformidade e o seu fator
    SituacaoDeConformidade.NAO_CONFORME: 1.0, # O risco conta inteiro
    SituacaoDeConformidade.ATENCAO: 0.5, # O risco conta pela metade
    SituacaoDeConformidade.CONFORME: 0.0, # O risco não conta
}


def calcular_score_de_risco(tipos_por_campo, total_de_campos, conformidade=SituacaoDeConformidade.NAO_CONFORME): # Define a função, que recebe os tipos de cada campo, o total de campos e a situação de conformidade
    """
    Equação (8): R = 100 · (Σ r_i) / (w_máx · N), com r_i = w_i · c_i.
    tipos_por_campo = lista com os tipos detectados de cada campo com dado pessoal
    (um campo de texto livre pode ter vários; vale o de maior peso).
    No banco de dados, o dado gravado em texto claro já é exposto (E verdadeiro).
    """
    if total_de_campos <= 0: # Confere se a tabela não tem campos (evita dividir por zero)
        return 0.0 # Sem campos, o score é 0
    fator = FATOR_DE_CONFORMIDADE[conformidade] # Pega o fator da situação de conformidade
    soma_dos_riscos = sum(max(PADROES_DE_DETECCAO[tipo].peso for tipo in tipos) * fator # Para cada campo, pega o maior peso entre os seus tipos e multiplica pelo fator
                          for tipos in tipos_por_campo if tipos) # Faz isso para todos os campos que têm tipo detectado, e soma tudo
    return round(100 * soma_dos_riscos / (PESO_MAXIMO * total_de_campos), 2) # Aplica a equação 8 e arredonda o resultado para 2 casas decimais
