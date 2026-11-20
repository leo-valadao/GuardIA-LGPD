-- =========================================
-- DADOS: produtos (100 registros)
-- Depende de: categorias
-- =========================================
INSERT INTO produtos (
    nome,
    marca,
    codigo_de_barras,
    preco,
    quantidade_em_estoque,
    id_categoria,
    data_de_fabricacao
)
SELECT 'Produto ' || numero,

       CASE numero % 5 WHEN 0 THEN 'Tommy Hilfiger'
                       WHEN 1 THEN 'Hugo Boss'
                       WHEN 2 THEN 'Nike'
                       WHEN 3 THEN 'Samsung'
                       ELSE 'Apple'
       END,

       LPAD((789000000000 + numero)::TEXT, 13, '0'),
       ROUND((RANDOM() * 1000)::NUMERIC, 2),
       (numero * 3) % 500,
       (numero % 10) + 1,
       CURRENT_DATE - (numero * 5)
  FROM GENERATE_SERIES(1, 100) numero;
