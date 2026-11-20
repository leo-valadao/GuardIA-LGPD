-- =========================================
-- DADOS: clientes (100 registros)
-- Depende de: fn_gerar_nome_aleatorio, fn_sortear_localidade,
--             fn_gerar_cpf, fn_gerar_email, fn_gerar_telefone
--
-- O nome e a localidade são sorteados uma única vez por cliente
-- (MATERIALIZED) e reaproveitados: o e-mail é feito a partir do nome,
-- e o telefone e o CEP seguem o DDD e a faixa de CEP da cidade.
-- =========================================
WITH pessoas AS MATERIALIZED (
    SELECT numero,
           fn_gerar_nome_aleatorio() AS nome_completo,
           fn_sortear_localidade()   AS localidade
      FROM GENERATE_SERIES(1, 100) numero
)
INSERT INTO clientes (
    nome_completo,
    cpf,
    data_de_nascimento,
    email,
    telefone,
    endereco,
    cidade,
    sigla_do_estado,
    cep,
    pontos_de_fidelidade
)
SELECT pessoas.nome_completo,
       fn_gerar_cpf(),
       DATE '1980-01-01' + ((pessoas.numero * 37) % 12000),
       fn_gerar_email(pessoas.nome_completo),
       fn_gerar_telefone((pessoas.localidade).ddd),

       (ARRAY['Rua', 'Avenida', 'Alameda', 'Travessa'])[1 + FLOOR(RANDOM() * 4)::INTEGER]
       || ' '  || (1 + FLOOR(RANDOM() * 300)::INTEGER)
       || ', ' || (1 + FLOOR(RANDOM() * 2000)::INTEGER),

       (pessoas.localidade).cidade,
       (pessoas.localidade).sigla_do_estado,
       (pessoas.localidade).cep,
       (pessoas.numero * 15) % 5000
  FROM pessoas;
