"""
Ajustes para o texto aparecer certo em qualquer terminal (Windows, Linux e IntelliJ).

O único caso que precisa de ajuste é o PowerShell do Windows recebendo a saída do
Python por um pipe (ex.: "python cli.py ... | Out-File"): o Python escreve em UTF-8,
mas o PowerShell 5.1 em português lê usando a página de código do console (850) e
os acentos ficam embaralhados ("Análise" vira "AnÃ¡lise").

Nos outros casos nada muda, porque o texto já sai certo:
  - terminal de verdade (PowerShell, cmd, Windows Terminal, terminal do IntelliJ,
    terminal do Linux): o Python escreve direto no console;
  - console de execução/debug do IntelliJ: a IDE lê em UTF-8;
  - Git Bash e terminais do Linux: leem em UTF-8.

O cli.py e o main.py rodam pelo executar(): ele chama o configurar_terminal() e, se o
usuário cancelar ou acontecer um erro do GuardIA ou do banco, mostra só uma mensagem
clara em vez do erro técnico (traceback).

Arquivos (um por função pública):
  configurar_terminal.py  configurar_terminal: Ajusta a saída do programa para os acentos aparecerem certos em qualquer terminal.
  executar.py             executar: Roda o programa e, se ele for cancelado ou der erro, mostra só uma mensagem clara.
"""
