-- =========================================
-- TIPO:   tp_localidade
-- FUNÇÃO: fn_sortear_localidade
-- Depende de: (nenhuma)
--
-- Sorteia uma cidade e retorna, de uma só vez, a cidade, a UF, o DDD
-- e um CEP aleatório dentro da faixa de CEP dessa cidade. Como tudo
-- sai do mesmo sorteio, os 4 valores são sempre compatíveis entre si.
--
-- O CEP não tem dígito verificador: ele é válido quando tem 8 dígitos
-- e está dentro da faixa que os Correios reservam para a cidade.
-- Faixas e DDDs: https://www.ruacep.com.br/ddd/uf/capitais/
--
-- O retorno é um tipo composto (tp_localidade) para ser chamado uma
-- única vez por registro; ex.: (localidade).cidade, (localidade).ddd
-- =========================================
-- TIPO
CREATE TYPE tp_localidade AS (
    cidade          VARCHAR(100),
    sigla_do_estado CHAR(2),
    ddd             CHAR(2),
    cep             CHAR(8)
);

-- FUNÇÃO
CREATE FUNCTION fn_sortear_localidade()
        RETURNS tp_localidade
       LANGUAGE SQL
       VOLATILE
AS $$
      SELECT cidades.cidade,
             cidades.sigla_do_estado,
             cidades.ddd,
             LPAD((cidades.cep_inicial::INTEGER + FLOOR(RANDOM() * (cidades.cep_final::INTEGER - cidades.cep_inicial::INTEGER + 1))::INTEGER)::TEXT, 8, '0')
        FROM (VALUES ('Goiânia',        'GO', '62', '74000001', '74899999'),
                     ('Brasília',       'DF', '61', '70000001', '72799999'),
                     ('São Paulo',      'SP', '11', '01000001', '05999999'),
                     ('Rio de Janeiro', 'RJ', '21', '20000001', '23799999'),
                     ('Belo Horizonte', 'MG', '31', '30000001', '31999999'),
                     ('Curitiba',       'PR', '41', '80000001', '82999999'),
                     ('Porto Alegre',   'RS', '51', '90000001', '91999999'),
                     ('Salvador',       'BA', '71', '40000001', '42599999'),
                     ('Fortaleza',      'CE', '85', '60000001', '61599999'),
                     ('Manaus',         'AM', '92', '69000001', '69099999'))
             AS cidades (cidade, sigla_do_estado, ddd, cep_inicial, cep_final)
    ORDER BY RANDOM()
       LIMIT 1;
$$;
