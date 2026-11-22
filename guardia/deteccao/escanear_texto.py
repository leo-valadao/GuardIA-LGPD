import re # Importa o módulo re, de expressões regulares (busca de padrões em texto)

from guardia.deteccao.validar_cpf import validar_cpf # Importa a função que confere os dígitos verificadores do CPF
from guardia.deteccao.padroes import PADROES_DE_DETECCAO # Importa a tabela com as regras de cada tipo de dado pessoal
from guardia.enumeracoes.tipo_de_dado_pessoal import TipoDeDadoPessoal # Importa o enum com os tipos de dado pessoal
from guardia.modelos.trecho import Trecho # Importa a classe que guarda um dado pessoal achado no texto
from guardia.utilitarios.normalizar_texto import normalizar_texto # Importa a função que deixa o texto em minúsculas e sem acentos
from guardia.utilitarios.converter_para_texto import converter_para_texto # Importa a função que transforma qualquer valor em texto


# Quantas palavras antes do valor são olhadas para achar contexto em texto livre
JANELA_DE_CONTEXTO_NO_TEXTO = 4 # O GuardIA olha as 4 palavras que vêm antes do valor

# Ordem da busca no texto: padrões fortes primeiro, depois os fracos (que precisam de contexto)
_TIPOS_NA_ORDEM_DE_BUSCA = ( # Cria a tupla (lista que não muda) com os tipos na ordem em que são procurados
    TipoDeDadoPessoal.EMAIL, TipoDeDadoPessoal.CPF, TipoDeDadoPessoal.TELEFONE, # Primeiro o e-mail e o CPF (fortes), depois o telefone
    TipoDeDadoPessoal.CEP, TipoDeDadoPessoal.DATA_DE_NASCIMENTO, TipoDeDadoPessoal.RG, # Por último o CEP, a data de nascimento e o RG
)

# Trecho dentro de um texto casando com o padrão (sem dígito colado antes ou depois)
_EXPRESSOES_REGULARES_DOS_TEXTOS = { # Cria o dicionário: cada tipo e a expressão regular usada para achá-lo no meio de um texto
    tipo: re.compile(padrao.expressao_regular if tipo == TipoDeDadoPessoal.EMAIL # O e-mail usa a expressão regular do jeito que está na tabela
                     else rf'(?<!\d){padrao.expressao_regular}(?!\d)') # Os outros tipos não podem ter dígito colado antes nem depois
    for tipo, padrao in PADROES_DE_DETECCAO.items() if padrao.expressao_regular # Passa por todos os tipos que têm expressão regular
}
_EXPRESSAO_REGULAR_DE_PALAVRA = re.compile(r"[A-Za-zÀ-ÿ]+") # Padrão de uma palavra: uma ou mais letras seguidas, com ou sem acento


def escanear_texto(texto, nomes_conhecidos=frozenset()):
    """Dados pessoais dentro de um texto livre (ex.: atendimentos.descricao)."""
    texto = converter_para_texto(texto) # Transforma o valor em texto
    if not texto: # Confere se o texto está vazio
        return [] # Texto vazio: devolve uma lista vazia
    trechos = [] # Lista que vai guardar os dados pessoais encontrados

    def verificar_posicao_livre(inicio, fim):
        """Diz se um pedaço do texto ainda não foi usado por nenhum trecho encontrado."""
        return all(fim <= trecho.inicio or inicio >= trecho.fim for trecho in trechos) # Devolve verdadeiro se o pedaço não encosta em nenhum trecho já encontrado

    for tipo in _TIPOS_NA_ORDEM_DE_BUSCA: # Procura cada tipo de dado, na ordem definida acima
        for ocorrencia in _EXPRESSOES_REGULARES_DOS_TEXTOS[tipo].finditer(texto): # Passa por cada pedaço do texto que tem o formato do tipo
            if not verificar_posicao_livre(ocorrencia.start(), ocorrencia.end()): # Confere se esse pedaço já faz parte de outro dado encontrado
                continue # Pula para o próximo pedaço
            tem_padrao_forte = (tipo == TipoDeDadoPessoal.EMAIL # É padrão forte se for e-mail
                                or (tipo == TipoDeDadoPessoal.CPF and validar_cpf(ocorrencia.group()))) # Ou se for CPF com os dígitos verificadores certos
            if tem_padrao_forte or _verificar_contexto_antes_do_valor(texto, ocorrencia.start(), tipo): # Aceita o pedaço se é padrão forte ou se há palavra de contexto antes dele
                trechos.append(Trecho(ocorrencia.start(), ocorrencia.end(), tipo, ocorrencia.group())) # Guarda o dado encontrado, com a posição dele no texto

    if nomes_conhecidos: # Confere se foram informados nomes de pessoas conhecidos
        for trecho in _encontrar_nomes_conhecidos(texto, nomes_conhecidos): # Passa por cada nome conhecido achado no texto
            if verificar_posicao_livre(trecho.inicio, trecho.fim): # Confere se o nome não está em cima de outro dado já encontrado
                trechos.append(trecho) # Guarda o nome encontrado

    return sorted(trechos, key=lambda trecho: trecho.inicio) # Devolve os dados encontrados na ordem em que aparecem no texto


