-- =========================================
-- TABELA: categorias
-- Depende de: (nenhuma)
-- =========================================
-- SEQUENCE
CREATE SEQUENCE sq_categorias_id_categoria
             AS INTEGER
     START WITH 1
   INCREMENT BY 1
       MINVALUE 1
       MAXVALUE 2147483647
          CACHE 1
       NO CYCLE;

-- TABELA
CREATE TABLE categorias (
    id_categoria INTEGER      NOT NULL DEFAULT NEXTVAL('sq_categorias_id_categoria'::REGCLASS),
    nome         VARCHAR(100) NOT NULL,
    descricao    VARCHAR(200)
);

-- VÍNCULO SEQUENCE → COLUNA
ALTER SEQUENCE sq_categorias_id_categoria
      OWNED BY categorias.id_categoria;

-- PRIMARY KEY
   ALTER TABLE categorias
ADD CONSTRAINT pk_categorias
   PRIMARY KEY (id_categoria);

-- UNIQUE
   ALTER TABLE categorias
ADD CONSTRAINT uq_categorias_nome
        UNIQUE (nome);

-- FOREIGN KEYS
-- (Nenhuma)
