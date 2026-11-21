import unicodedata # Importa o módulo unicodedata, que sabe separar as letras dos seus acentos


def normalizar_texto(texto): # Define a função, que recebe um texto
    """Minúsculas e sem acentos: 'Data de Nascimento' → 'data de nascimento'."""
    texto = unicodedata.normalize('NFKD', str(texto)) # Separa cada letra acentuada em duas partes: a letra e o acento
    return ''.join(caractere for caractere in texto if not unicodedata.combining(caractere)).lower() # Junta de novo só as letras, sem os acentos, e passa tudo para minúsculas
