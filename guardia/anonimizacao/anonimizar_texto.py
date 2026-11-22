from guardia.anonimizacao.constantes import CARACTERE_DA_MASCARA # Importa o caractere usado na censura
from guardia.deteccao.escanear_texto import escanear_texto # Importa a função que acha dados pessoais dentro de um texto
from guardia.enumeracoes.modo_de_anonimizacao import ModoDeAnonimizacao # Importa o enum com os modos de anonimização
from guardia.utilitarios.verificar_se_esta_vazio import verificar_se_esta_vazio # Importa a função que diz se um valor está vazio


def anonimizar_texto(texto, modo, substituidor, nomes_conhecidos=frozenset()):
    """Troca só os trechos com dado pessoal dentro de um texto livre. Retorna (texto, quantidade_de_trechos)."""
    if verificar_se_esta_vazio(texto): # Confere se o texto está vazio
        return texto, 0 # Devolve o texto como veio, com 0 trechos trocados
    trechos = escanear_texto(texto, nomes_conhecidos) # Acha os dados pessoais dentro do texto
    if not trechos: # Confere se nenhum dado pessoal foi achado
        return texto, 0 # Devolve o texto como veio, com 0 trechos trocados
    partes, posicao = [], 0 # Começa uma lista vazia de pedaços e a posição no começo do texto
    for trecho in trechos: # Passa por cada dado pessoal achado, na ordem do texto
        partes.append(texto[posicao:trecho.inicio]) # Guarda o pedaço do texto que vem antes do dado pessoal
        if modo == ModoDeAnonimizacao.MASCARAR: # Se o modo é censura
            partes.append(CARACTERE_DA_MASCARA * len(trecho.valor)) # Troca o dado por asteriscos, no mesmo tamanho
        else: # Se o modo é dado sintético
            partes.append(str(substituidor.substituir(trecho.tipo, trecho.valor))) # Troca o dado por um valor falso e coerente
        posicao = trecho.fim # Avança a posição para logo depois do dado pessoal
    partes.append(texto[posicao:]) # Guarda o pedaço do texto que vem depois do último dado pessoal
    return ''.join(partes), len(trechos) # Junta os pedaços num texto só e devolve junto com a quantidade de trechos trocados