def _verificar_contexto_antes_do_valor(texto, inicio, tipo):
    """True se uma palavra de contexto do tipo aparece pouco antes do valor no texto."""
    palavras = normalizar_texto(texto[:inicio]).split()[-JANELA_DE_CONTEXTO_NO_TEXTO:] # Pega o texto antes do valor, sem acentos, e fica com as últimas 4 palavras
    partes_das_palavras = [parte for palavra in palavras for parte in re.split(r'[^a-z0-9]+', palavra) if parte] # Corta cada palavra em tudo que não é letra nem número
    # Junta cada parte com a seguinte, para achar também os termos escritos com hífen no meio
    partes_das_palavras += [''.join(partes_das_palavras[posicao:posicao + 2]) # Acrescenta à lista cada parte grudada na parte seguinte
                            for posicao in range(len(partes_das_palavras))] # Passa por todas as posições da lista de partes
    termos_de_contexto = PADROES_DE_DETECCAO[tipo].termos_de_contexto # Pega os termos de contexto do tipo na tabela de padrões
    return any(parte.startswith(termo) for parte in partes_das_palavras for termo in termos_de_contexto) # Devolve verdadeiro se alguma parte começa com algum termo de contexto


def _encontrar_nomes_conhecidos(texto, nomes_conhecidos):
    """Acha nomes já conhecidos (das colunas de nome) dentro do texto, do mais longo ao mais curto."""
    trechos = [] # Lista que vai guardar os nomes encontrados
    palavras = list(_EXPRESSAO_REGULAR_DE_PALAVRA.finditer(texto)) # Acha todas as palavras do texto, com a posição de cada uma
    indice_inicial = 0 # Começa pela primeira palavra do texto
    while indice_inicial < len(palavras): # Repete enquanto ainda houver palavras para testar
        achou = False # Ainda não achou nenhum nome começando nesta palavra
        for indice_final in range(min(indice_inicial + 6, len(palavras)), indice_inicial + 1, -1): # Testa grupos de até 6 palavras, do maior para o menor
            inicio, fim = palavras[indice_inicial].start(), palavras[indice_final - 1].end() # Pega onde o grupo de palavras começa e termina no texto
            candidato = texto[inicio:fim] # Recorta do texto o grupo de palavras
            if candidato in nomes_conhecidos: # Confere se esse grupo é um nome de pessoa conhecido
                trechos.append(Trecho(inicio, fim, TipoDeDadoPessoal.NOME, candidato)) # Guarda o nome encontrado, com a posição dele no texto
                indice_inicial, achou = indice_final, True # Pula para a palavra logo depois do nome e marca que achou
                break # Para de testar grupos menores
        if not achou: # Confere se nenhum nome começa nesta palavra
            indice_inicial += 1 # Passa para a próxima palavra
    return trechos # Devolve a lista de nomes encontrados
