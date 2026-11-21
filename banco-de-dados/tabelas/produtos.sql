-- =========================================
-- TABELA: produtos
-- Depende de: categorias
-- =========================================
-- SEQUENCE
CREATE SEQUENCE sq_produtos_id_produto
             AS INTEGER
     START WITH 1
   INCREMENT BY 1
       MINVALUE 1
       MAXVALUE 2147483647
          CACHE 1
       NO CYCLE;

-- TABELA
CREATE TABLE produtos (
    id_produto            INTEGER        NOT NULL DEFAULT NEXTVAL('sq_produtos_id_produto'::REGCLASS),
    nome                  VARCHAR(150),
    marca                 VARCHAR(100),
    codigo_de_barras      VARCHAR(20),
    preco                 NUMERIC(10,2),
    quantidade_em_estoque INTEGER,
    id_categoria          INTEGER,
    data_de_fabricacao    DATE
);

-- VÍNCULO SEQUENCE → COLUNA
ALTER SEQUENCE sq_produtos_id_produto
      OWNED BY produtos.id_produto;

-- PRIMARY KEY
   ALTER TABLE produtos
ADD CONSTRAINT pk_produtos
   PRIMARY KEY (id_produto);

-- FOREIGN KEYS
   ALTER TABLE produtos
ADD CONSTRAINT fk_produtos_categorias
   FOREIGN KEY (id_categoria)
    REFERENCES categorias (id_categoria)
     ON UPDATE NO ACTION
     ON DELETE NO ACTION;

-- ÍNDICES DAS FOREIGN KEYS
CREATE INDEX ix_produtos_id_categoria
          ON produtos (id_categoria);
