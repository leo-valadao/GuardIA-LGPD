import argparse
import pandas as pd
from deteccao import escanear_banco
from classificacao import classificar_dados
from avaliar import calcular_precisao_revocacao
from relatorio import gerar_relatorio
from anonimo import mascarar, substituir_por_sintetico

def main():
    parser = argparse.ArgumentParser(description="GardIA-LGPD CLI: Análise e Anonimização de CSVs")
    parser.add_argument("--input", "-i", required=True, help="Caminho do arquivo CSV de entrada")
    parser.add_argument("--output", "-o", default="dados_anonimizados.csv", help="Caminho do CSV de saída")
    parser.add_argument("--modo", "-m", choices=["mascarar", "sintetico", "apenas_relatorio"], default="sintetico", help="Modo de operação")
    parser.add_argument("--relatorio_out", "-r", default="relatorio_lgpd.md", help="Caminho para salvar o relatório Markdown")

    args = parser.parse_args()

    print(f"Lendo arquivo: {args.input}...")
    df = pd.read_csv(args.input)

    colunas_risco = escanear_banco(df)
    classificacao = classificar_dados(colunas_risco)
    metricas = calcular_precisao_revocacao(colunas_risco, colunas_risco)

    texto_relatorio = gerar_relatorio(classificacao, metricas)
    with open(args.relatorio_out, 'w', encoding='utf-8') as f:
        f.write(texto_relatorio)
    print(f"Relatório gerado em: {args.relatorio_out}")

    if args.modo == "mascarar":
        df_res = mascarar(df, colunas_risco)
        df_res.to_csv(args.output, index=False)
        print(f"Dados mascarados salvos em: {args.output}")

    elif args.modo == "sintetico":
        mapeamento = {col: col for col in colunas_risco}
        df_res = substituir_por_sintetico(df, mapeamento)
        df_res.to_csv(args.output, index=False)
        print(f"Dados sintéticos salvos em: {args.output}")

if __name__ == "__main__":
    main()
