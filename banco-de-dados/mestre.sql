-- =========================================
-- SCRIPT MESTRE
-- Executa todos os scripts do banco na ordem correta.
--
-- Uso (precisa do psql, devido aos comandos \ir):
--   psql -U guardia -d guardia -f banco-de-dados/mestre.sql
--
-- No Docker ele roda sozinho na primeira inicialização: é o único .sql
-- na raiz desta pasta; as subpastas são ignoradas pelo entrypoint.
--
-- \ir resolve o caminho relativo à pasta deste arquivo, então o
-- comando funciona a partir de qualquer diretório.
-- =========================================

\set ON_ERROR_STOP ON

-- Tudo numa única transação: se qualquer script falhar,
-- nada fica criado pela metade.
BEGIN;

-- -----------------------------------------
-- 1. TABELAS
-- A ordem respeita as foreign keys: uma tabela só é criada
-- depois das tabelas que ela referencia.
-- -----------------------------------------
\echo '>> Criando tabelas'
\ir tabelas/filiais.sql
\ir tabelas/clientes.sql
\ir tabelas/funcionarios.sql
\ir tabelas/categorias.sql
\ir tabelas/produtos.sql
\ir tabelas/atendimentos.sql

-- -----------------------------------------
-- 2. FUNÇÕES
-- Usadas pelo script de dados para gerar valores fictícios.
-- -----------------------------------------
\echo '>> Criando funções'
\ir funcoes/gerar_nome_aleatorio.sql
\ir funcoes/gerar_cpf.sql
\ir funcoes/gerar_rg.sql
\ir funcoes/gerar_email.sql
\ir funcoes/sortear_localidade.sql
\ir funcoes/gerar_telefone.sql

-- -----------------------------------------
-- 3. DADOS DE TESTE
-- A ordem respeita as foreign keys: os dados de uma tabela só são
-- inseridos depois dos dados das tabelas que ela referencia.
-- -----------------------------------------
\echo '>> Inserindo dados de teste'
\ir dados/filiais.sql
\ir dados/clientes.sql
\ir dados/funcionarios.sql
\ir dados/categorias.sql
\ir dados/produtos.sql
\ir dados/atendimentos.sql

COMMIT;

-- -----------------------------------------
-- 4. CONSULTAS DE VALIDAÇÃO (somente leitura)
-- -----------------------------------------
\echo '>> Executando consultas de teste'
\ir consultas/queries_teste.sql

\echo '>> Banco criado com sucesso'
