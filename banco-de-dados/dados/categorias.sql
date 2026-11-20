-- =========================================
-- DADOS: categorias (10 registros)
-- Depende de: (nenhuma)
--
-- Os ids 1..10 são usados por produtos.id_categoria
-- =========================================
INSERT INTO categorias (
    nome,
    descricao
)
VALUES ('Vestuário',   'Roupas masculinas e femininas'),
       ('Calçados',    'Tênis, sapatos e sandálias'),
       ('Eletrônicos', 'Aparelhos eletrônicos em geral'),
       ('Smartphones', 'Celulares e smartphones'),
       ('Informática', 'Computadores, notebooks e periféricos'),
       ('Acessórios',  'Bolsas, cintos e carteiras'),
       ('Perfumaria',  'Perfumes e cosméticos'),
       ('Esportes',    'Artigos esportivos'),
       ('Relógios',    'Relógios e smartwatches'),
       ('Áudio',       'Fones de ouvido e caixas de som');
