def verificar_se_esta_vazio(valor):
    """None ou NaN."""
    if valor is None: # Confere se o valor é None (sem valor nenhum)
        return True # Devolve verdadeiro: o valor está vazio
    try: # Tenta fazer a comparação abaixo; alguns tipos não deixam comparar
        return bool(valor != valor)   # NaN é diferente de si mesmo
    except (TypeError, ValueError): # Se o tipo do valor não permitiu a comparação
        return False # Devolve falso: o valor não está vazio
