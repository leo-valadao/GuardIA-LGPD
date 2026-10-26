# GardIA-LGPD 🛡️

Skill modular e biblioteca Python para análise, auditoria (precisão/revocação), classificação e anonimização de dados pessoais de acordo com a LGPD (Lei Geral de Proteção de Dados).

Projetada para ser **100% compatível com qualquer IA ou agente de desenvolvimento** (ChatGPT/Custom GPTs, Claude Code, LangChain, AutoGen, CrewAI, Ollama, Aider, Cursor, etc.).

---

## 📁 Estrutura do Repositório

| Arquivo / Módulo | Descrição |
| :--- | :--- |
| `SKILL.md` | Instruções da Skill no padrão de Agentes de IA (YAML Frontmatter + Markdown). |
| `tools.json` | Definição de Function Calling / Tools em JSON Schema (OpenAI, Anthropic, LangChain). |
| `deteccao.py` | Função `escanear_banco(df)` para mapear colunas sensíveis. |
| `classificacao.py` | Função `classificar_dados(colunas)` para atribuir nível de risco. |
| `avaliar.py` | Função `calcular_precisao_revocacao()` para auditoria de acurácia. |
| `relatorio.py` | Função `gerar_relatorio()` para gerar a documentação Markdown. |
| `anonimo.py` | Funções `mascarar()` e `substituir_por_sintetico()` com `Faker`. |
| `cli.py` | Interface de Linha de Comando (CLI) para execução direta no terminal. |
| `main.py` | Script de orquestração de exemplo. |
| `test_gardia.py` | Suíte de testes unitários (`unittest`). |
| `requirements.txt` | Dependências (`pandas`, `faker`, `numpy`). |
| `LICENSE` | Licença Open Source (MIT). |

---

## 🚀 Como Usar em Qualquer IA

### 1. Agentes baseados em Terminal / CLI (Claude Code, Aider, OpenHands, Terminal)
Execute diretamente pelo terminal usando a CLI:
```bash
python cli.py -i amostra.csv -o dados_anonimizados.csv -m sintetico -r relatorio.md
```

### 2. Agentes de IA em Python (LangChain, CrewAI, AutoGen, LlamaIndex)
Importe os módulos diretamente em seus workflows de agentes:
```python
import pandas as pd
from deteccao import escanear_banco
from classificacao import classificar_dados
from anonimo import substituir_por_sintetico

df = pd.read_csv("dados.csv")
colunas_risco = escanear_banco(df)
df_anonimo = substituir_por_sintetico(df, {col: col for col in colunas_risco})
```

### 3. ChatGPT Custom GPTs / Assistants API / Ollama
Importe as rotinas contidas em `tools.json` na aba **Actions** ou **Tools** da sua IA para que ela possa chamar o código automaticamente.

---

## 🧪 Rodando os Testes Unitários

Para garantir que tudo está funcionando perfeitamente:
```bash
python -m unittest test_gardia.py
```
