-- =========================================
-- TABELA: clientes
-- Depende de: (nenhuma)
-- =========================================
-- SEQUENCE
CREATE SEQUENCE sq_clientes_id_cliente
             AS INTEGER
     START WITH 1
   INCREMENT BY 1
       MINVALUE 1
       MAXVALUE 2147483647
          CACHE 1
       NO CYCLE;

-- TABELA
CREATE TABLE clientes (
    id_cliente           INTEGER       NOT NULL DEFAULT NEXTVAL('sq_clientes_id_cliente'::REGCLASS),
    nome_completo        VARCHAR(150)  NOT NULL,
    cpf                  VARCHAR(14)   NOT NULL,
    data_de_nascimento   DATE,
    email                VARCHAR(150),
    telefone             VARCHAR(20),
    endereco             VARCHAR(200),
    cidade               VARCHAR(100),
    sigla_do_estado      CHAR(2),
    cep                  VARCHAR(10),
    data_de_cadastro     TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
    pontos_de_fidelidade INTEGER       DEFAULT 0
);

-- VÍNCULO SEQUENCE → COLUNA
ALTER SEQUENCE sq_clientes_id_cliente
      OWNED BY clientes.id_cliente;

-- PRIMARY KEY
   ALTER TABLE clientes
ADD CONSTRAINT pk_clientes
   PRIMARY KEY (id_cliente);

-- FOREIGN KEYS
-- (Nenhuma)
