def gerar_relatorio(classificacao, metricas):
    """
    Gera o relatório formatado em Markdown com as métricas e a classificação de riscos.
    """
    relatorio = "### Relatório de Riscos e Classificação (GardIA-LGPD)\n\n"
    
    relatorio += "#### 1. Métricas de Avaliação da Identificação\n"
    relatorio += f"* **Precisão Estimada:** {metricas['precisao']}%\n"
    relatorio += f"* **Revocação Estimada:** {metricas['revocacao']}%\n"
    relatorio += f"* **Falsos Positivos Identificados:** {metricas['falsos_positivos']}\n"
    relatorio += f"* **Falsos Negativos Identificados:** {metricas['falsos_negativos']}\n\n"
    
    relatorio += "#### 2. Dados em Risco e Classificação\n\n"
    for coluna, info in classificacao.items():
        relatorio += f"* **{coluna}**\n"
        relatorio += f"    * **Classificação:** {info['tipo']}\n"
        relatorio += f"    * **Nível de Risco:** {info['risco']}\n"
        relatorio += f"    * **Mitigação:** {info['mitigacao']}\n"
        
    return relatorio
