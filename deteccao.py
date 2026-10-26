import pandas as pd

def escanear_banco(df):
    """
    Escaneia um DataFrame e identifica colunas que contêm dados pessoais
    com base em palavras-chave ou padrões (insensível a hífens, sublinhados e maiúsculas).
    """
    colunas_pessoais = []
    termos_chave = ['nome', 'cpf', 'rg', 'email', 'nascimento', 'telefone', 'cep', 'celular', 'fone']
    
    for coluna in df.columns:
        # Normaliza o nome da coluna removendo caracteres especiais
        coluna_limpa = coluna.lower().replace('-', '').replace('_', '').replace(' ', '')
        if any(termo in coluna_limpa for termo in termos_chave):
            colunas_pessoais.append(coluna)
            
    return colunas_pessoais
