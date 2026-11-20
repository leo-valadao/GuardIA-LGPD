-- =========================================
-- TESTE 1
-- Detectar CPFs na tabela clientes
-- =========================================
SELECT *
  FROM clientes
 WHERE cpf ~ '^[0-9]{11}$';

-- =========================================
-- TESTE 2
-- Detectar e-mails em texto livre
-- =========================================
SELECT *
  FROM atendimentos
 WHERE descricao ~* '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}';

-- =========================================
-- TESTE 3
-- Detectar CPF em texto livre
-- =========================================
SELECT *
  FROM atendimentos
 WHERE descricao ~ '[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}';

-- =========================================
-- TESTE 4
-- Detectar telefone em texto livre
-- =========================================
SELECT *
  FROM atendimentos
 WHERE descricao ~ '\(?[0-9]{2}\)? ?9?[0-9]{4}-?[0-9]{4}';

-- =========================================
-- TESTE 5
-- Mostrar possíveis falsos positivos
-- Marcas que parecem nomes de pessoas
-- =========================================
SELECT id_produto,
       nome,
       marca
  FROM produtos;

-- =========================================
-- TESTE 6
-- Mostrar razão social das filiais
-- Pode parecer nome de pessoa
-- =========================================
SELECT id_filial,
       razao_social,
       cnpj
  FROM filiais;

-- =========================================
-- TESTE 7
-- Quantidade de registros por tabela
-- =========================================
SELECT 'clientes' AS tabela,
       COUNT(*)
  FROM clientes

 UNION ALL

SELECT 'funcionarios',
       COUNT(*)
  FROM funcionarios

 UNION ALL

SELECT 'produtos',
       COUNT(*)
  FROM produtos

 UNION ALL

SELECT 'atendimentos',
       COUNT(*)
  FROM atendimentos

 UNION ALL

SELECT 'filiais',
       COUNT(*)
  FROM filiais

 UNION ALL

SELECT 'categorias',
       COUNT(*)
  FROM categorias;

-- =========================================
-- TESTE 8
-- Verificar relacionamentos
-- Atendimento + Cliente + Funcionário
-- =========================================
SELECT atendimentos.id_atendimento,
       clientes.nome_completo     AS nome_do_cliente,
       funcionarios.nome_completo AS nome_do_funcionario,
       atendimentos.canal,
       atendimentos.status
  FROM atendimentos
  JOIN clientes ON atendimentos.id_cliente = clientes.id_cliente
  JOIN funcionarios ON atendimentos.id_funcionario = funcionarios.id_funcionario
 LIMIT 20;

-- =========================================
-- TESTE 9
-- Verificar relacionamentos
-- Produto + Categoria
-- =========================================
SELECT produtos.id_produto,
       produtos.nome,
       produtos.marca,
       categorias.nome AS categoria
  FROM produtos
  JOIN categorias ON produtos.id_categoria = categorias.id_categoria
 LIMIT 20;

-- =========================================
-- TESTE 10
-- Verificar relacionamentos
-- Funcionário + Filial
-- =========================================
SELECT funcionarios.id_funcionario,
       funcionarios.nome_completo,
       funcionarios.cargo,
       filiais.razao_social AS filial
  FROM funcionarios
  JOIN filiais ON funcionarios.id_filial = filiais.id_filial
 LIMIT 20;

-- =========================================
-- TESTE 11
-- Verificar o plano de cargos
-- Senioridade, faixa salarial e filiação por cargo
-- =========================================
  SELECT cargo,
         senioridade,
         COUNT(*)                 AS funcionarios,
         MIN(salario)             AS menor_salario,
         MAX(salario)             AS maior_salario,
         COUNT(filiacao_sindical) AS filiados
    FROM funcionarios
GROUP BY cargo,
         senioridade
ORDER BY cargo,
         MIN(salario);
