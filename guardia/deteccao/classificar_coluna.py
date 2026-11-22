import re # Importa o módulo re, de expressões regulares (busca de padrões em texto)

from guardia.deteccao.validar_cpf import validar_cpf # Importa a função que confere os dígitos verificadores do CPF
from guardia.deteccao.padroes import PADROES_DE_DETECCAO, TIPOS_SENSIVEIS # Importa a tabela de regras de cada tipo e o conjunto dos tipos sensíveis
from guardia.deteccao.validar_nome_de_pessoa import validar_nome_de_pessoa # Importa a função que diz se um valor tem cara de nome de pessoa
from guardia.deteccao.identificar_tipos_pelo_contexto import identificar_tipos_pelo_contexto # Importa a função que diz quais tipos o nome da coluna indica
from guardia.enumeracoes.forca_do_padrao import ForcaDoPadrao # Importa o enum com as forças do padrão (forte ou fraco)
from guardia.enumeracoes.tipo_de_dado_pessoal import TipoDeDadoPessoal # Importa o enum com os tipos de dado pessoal
from guardia.modelos.achado import Achado # Importa a classe que guarda o resultado da detecção
from guardia.utilitarios.converter_para_texto import converter_para_texto # Importa a função que transforma qualquer valor em texto


# Fração mínima da amostra de uma coluna que precisa casar com o padrão
LIMIAR_DE_DETECCAO = 0.5 # Metade da amostra (0,5 = 50%)

# Valor inteiro da coluna casando com o padrão (fullmatch)
_EXPRESSOES_REGULARES_DOS_VALORES = { # Cria o dicionário: cada tipo e a sua expressão regular já preparada para uso
    tipo: re.compile(padrao.expressao_regular) # Prepara (compila) a expressão regular do tipo, para a busca ficar mais rápida
    for tipo, padrao in PADROES_DE_DETECCAO.items() if padrao.expressao_regular # Passa por todos os tipos que têm expressão regular
}


def classificar_coluna(nome_da_coluna, valores):
    """Aplica D = F ∨ (W ∧ C) a uma amostra de valores. Retorna um Achado ou None."""
    amostra = [texto for texto in (converter_para_texto(valor) for valor in valores) if texto] # Transforma cada valor em texto e descarta os vazios

    if not amostra: # Confere se não sobrou nenhum valor preenchido
        return None # Sem valores, não há o que detectar: devolve None (nada)

    tipos_indicados_pelo_contexto = identificar_tipos_pelo_contexto(nome_da_coluna) # Descobre quais tipos o nome da coluna indica (o C da regra)
    total_da_amostra = len(amostra) # Conta quantos valores preenchidos há na amostra
    candidatos = [] # Lista que vai guardar todos os tipos que a coluna pode ser

    def criar_achado(tipo, forca, taxa, tem_contexto):
        """Monta um Achado para o tipo."""
        padrao = PADROES_DE_DETECCAO[tipo] # Pega as regras do tipo na tabela de padrões
        return Achado(tipo, forca, padrao.peso, taxa, tem_contexto, sensivel=tipo in TIPOS_SENSIVEIS) # Cria e devolve o Achado com os dados do tipo

    for tipo, padrao in PADROES_DE_DETECCAO.items(): # Testa a coluna contra cada tipo de dado da tabela
        if tipo == TipoDeDadoPessoal.NOME: # O nome de pessoa não tem expressão regular, então é testado de outro jeito
            if TipoDeDadoPessoal.NOME in tipos_indicados_pelo_contexto:                          # W ∧ C
                taxa = sum(validar_nome_de_pessoa(valor) for valor in amostra) / total_da_amostra # Calcula a parte da amostra que tem cara de nome de pessoa
                if taxa >= LIMIAR_DE_DETECCAO: # Confere se pelo menos metade da amostra tem cara de nome
                    candidatos.append(criar_achado(tipo, ForcaDoPadrao.FRACO, taxa, True)) # Guarda o nome como candidato, detectado por padrão fraco com contexto
            continue # Pula para o próximo tipo da tabela

        valores_que_casam = [valor for valor in amostra if _EXPRESSOES_REGULARES_DOS_VALORES[tipo].fullmatch(valor)] # Separa os valores que têm exatamente o formato do tipo
        taxa_do_formato = len(valores_que_casam) / total_da_amostra # Calcula a parte da amostra que tem o formato do tipo
        if tipo == TipoDeDadoPessoal.CPF: # O CPF só é padrão forte quando os dígitos verificadores estão certos
            taxa_do_padrao_forte = sum(validar_cpf(valor) for valor in valores_que_casam) / total_da_amostra # Calcula a parte da amostra que é CPF válido
        else: # Para os outros tipos
            taxa_do_padrao_forte = taxa_do_formato if padrao.forca == ForcaDoPadrao.FORTE else 0.0 # Usa a taxa do formato se o tipo for forte; se for fraco, a taxa forte é 0

        tem_contexto = tipo in tipos_indicados_pelo_contexto # Confere se o nome da coluna indica este tipo
        if taxa_do_padrao_forte >= LIMIAR_DE_DETECCAO:                                           # F
            candidatos.append(criar_achado(tipo, ForcaDoPadrao.FORTE, taxa_do_padrao_forte, tem_contexto)) # Guarda o tipo como candidato, detectado por padrão forte
        elif taxa_do_formato >= LIMIAR_DE_DETECCAO and tem_contexto:                             # W ∧ C
            candidatos.append(criar_achado(tipo, ForcaDoPadrao.FRACO, taxa_do_formato, True)) # Guarda o tipo como candidato, detectado por padrão fraco com contexto

    if not candidatos: # Confere se nenhum tipo combinou com a coluna
        return None # Nenhum dado pessoal detectado: devolve None (nada)
    # Prioridade: o tipo que o nome da coluna indica; depois padrão forte; depois a maior taxa
    achado = max(candidatos, key=lambda achado_candidato: (achado_candidato.tem_contexto, # Escolhe o melhor candidato: primeiro o que tem contexto
                                                           achado_candidato.forca == ForcaDoPadrao.FORTE, # Depois o de padrão forte
                                                           achado_candidato.taxa, # Depois o de maior taxa
                                                           achado_candidato.peso)) # Por último, o de maior peso

    if achado.sensivel: # Confere se o tipo escolhido é dado sensível
        achado.valores_observados = tuple(sorted(set(amostra))) # Guarda os valores diferentes da amostra, em ordem, para o sorteio do dado sintético
        achado.taxa_de_preenchimento = total_da_amostra / len(valores) # Guarda a parte das linhas que tem valor preenchido

    return achado # Devolve o Achado escolhido
