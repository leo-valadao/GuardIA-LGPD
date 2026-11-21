def ocultar_senha_da_url(url): # Define a função, que recebe a URL de conexão
    """URL para exibir em tela e relatório, com a senha oculta."""
    return url.render_as_string(hide_password=True) # Devolve a URL como texto, com a senha trocada por ***
