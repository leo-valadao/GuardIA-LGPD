def sugerir_nome_do_destino(url_de_origem): # Define a função, que recebe a URL do banco de origem
    """Nome padrão do banco de cópia: <banco de origem>_anonimizado."""
    return f'{url_de_origem.database}_anonimizado' # Devolve o nome do banco de origem com "_anonimizado" no fim
