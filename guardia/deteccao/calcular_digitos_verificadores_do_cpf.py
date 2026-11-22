def calcular_digitos_verificadores_do_cpf(nove_digitos):
    """Dígitos verificadores do CPF, equações (5), (6) e (7) do artigo."""
    digitos = [int(caractere) for caractere in nove_digitos] # Transforma o texto com os 9 dígitos em uma lista de números.

    # No Python a posição começa em 0; no artigo, i começa em 1 (i = posicao + 1).
    # Por isso o peso (11 − i) do artigo vira (10 − posicao) aqui, e (12 − i) vira (11 − posicao).

    # Equações (5) e (6): S1 = Σ d_i · (11 − i), com i = 1..9
    primeira_soma = sum(digitos[posicao] * (10 - posicao) for posicao in range(9)) # Multiplica cada um dos 9 primeiros dígitos pelo seu peso (10, 9, 8, ..., 2) e soma os resultados.
    primeiro_resto = primeira_soma % 11 # Resto da divisão da 1.ª soma por 11 (o operador % dá o resto da divisão, chamado de "módulo 11").
    primeiro_digito_verificador = 0 if primeiro_resto < 2 else 11 - primeiro_resto # Define o 1.º dígito verificador: 0 se o resto for 0 ou 1; senão, 11 menos o resto.

    # Equação (7): S2 = Σ d_i · (12 − i), com i = 1..9, + 2 · DV1
    segunda_soma = sum(digitos[posicao] * (11 - posicao) for posicao in range(9)) + 2 * primeiro_digito_verificador # Multiplica os 9 primeiros dígitos pelos pesos (11, 10, ..., 3), soma os resultados e soma também 2 vezes o 1.º dígito verificador.
    segundo_resto = segunda_soma % 11 # Resto da divisão da 2.ª soma por 11.
    segundo_digito_verificador = 0 if segundo_resto < 2 else 11 - segundo_resto # Define o 2.º dígito verificador, com a mesma regra do 1.º.

    return primeiro_digito_verificador, segundo_digito_verificador # Retorna o 1.º e o 2.º dígitos verificadores.
