-- =========================================
-- DADOS: filiais (3 registros)
-- Depende de: (nenhuma)
-- =========================================
INSERT INTO filiais (
    razao_social,
    cnpj,
    endereco,
    cidade,
    sigla_do_estado,
    cep,
    telefone_comercial,
    email_de_contato,
    horario_de_funcionamento
)
VALUES ('Loja Centro LTDA',    '12.345.678/0001-99', 'Rua A, 100',         'Goiânia',  'GO', '74000-000', '6230000000', 'contato@lojacentro.com.br',    '08:00-18:00'),
       ('João Silva ME',       '98.765.432/0001-88', 'Rua B, 50',          'Anápolis', 'GO', '75000-000', '6231111111', 'contato@joaosilvame.com.br',   '08:00-17:00'),
       ('Ecommerce Brasil SA', '44.555.666/0001-77', 'Av. Principal, 999', 'Brasília', 'DF', '70000-000', '6132222222', 'atendimento@ecommerce.com.br', '24h');
