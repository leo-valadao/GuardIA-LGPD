-- =========================================
-- FUNÇÃO: fn_gerar_telefone
-- Depende de: (nenhuma)
--
-- Recebe o DDD e retorna um celular fictício com 11 dígitos:
--   DDD (2) + 9 + 8 dígitos, o primeiro deles entre 6 e 9
--   ex.: fn_gerar_telefone('62') -> 62981234567
--
-- Use com o DDD vindo da fn_sortear_localidade() para o telefone
-- ser compatível com a cidade.
-- =========================================
CREATE FUNCTION fn_gerar_telefone(p_ddd CHAR(2))
        RETURNS VARCHAR
       LANGUAGE SQL
       VOLATILE
AS $$
    SELECT p_ddd || '9' || (6 + FLOOR(RANDOM() * 4)::INTEGER) || LPAD(FLOOR(RANDOM() * 10000000)::INTEGER::TEXT, 7, '0');
$$;
