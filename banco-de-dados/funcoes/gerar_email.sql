-- =========================================
-- FUNÇÃO: fn_gerar_email
-- Depende de: (nenhuma)
--
-- Recebe o nome completo da pessoa e retorna um e-mail fictício feito
-- a partir do nome, em um formato sorteado entre 7 possíveis.
-- Exemplo para "Ana Clara Ribeiro":
--   ana.ribeiro         ana_ribeiro         anaribeiro
--   ana.clara.ribeiro   aribeiro            anacribeiro
--   ribeiro.ana
-- Metade dos e-mails ganha um número no final (ex.: ana.ribeiro87) e o
-- domínio também é sorteado (gmail.com, hotmail.com, ...).
--
-- Acentos e cedilha são removidos e tudo fica em minúsculas, como em
-- um e-mail de verdade ("João Araújo" → joao.araujo).
-- =========================================
CREATE FUNCTION fn_gerar_email(p_nome_completo VARCHAR)
        RETURNS VARCHAR
       LANGUAGE PLPGSQL
       VOLATILE
AS $$
DECLARE
    v_dominios TEXT[] := ARRAY[
        'gmail.com',  'hotmail.com', 'outlook.com',  'yahoo.com.br', 'icloud.com',
        'uol.com.br', 'bol.com.br',  'terra.com.br', 'live.com',     'globo.com'
    ];

    v_partes       TEXT[];
    v_nome         TEXT;
    v_nome_do_meio TEXT;
    v_sobrenome    TEXT;
    v_formato      INTEGER;
    v_usuario      TEXT;
BEGIN
    -- Separa o nome em partes, em minúsculas e sem acentos
    v_partes := STRING_TO_ARRAY(LOWER(TRANSLATE(p_nome_completo, 'ÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇáàâãäéèêëíìîïóòôõöúùûüç', 'AAAAAEEEEIIIIOOOOOUUUUCaaaaaeeeeiiiiooooouuuuc')), ' ');
    v_nome         := v_partes[1];
    v_nome_do_meio := v_partes[2];
    v_sobrenome    := v_partes[CARDINALITY(v_partes)];

    -- Sorteia um dos 7 formatos do usuário (parte antes do @)
    v_formato := FLOOR(RANDOM() * 7)::INTEGER;
    v_usuario := CASE v_formato WHEN 0 THEN v_nome || '.' || v_sobrenome
                                WHEN 1 THEN v_nome || '_' || v_sobrenome
                                WHEN 2 THEN v_nome || v_sobrenome
                                WHEN 3 THEN v_nome || '.' || v_nome_do_meio || '.' || v_sobrenome
                                WHEN 4 THEN LEFT(v_nome, 1) || v_sobrenome
                                WHEN 5 THEN v_nome || LEFT(v_nome_do_meio, 1) || v_sobrenome
                                ELSE v_sobrenome || '.' || v_nome
                 END;

    -- Metade dos e-mails ganha um número de 0 a 99 no final
    IF RANDOM() < 0.5
        THEN v_usuario := v_usuario || FLOOR(RANDOM() * 100)::INTEGER;
    END IF;

    RETURN v_usuario || '@' || v_dominios[1 + FLOOR(RANDOM() * CARDINALITY(v_dominios))::INTEGER];
END;
$$;
