---
name: gardia-lgpd
description: Analisa arquivos CSV para conformidade com a LGPD. A skill age de forma interativa: primeiro detecta automaticamente as colunas em risco, depois pergunta ao usuário qual ação tomar (Gerar Relatório, Mascarar ou Sintetizar).
---
# GardIA LGPD

Skill de IA para análise de conformidade de bases de dados com a Lei Geral de Proteção de Dados (LGPD).

## Quando Usar
* O usuário envia um arquivo CSV ou estrutura de tabela pedindo verificação de LGPD.

## Fluxo de Trabalho (Passos Obrigatórios)

1. **Detecção Inicial (Automática):** Assim que o usuário enviar os dados ou arquivo CSV, não gere o relatório inteiro de imediato. Primeiramente, execute APENAS a detecção de dados pessoais (Nome, CPF, RG, E-mail, Data de Nascimento, Telefone, CEP).
2. **Apresentação e Pergunta:** Liste para o usuário de forma concisa quais colunas em risco foram encontradas. Em seguida, PERGUNTE explicitamente qual das seguintes tarefas ele deseja executar:
   * 1️⃣ **Gerar Relatório de Riscos**: Classificar os dados, calcular precisão/revocação e gerar o relatório detalhado em Markdown/PDF.
   * 2️⃣ **Mascarar Dados**: Aplicar a técnica de ocultação com asteriscos e entregar o arquivo CSV seguro.
   * 3️⃣ **Gerar Dados Sintéticos**: Substituir os dados originais por dados falsos realistas e entregar o arquivo CSV.
3. **Execução:** Aguarde a resposta do usuário e execute *apenas* a ferramenta/tarefa solicitada por ele.

## Módulos de Suporte
- `escanear_banco()`: Para o Passo 1.
- `classificar_dados()` e `gerar_relatorio()`: Para a opção 1.
- `mascarar()`: Para a opção 2.
- `substituir_por_sintetico()`: Para a opção 3.
