from guardia.anonimizacao.constantes import CARACTERE_DA_MASCARA # Importa o caractere usado na censura
from guardia.anonimizacao.mascarar_valor import mascarar_valor # Importa a função que censura um valor
from guardia.deteccao.padroes import TIPOS_SENSIVEIS # Importa o conjunto dos tipos de dado sensível
from guardia.enumeracoes.modo_de_anonimizacao import ModoDeAnonimizacao # Importa o enum com os modos de anonimização
from guardia.enumeracoes.tipo_de_dado_pessoal import TipoDeDadoPessoal # Importa o enum com os tipos de dado pessoal
from guardia.utilitarios.verificar_se_esta_vazio import verificar_se_esta_vazio # Importa a função que diz se um valor está vazio


# Dado sensível censurado: o mesmo valor em TODAS as linhas, inclusive nas vazias,
# para a cópia não revelar nem o valor nem quem tem/não tem o dado (ex.: quem é filiado).
MASCARA_DE_DADO_SENSIVEL = CARACTERE_DA_MASCARA * 8 # Oito asteriscos seguidos


def anonimizar_registro(registro, tipos, modo, substituidor, forcar_sintetico=(), achados=None): # Define a função, que recebe a linha da tabela, o tipo de cada coluna, o modo e o substituidor
    """
    Anonimiza um registro (dict coluna → valor). 'tipos' = {coluna: tipo detectado}.
    Os nomes são tratados primeiro para o e-mail sintético usar o nome sintético da pessoa.
    'achados' = {coluna: Achado}, necessário para sortear os dados sensíveis.
    """
    registro_anonimizado = dict(registro) # Faz uma cópia da linha, para não alterar a original
    colunas_em_ordem = sorted(tipos, key=lambda coluna: tipos[coluna] != TipoDeDadoPessoal.NOME) # Coloca as colunas de nome primeiro e as outras depois
    nome_sintetico = None # Ainda não há nome sintético para montar o e-mail
    for coluna in colunas_em_ordem: # Passa por cada coluna com dado pessoal, na ordem acima
        tipo, valor = tipos[coluna], registro.get(coluna) # Pega o tipo da coluna e o valor dela nesta linha
        if tipo in TIPOS_SENSIVEIS:                       # Todas as linhas, inclusive as vazias
            if modo == ModoDeAnonimizacao.MASCARAR: # Se o modo é censura
                registro_anonimizado[coluna] = MASCARA_DE_DADO_SENSIVEL # Troca o valor pela máscara de dado sensível
            else: # Se o modo é dado sintético
                registro_anonimizado[coluna] = substituidor.sortear_dado_sensivel(achados[coluna]) # Sorteia um valor falso para o dado sensível
            continue # Pula para a próxima coluna
        if modo == ModoDeAnonimizacao.MASCARAR and coluna not in forcar_sintetico: # Se o modo é censura e a coluna não é chave
            registro_anonimizado[coluna] = mascarar_valor(valor) # Censura o valor
        else: # Se o modo é sintético, ou se a coluna é chave
            registro_anonimizado[coluna] = substituidor.substituir(tipo, valor, nome=nome_sintetico) # Troca o valor por um valor falso e coerente
            if tipo == TipoDeDadoPessoal.NOME and nome_sintetico is None and not verificar_se_esta_vazio(valor): # Confere se esta é a primeira coluna de nome preenchida
                nome_sintetico = registro_anonimizado[coluna] # Guarda o nome falso para montar o e-mail da mesma pessoa
    return registro_anonimizado # Devolve a linha anonimizada
