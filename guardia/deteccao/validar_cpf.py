import re # Importa o módulo re, de expressões regulares (busca de padrões em texto)

from guardia.deteccao.calcular_digitos_verificadores_do_cpf import calcular_digitos_verificadores_do_cpf # Importa a função que calcula os 2 dígitos verificadores do CPF


def validar_cpf(cpf):
    """CPF com 11 dígitos, não repetidos, e dígitos verificadores corretos."""
    digitos = re.sub(r'\D', '', str(cpf)) # Remove todos os caracteres que não são digitos.

    if len(digitos) != 11 or len(set(digitos)) == 1: # Checa se o CPF não tem 11 digitos ou se todos os digitos são iguais.
        return False # Devolve falso: o CPF é inválido

    # Verifica se os digitos verificadores do CPF são validos.
    digitos_verificadores_esperados = calcular_digitos_verificadores_do_cpf(digitos[:9]) # Calcula os 2 dígitos verificadores a partir dos 9 primeiros dígitos
    digitos_verificadores_informados = (int(digitos[9]), int(digitos[10])) # Pega os 2 últimos dígitos do CPF informado, como números

    return digitos_verificadores_esperados == digitos_verificadores_informados # Devolve verdadeiro se os dígitos calculados forem iguais aos informados
