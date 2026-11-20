-- =========================================
-- DADOS: funcionarios (100 registros)
-- Depende de: filiais, fn_gerar_nome_aleatorio, fn_gerar_rg, fn_gerar_cpf
--
-- Plano de cargos: cada cargo tem as suas senioridades, a faixa salarial
-- de cada senioridade e o sindicato da categoria.
--   - A senioridade é sorteada entre as do cargo; os valores repetidos no
--     ARRAY dão o peso (ex.: 2 Júnior, 2 Pleno, 1 Sênior = 40%, 40%, 20%).
--   - O salário é sorteado dentro da faixa do cargo + senioridade.
--   - A filiação ao sindicato segue a chance de filiação do cargo;
--     gerente é cargo de gestão, sem filiação.
-- Quadro: 45 vendedores, 20 caixas, 15 estoquistas, 14 analistas e
-- 6 gerentes (2 por filial).
-- =========================================

WITH cargos (cargo, senioridades, sindicato, chance_de_filiacao) AS (
    VALUES ('Vendedor',   ARRAY['Júnior', 'Júnior', 'Pleno', 'Pleno', 'Sênior'], 'Sindicato dos Empregados no Comércio',                  0.40),
           ('Caixa',      ARRAY['Júnior', 'Júnior', 'Pleno', 'Pleno', 'Sênior'], 'Sindicato dos Empregados no Comércio',                  0.45),
           ('Estoquista', ARRAY['Júnior', 'Júnior', 'Pleno', 'Pleno', 'Sênior'], 'Sindicato dos Empregados no Comércio',                  0.50),
           ('Analista',   ARRAY['Júnior', 'Pleno', 'Pleno', 'Sênior'],           'Sindicato dos Trabalhadores em Processamento de Dados', 0.25),
           ('Gerente',    ARRAY['Pleno', 'Sênior'],                              NULL,                                                    0.00)
),
faixas_salariais (cargo, senioridade, salario_minimo, salario_maximo) AS (
    VALUES ('Vendedor',   'Júnior', 1900.00, 2400.00),
           ('Vendedor',   'Pleno',  2400.00, 3100.00),
           ('Vendedor',   'Sênior', 3100.00, 4000.00),
           ('Caixa',      'Júnior', 1700.00, 2000.00),
           ('Caixa',      'Pleno',  2000.00, 2400.00),
           ('Caixa',      'Sênior', 2400.00, 2900.00),
           ('Estoquista', 'Júnior', 1700.00, 2100.00),
           ('Estoquista', 'Pleno',  2100.00, 2600.00),
           ('Estoquista', 'Sênior', 2600.00, 3200.00),
           ('Analista',   'Júnior', 3500.00, 5000.00),
           ('Analista',   'Pleno',  5000.00, 7500.00),
           ('Analista',   'Sênior', 7500.00, 11000.00),
           ('Gerente',    'Pleno',  7000.00, 9500.00),
           ('Gerente',    'Sênior', 9500.00, 14000.00)
),
sorteados AS MATERIALIZED (
    SELECT numero,
           cargos.cargo,
           cargos.senioridades[1 + FLOOR(RANDOM() * CARDINALITY(cargos.senioridades))::INTEGER] AS senioridade,

           CASE WHEN RANDOM() < cargos.chance_de_filiacao THEN cargos.sindicato
           END AS filiacao_sindical

      FROM GENERATE_SERIES(1, 100) numero
      JOIN cargos ON cargos.cargo = CASE WHEN numero <= 45 THEN 'Vendedor'
                                         WHEN numero <= 65 THEN 'Caixa'
                                         WHEN numero <= 80 THEN 'Estoquista'
                                         WHEN numero <= 94 THEN 'Analista'
                                         ELSE 'Gerente'
                                    END
)
INSERT INTO funcionarios (
    nome_completo,
    rg,
    pis,
    cpf,
    salario,
    conta_bancaria,
    tipo_sanguineo,
    filiacao_sindical,
    cargo,
    senioridade,
    data_de_admissao,
    id_filial
)
  SELECT fn_gerar_nome_aleatorio(),
         fn_gerar_rg(),
         'PIS' || sorteados.numero,
         fn_gerar_cpf(),
         ROUND((faixas_salariais.salario_minimo + RANDOM() * (faixas_salariais.salario_maximo - faixas_salariais.salario_minimo))::NUMERIC, 2),
         '00012345' || sorteados.numero,

         CASE sorteados.numero % 8 WHEN 0 THEN 'A+'
                                   WHEN 1 THEN 'A-'
                                   WHEN 2 THEN 'B+'
                                   WHEN 3 THEN 'B-'
                                   WHEN 4 THEN 'AB+'
                                   WHEN 5 THEN 'AB-'
                                   WHEN 6 THEN 'O+'
                                   ELSE 'O-'
         END,

         sorteados.filiacao_sindical,
         sorteados.cargo,
         sorteados.senioridade,
         CURRENT_DATE - (sorteados.numero * 10),
         ((sorteados.numero - 1) % 3) + 1
    FROM sorteados
    JOIN faixas_salariais ON faixas_salariais.cargo       = sorteados.cargo
                       AND faixas_salariais.senioridade = sorteados.senioridade
ORDER BY sorteados.numero;
