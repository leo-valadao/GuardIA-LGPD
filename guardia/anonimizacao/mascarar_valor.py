import datetime # Importa o módulo datetime, que trabalha com datas e horas
from decimal import Decimal # Importa o Decimal, o tipo de número usado para valores com casas decimais exatas

from guardia.anonimizacao.constantes import CARACTERE_DA_MASCARA # Importa o caractere usado na censura
from guardia.utilitarios.verificar_se_esta_vazio import verificar_se_esta_vazio # Importa a função que diz se um valor está vazio


def mascarar_valor(valor): # Define a função, que recebe o valor a ser censurado
    """Máscara total: texto → '*' no mesmo tamanho; data → 1.º de janeiro do mesmo ano."""
    if verificar_se_esta_vazio(valor): # Confere se o valor está vazio
        return valor # Valor vazio continua vazio
    if isinstance(valor, datetime.datetime): # Confere se o valor é uma data com hora
        return valor.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0) # Mantém só o ano: vira 1.º de janeiro, à meia-noite
    if isinstance(valor, datetime.date): # Confere se o valor é uma data sem hora
        return valor.replace(month=1, day=1) # Mantém só o ano: vira 1.º de janeiro
    if isinstance(valor, (int, float, Decimal)) and not isinstance(valor, bool): # Confere se o valor é um número (verdadeiro e falso não contam)
        return type(valor)(0) # Troca o número por zero, do mesmo tipo do original
    return CARACTERE_DA_MASCARA * len(str(valor).strip()) # Troca o texto por asteriscos, no mesmo tamanho
