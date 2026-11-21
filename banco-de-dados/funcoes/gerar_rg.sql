-- =========================================
-- FUNÇÃO: fn_gerar_rg
-- Depende de: (nenhuma)
--
-- Retorna um RG fictício no formato do RG de São Paulo: 99.999.999-D
--
-- O RG não tem uma regra nacional: cada estado tem o seu formato.
-- O padrão de SP é o mais usado e tem dígito verificador (módulo 11):
--   S  = d1·2 + d2·3 + d3·4 + d4·5 + d5·6 + d6·7 + d7·8 + d8·9
--   DV = 11 - (S mod 11);  DV = 10 → 'X';  DV = 11 → '0'
-- Ex.: 24.678.131-2 → S = 163, 163 mod 11 = 9, DV = 11 - 9 = 2
-- =========================================
CREATE FUNCTION fn_gerar_rg()
        RETURNS VARCHAR
       LANGUAGE PLPGSQL
       VOLATILE
AS $$
DECLARE
    v_digitos            INTEGER[];
    v_soma               INTEGER;
    v_digito_verificador INTEGER;
    v_numero             VARCHAR(8);
BEGIN
    -- 8 dígitos aleatórios do número de registro
    v_digitos := ARRAY(SELECT FLOOR(RANDOM() * 10)::INTEGER
                         FROM GENERATE_SERIES(1, 8));

    -- Dígito verificador: pesos de 2 a 9, da esquerda para a direita
    v_soma := 0;

    FOR posicao IN 1..8 LOOP
        v_soma := v_soma + v_digitos[posicao] * (posicao + 1);
    END LOOP;

    v_digito_verificador := 11 - (v_soma % 11);
    v_numero             := ARRAY_TO_STRING(v_digitos, '');

    RETURN SUBSTR(v_numero, 1, 2) || '.' || SUBSTR(v_numero, 3, 3) || '.' || SUBSTR(v_numero, 6, 3) || '-' ||
           CASE WHEN v_digito_verificador = 10 THEN 'X'
                WHEN v_digito_verificador = 11 THEN '0'
                ELSE v_digito_verificador::TEXT
           END;
END;
$$;
