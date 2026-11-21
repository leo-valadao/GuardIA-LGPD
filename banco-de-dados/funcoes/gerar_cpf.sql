-- =========================================
-- FUNÇÃO: fn_gerar_cpf
-- Depende de: (nenhuma)
--
-- Retorna um CPF fictício VÁLIDO, só com os 11 dígitos (ex.: 52998224725).
--
-- Os 9 primeiros dígitos são sorteados e os 2 dígitos verificadores são
-- calculados pelo módulo 11, as mesmas equações (5), (6) e (7) do artigo:
--   S1  = soma de d(i) * (11 - i), com i = 1..9
--   DV1 = 0 se (S1 mod 11) < 2; senão 11 - (S1 mod 11)
--   S2  = soma de d(i) * (12 - i), com i = 1..9, + 2 * DV1
--   DV2 = mesma regra do DV1, aplicada a S2
--
-- Sequências de dígitos repetidos (111.111.111-11) passam no cálculo,
-- mas não são CPFs válidos; por isso são sorteadas de novo.
--
-- Atenção: um CPF sintético válido pode coincidir com o de uma pessoa
-- real (risco residual citado no artigo, conforme Åbrandt, 2026).
-- =========================================
CREATE FUNCTION fn_gerar_cpf()
        RETURNS VARCHAR
       LANGUAGE PLPGSQL
       VOLATILE
AS $$
DECLARE
    v_digitos              INTEGER[];
    v_soma                 INTEGER;
    v_resto                INTEGER;
    v_digito_verificador_1 INTEGER;
    v_digito_verificador_2 INTEGER;
BEGIN
    -- 9 dígitos aleatórios, sorteados de novo se forem todos iguais
    LOOP
        v_digitos := ARRAY(SELECT FLOOR(RANDOM() * 10)::INTEGER
                             FROM GENERATE_SERIES(1, 9));

        EXIT WHEN (SELECT COUNT(DISTINCT digito)
                     FROM UNNEST(v_digitos) digito) > 1;
    END LOOP;

    -- 1.º dígito verificador: equações (5) e (6)
    v_soma := 0;

    FOR posicao IN 1..9 LOOP
        v_soma := v_soma + v_digitos[posicao] * (11 - posicao);
    END LOOP;

    v_resto                := v_soma % 11;
    v_digito_verificador_1 := CASE WHEN v_resto < 2 THEN 0
                                   ELSE 11 - v_resto
                              END;

    -- 2.º dígito verificador: equação (7)
    v_soma := 2 * v_digito_verificador_1;

    FOR posicao IN 1..9 LOOP
        v_soma := v_soma + v_digitos[posicao] * (12 - posicao);
    END LOOP;

    v_resto                := v_soma % 11;
    v_digito_verificador_2 := CASE WHEN v_resto < 2 THEN 0
                                   ELSE 11 - v_resto
                              END;

    RETURN ARRAY_TO_STRING(v_digitos, '') || v_digito_verificador_1 || v_digito_verificador_2;
END;
$$;
