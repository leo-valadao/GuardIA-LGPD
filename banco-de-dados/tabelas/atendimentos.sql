-- =========================================
-- TABELA: atendimentos
-- Depende de: clientes, funcionarios
-- =========================================
-- SEQUENCE
CREATE SEQUENCE sq_atendimentos_id_atendimento
             AS INTEGER
     START WITH 1
   INCREMENT BY 1
       MINVALUE 1
       MAXVALUE 2147483647
          CACHE 1
       NO CYCLE;

-- TABELA
CREATE TABLE atendimentos (
    id_atendimento INTEGER      NOT NULL DEFAULT NEXTVAL('sq_atendimentos_id_atendimento'::REGCLASS),
    id_cliente     INTEGER,
    id_funcionario INTEGER,
    data_e_hora    TIMESTAMP,
    canal          VARCHAR(30),
    descricao      TEXT,
    ip_de_origem   VARCHAR(45),
    status         VARCHAR(30)
);

-- VÍNCULO SEQUENCE → COLUNA
ALTER SEQUENCE sq_atendimentos_id_atendimento
      OWNED BY atendimentos.id_atendimento;

-- PRIMARY KEY
   ALTER TABLE atendimentos
ADD CONSTRAINT pk_atendimentos
   PRIMARY KEY (id_atendimento);

-- FOREIGN KEYS
   ALTER TABLE atendimentos
ADD CONSTRAINT fk_atendimentos_clientes
   FOREIGN KEY (id_cliente)
    REFERENCES clientes (id_cliente)
     ON UPDATE NO ACTION
     ON DELETE NO ACTION;

   ALTER TABLE atendimentos
ADD CONSTRAINT fk_atendimentos_funcionarios
   FOREIGN KEY (id_funcionario)
    REFERENCES funcionarios (id_funcionario)
     ON UPDATE NO ACTION
     ON DELETE NO ACTION;

-- ÍNDICES DAS FOREIGN KEYS
CREATE INDEX ix_atendimentos_id_cliente
          ON atendimentos (id_cliente);

CREATE INDEX ix_atendimentos_id_funcionario
          ON atendimentos (id_funcionario);
