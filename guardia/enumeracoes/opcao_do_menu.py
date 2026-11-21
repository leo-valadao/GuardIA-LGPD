from enum import StrEnum # Importa o StrEnum, um tipo de enum em que cada opção também é um texto


class OpcaoDoMenu(StrEnum): # Define o enum com as opções do menu do modo interativo
    """Opções do menu do modo interativo (main.py): o número que o usuário digita."""
    GERAR_RELATORIO = '1'            # Gera só o relatório de riscos
    GERAR_COPIA_CENSURADA = '2'      # Gera a cópia do banco com os dados censurados
    GERAR_COPIA_SINTETICA = '3'      # Gera a cópia do banco com dados sintéticos
    SAIR = '4'                       # Encerra o programa
