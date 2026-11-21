from guardia.utilitarios.verificar_se_esta_vazio import verificar_se_esta_vazio # Importa a função que diz se um valor está vazio


def converter_para_texto(valor): # Define a função, que recebe um valor de qualquer tipo
    """O valor como texto sem espaços nas pontas; vazio ("") se for None ou NaN."""
    return '' if verificar_se_esta_vazio(valor) else str(valor).strip() # Devolve texto vazio se o valor estiver vazio; senão, o valor como texto sem espaços nas pontas
