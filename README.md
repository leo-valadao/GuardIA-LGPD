# GuardIA-LGPD 🛡️

Skill modular e biblioteca Python para análise, auditoria (precisão/revocação), classificação e anonimização de dados pessoais de acordo com a LGPD (Lei Geral de Proteção de Dados).

Funciona direto em um **banco de dados PostgreSQL**: o GuardIA lê o banco em modo somente leitura, detecta os dados pessoais e gera uma **cópia do banco** com esses dados **censurados** ou **substituídos por dados sintéticos**.

Projetada para ser **100% compatível com qualquer IA ou agente de desenvolvimento** (ChatGPT/Custom GPTs, Claude Code, LangChain, AutoGen, CrewAI, Ollama, Aider, Cursor, etc.).

---

## 📁 Estrutura do Repositório

Dentro de `guardia/`, cada pasta tem **um arquivo por função pública**, com o mesmo nome da função
(ex.: `deteccao/classificar_coluna.py` → `def classificar_coluna`). O `__init__.py` de cada pasta
tem o mapa dos seus arquivos.

```
GuardIA-LGPD/
├── main.py                  modo interativo
├── cli.py                   linha de comando (CLI)
├── SKILL.md                 instruções da Skill para agentes de IA
├── tools.json               ferramentas (function calling) que a IA pode chamar
├── requirements.txt         dependências (faker, SQLAlchemy, pg8000)
│
├── guardia/                 código do GuardIA, na ordem das etapas do artigo
│   ├── deteccao/            1. encontra os dados pessoais: regra D = F ∨ (W ∧ C)
│   ├── classificacao/       2. classifica o risco e calcula o score (equação 8)
│   ├── anonimizacao/        3. censura ou troca por dados sintéticos (dicionário bijetor)
│   ├── avaliacao/           4. precisão e revocação da detecção
│   ├── relatorio/           5. relatórios em Markdown, sem valores reais
│   ├── ferramentas/         funções descritas no tools.json
│   ├── terminal/            texto certo em qualquer terminal e mensagens de erro sem traceback
│   ├── banco/               tudo que conversa com o PostgreSQL
│   │   ├── conexao/         acesso, senha oculta, origem somente leitura, criação da cópia
│   │   └── copia/           análise do banco e cópia anonimizada com a mesma estrutura
│   ├── utilitarios/         funções de apoio usadas por mais de uma função
│   ├── excecoes/            os erros do GuardIA, um arquivo para cada (ex.: banco_ja_existe.py)
│   ├── modelos/             as classes que só guardam dados (dataclasses), um arquivo para cada
│   └── enumeracoes/         as listas fechadas de opções (enums), um arquivo para cada
│
├── testes/                  testes unitários (unittest)
├── banco-de-dados/          banco de testes com dados fictícios (mestre.sql cria tudo)
└── docker/                  docker-compose.yml com o PostgreSQL de testes
```

---

## ⚙️ Instalação

Requer **Python 3.11 ou mais novo** (os enums usam `StrEnum`).

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt
```

Banco de testes (dados fictícios), na pasta `docker/`:
```bash
docker compose up -d            # banco "guardia", usuário "guardia", senha "guardia"
```

---

## 🗄️ Banco de Dados

O GuardIA **nunca altera o banco original**: a conexão de origem é somente leitura. A cópia é criada como um banco **novo no mesmo servidor** (padrão: `<banco>_anonimizado`), com as mesmas tabelas, sequences, PK, FK, UNIQUE, CHECK e índices, e os dados pessoais trocados. O usuário do banco precisa da permissão `CREATEDB`.

```bash
# só o relatório de riscos
python cli.py --host localhost --banco guardia --usuario guardia -m apenas_relatorio

# cópia com dados sintéticos coerentes (CPF válido, e-mail feito do nome, DDD/CEP da mesma cidade)
python cli.py --host localhost --banco guardia --usuario guardia -m sintetico

# cópia censurada (valores viram ****; datas ficam só com o ano)
python cli.py --url postgresql://guardia@localhost:5432/guardia -m mascarar --destino guardia_censurado
```

* **Senha:** nunca vai na linha de comando. Ela é pedida sem aparecer na tela, ou lida da variável de ambiente `PGPASSWORD`.
* **Banco de destino já existe:** o GuardIA para. Use `--destino` com outro nome ou `--sobrescrever` (pede confirmação).
* **`--semente N`:** gera sempre os mesmos dados sintéticos (resultados reprodutíveis).
* O relatório (`-r`, padrão `relatorio_lgpd.md`) traz tabelas, colunas, tipos, score de risco e avisos de possíveis dados sensíveis, **sem nenhum valor real**.

Modo interativo: `python main.py` (pergunta os dados de acesso ao banco e o que fazer).

---

## 🚀 Como Usar em Qualquer IA

### 1. Agentes baseados em Terminal / CLI (Claude Code, Aider, OpenHands, Terminal)
Execute diretamente pelo terminal usando a CLI, com os comandos da seção **Banco de Dados** acima.

### 2. Agentes de IA em Python (LangChain, CrewAI, AutoGen, LlamaIndex)
Importe as funções do GuardIA diretamente em seus workflows de agentes
(a senha vem da variável de ambiente `PGPASSWORD`):
```python
from guardia.ferramentas.analisar_banco_dados import analisar_banco_dados
from guardia.ferramentas.gerar_copia_anonimizada import gerar_copia_anonimizada

relatorio = analisar_banco_dados('localhost', 'guardia', 'guardia')
relatorio_da_copia = gerar_copia_anonimizada('localhost', 'guardia', 'guardia', modo='sintetico')
```

### 3. ChatGPT Custom GPTs / Assistants API / Ollama
Importe as rotinas contidas em `tools.json` na aba **Actions** ou **Tools** da sua IA para que ela possa chamar o código automaticamente. As tools nunca recebem a senha do banco: configure `PGPASSWORD` antes de iniciar o agente.

---

## 🧪 Rodando os Testes Unitários

Para garantir que tudo está funcionando perfeitamente:
```bash
python -m unittest discover testes
```
