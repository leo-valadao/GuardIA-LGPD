---
name: guardia-lgpd
description: Analisa bancos de dados PostgreSQL para conformidade com a LGPD e gera uma cópia anonimizada. A skill age de forma interativa: primeiro detecta automaticamente as colunas e textos em risco, depois pergunta ao usuário qual ação tomar (Gerar Relatório, Censurar ou Sintetizar).
---
# GuardIA LGPD

Skill de IA para análise de conformidade de bases de dados com a Lei Geral de Proteção de Dados (LGPD).

## Quando Usar
* O usuário pede verificação de LGPD de um banco de dados PostgreSQL (host, porta, banco, usuário).

## Regras de Segurança (Obrigatórias)
* **Nunca peça a senha do banco na conversa.** A senha deve estar na variável de ambiente
  `PGPASSWORD`, configurada pelo próprio usuário antes de iniciar o agente. Se ela não estiver
  definida, explique isso ao usuário e espere.
* O banco original é sempre aberto em modo somente leitura; a remediação acontece em uma **cópia**.
* Nunca mostre valores reais de dados pessoais nas respostas: cite apenas tabelas, colunas, tipos e quantidades.

## Fluxo de Trabalho (Passos Obrigatórios)

1. **Detecção Inicial (Automática):** Assim que o usuário informar o banco, não gere a cópia de
   imediato. Primeiro, execute APENAS a detecção de dados pessoais (Nome, CPF, RG, E-mail, Data de
   Nascimento, Telefone, CEP, e os sensíveis Tipo Sanguíneo e Filiação Sindical), com `analisar_banco_dados`.
2. **Apresentação e Pergunta:** Liste de forma concisa as colunas e os textos livres em risco, por tabela,
   e os avisos de possíveis dados sensíveis. Em seguida, PERGUNTE explicitamente qual tarefa ele deseja:
   * 1️⃣ **Gerar Relatório de Riscos**: Entregar o relatório em Markdown (classificação, score de risco por tabela).
   * 2️⃣ **Censurar Dados**: Gerar a cópia com os dados pessoais trocados por asteriscos (`modo = mascarar`).
   * 3️⃣ **Gerar Dados Sintéticos**: Gerar a cópia com dados falsos coerentes (`modo = sintetico`).
3. **Execução:** Aguarde a resposta do usuário e execute *apenas* a tarefa solicitada, com
   `gerar_copia_anonimizada`. Informe o nome do banco de cópia gerado.
4. **Interpretação:** Explique os achados em linguagem natural e recomende as ações de remediação.
   Lembre que o GuardIA é uma ferramenta de apoio e não substitui a análise jurídica.

## Ferramentas (`tools.json` → `guardia/ferramentas/`)
- `analisar_banco_dados(host, banco, usuario, porta)`: Passo 1 e opção 1.
- `gerar_copia_anonimizada(host, banco, usuario, modo, porta, destino)`: opções 2 e 3.

Sem suporte a function calling, use a CLI: `python cli.py --host <host> --banco <banco> --usuario <usuario> -m apenas_relatorio|mascarar|sintetico`.
