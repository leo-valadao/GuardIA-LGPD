import pandas as pd
from faker import Faker

fake = Faker('pt_BR')

def mascarar(df, colunas):
    """
    Substitui todos os caracteres dos dados nas colunas especificadas por '*'.
    """
    df_mascarado = df.copy()
    
    for coluna in colunas:
        if coluna in df_mascarado.columns:
            df_mascarado[coluna] = df_mascarado[coluna].apply(
                lambda x: '*' * len(str(x).strip()) if pd.notna(x) else x
            )
            
    return df_mascarado

def substituir_por_sintetico(df, mapeamento_colunas):
    """
    Substitui os dados originais por dados falsos (sintéticos) realistas.
    """
    df_sintetico = df.copy()
    total_linhas = len(df_sintetico)
    
    for coluna, tipo in mapeamento_colunas.items():
        if coluna in df_sintetico.columns:
            if tipo.lower() == 'nome':
                df_sintetico[coluna] = [fake.name() for _ in range(total_linhas)]
            elif tipo.lower() == 'cpf':
                df_sintetico[coluna] = [fake.cpf() for _ in range(total_linhas)]
            elif tipo.lower() == 'rg':
                df_sintetico[coluna] = [fake.rg() for _ in range(total_linhas)]
            elif tipo.lower() == 'email':
                df_sintetico[coluna] = [fake.email() for _ in range(total_linhas)]
            elif tipo.lower() == 'telefone':
                df_sintetico[coluna] = [fake.phone_number() for _ in range(total_linhas)]
            elif tipo.lower() == 'cep':
                df_sintetico[coluna] = [fake.postcode() for _ in range(total_linhas)]
            elif 'data' in tipo.lower() or 'nascimento' in tipo.lower():
                df_sintetico[coluna] = [fake.date_of_birth(minimum_age=18, maximum_age=85).strftime('%d/%m/%Y') for _ in range(total_linhas)]
            else:
                df_sintetico[coluna] = [fake.word() for _ in range(total_linhas)]
                
    return df_sintetico
