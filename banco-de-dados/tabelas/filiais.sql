-- =========================================
-- TABELA: filiais
-- Depende de: (nenhuma)
-- =========================================
-- SEQUENCE
CREATE SEQUENCE sq_filiais_id_filial
             AS INTEGER
     START WITH 1
   INCREMENT BY 1
       MINVALUE 1
       MAXVALUE 2147483647
          CACHE 1
       NO CYCLE;

-- TABELA
CREATE TABLE filiais (
    id_filial                INTEGER       NOT NULL DEFAULT NEXTVAL('sq_filiais_id_filial'::REGCLASS),
    razao_social             VARCHAR(200),
    cnpj                     VARCHAR(18),
    endereco                 VARCHAR(200),
    cidade                   VARCHAR(100),
    sigla_do_estado          CHAR(2),
    cep                      VARCHAR(10),
    telefone_comercial       VARCHAR(20),
    email_de_contato         VARCHAR(150),
    horario_de_funcionamento VARCHAR(100)
);

-- VÍNCULO SEQUENCE -> COLUNA
ALTER SEQUENCE sq_filiais_id_filial
      OWNED BY filiais.id_filial;

-- PRIMARY KEY
   ALTER TABLE filiais
ADD CONSTRAINT pk_filiais
   PRIMARY KEY (id_filial);

-- FOREIGN KEYS
-- (nenhuma)
