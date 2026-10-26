import pandas as pd
import sys
from deteccao import escanear_banco
from classificacao import classificar_dados
from avaliar import calcular_precisao_revocacao
from relatorio import gerar_relatorio
from anonimo import mascarar, substituir_por_sintetico

def main():
    print("=== GardIA-LGPD (Modo Interativo) ===")
    arquivo = input("Digite o caminho do arquivo CSV (ex: amostra.csv): ")
    
    try:
        df = pd.read_csv(arquivo)
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        sys.exit(1)
        
    print("\n[Passo 1] Executando detecção inicial de dados em risco...")
    colunas_risco = escanear_banco(df)
    
    if not colunas_risco:
        print("✅ Nenhum dado pessoal sensível encontrado nas colunas.")
        sys.exit(0)
        
    print(f"\n⚠️ Atenção! Encontramos {len(colunas_risco)} coluna(s) com dados pessoais: {', '.join(colunas_risco)}")
    
    print("\n[Passo 2] O que você deseja fazer com esses dados?")
    print("1️⃣ - Gerar Relatório de Riscos e Métricas (Markdown)")
    print("2️⃣ - Mascarar dados (Substituir por *)")
    print("3️⃣ - Gerar Dados Sintéticos (Substituir por dados falsos usando Faker)")
    print("4️⃣ - Sair")
    
    escolha = input("\nDigite o número da tarefa desejada: ")
    
    if escolha == '1':
        print("\nGerando relatório...")
        classificacao = classificar_dados(colunas_risco)
        metricas = calcular_precisao_revocacao(colunas_risco, colunas_risco)
        relatorio = gerar_relatorio(classificacao, metricas)
        print("\n" + relatorio)
        
    elif escolha == '2':
        print("\nMascarando dados...")
        df_mascarado = mascarar(df, colunas_risco)
        output = "dados_mascarados.csv"
        df_mascarado.to_csv(output, index=False)
        print(f"✅ Dados mascarados com sucesso! Salvo em: {output}")
        
    elif escolha == '3':
        print("\nGerando dados sintéticos...")
        mapeamento = {col: col for col in colunas_risco}
        df_sintetico = substituir_por_sintetico(df, mapeamento)
        output = "dados_sinteticos.csv"
        df_sintetico.to_csv(output, index=False)
        print(f"✅ Dados sintéticos gerados com sucesso! Salvo em: {output}")
        
    else:
        print("Operação encerrada.")

if __name__ == "__main__":
    main()
