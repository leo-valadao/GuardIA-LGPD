def classificar_dados(colunas_identificadas):
    """
    Atribui a classificação LGPD e o nível de risco para as colunas encontradas.
    """
    classificacao_final = {}
    
    regras = {
        'cpf': {'tipo': 'Dado Pessoal Direto', 'risco': 'Crítico', 'mitigacao': 'Mascarar 6 dígitos'},
        'rg': {'tipo': 'Dado Pessoal Direto', 'risco': 'Alto', 'mitigacao': 'Mascarar prefixo/sufixo'},
        'nome': {'tipo': 'Dado Pessoal Direto', 'risco': 'Alto', 'mitigacao': 'Ocultar sobrenome'},
        'email': {'tipo': 'Dado Pessoal Direto', 'risco': 'Alto', 'mitigacao': 'Ocultar prefixo do usuário'},
        'telefone': {'tipo': 'Dado Pessoal Direto', 'risco': 'Alto', 'mitigacao': 'Ocultar os 4 últimos dígitos'},
        'nascimento': {'tipo': 'Dado Pessoal Indireto', 'risco': 'Médio', 'mitigacao': 'Reter apenas o ano'},
        'cep': {'tipo': 'Dado Pessoal Indireto', 'risco': 'Baixo/Médio', 'mitigacao': 'Ocultar os 3 últimos dígitos'}
    }
    
    for coluna in colunas_identificadas:
        coluna_lower = coluna.lower()
        classificacao_final[coluna] = {'tipo': 'Requer Análise Manual', 'risco': 'Desconhecido', 'mitigacao': 'N/A'}
        
        for chave, info in regras.items():
            if chave in coluna_lower:
                classificacao_final[coluna] = info
                break
                
    return classificacao_final
