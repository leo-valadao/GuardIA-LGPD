-- =========================================
-- TABELA: funcionarios
-- Depende de: filiais
-- =========================================
-- SEQUENCE
CREATE SEQUENCE sq_funcionarios_id_funcionario
             AS INTEGER
     START WITH 1
   INCREMENT BY 1
       MINVALUE 1
       MAXVALUE 2147483647
          CACHE 1
       NO CYCLE;

-- TABELA
CREATE TABLE funcionarios (
    id_funcionario    INTEGER        NOT NULL DEFAULT NEXTVAL('sq_funcionarios_id_funcionario'::REGCLASS),
    nome_completo     VARCHAR(150),
    rg                VARCHAR(20),
    pis               VARCHAR(20),
    cpf               VARCHAR(14),
    salario           NUMERIC(10,2),
    conta_bancaria    VARCHAR(50),
    tipo_sanguineo    VARCHAR(5),
    filiacao_sindical VARCHAR(100),
    cargo             VARCHAR(100),
    senioridade       VARCHAR(20),
    data_de_admissao  DATE,
    id_filial         INTEGER
);

-- VÍNCULO SEQUENCE -> COLUNA
ALTER SEQUENCE sq_funcionarios_id_funcionario
      OWNED BY funcionarios.id_funcionario;

-- PRIMARY KEY
   ALTER TABLE funcionarios
ADD CONSTRAINT pk_funcionarios
   PRIMARY KEY (id_funcionario);

-- FOREIGN KEYS
   ALTER TABLE funcionarios
ADD CONSTRAINT fk_funcionarios_filiais
   FOREIGN KEY (id_filial)
    REFERENCES filiais (id_filial)
     ON UPDATE NO ACTION
     ON DELETE NO ACTION;

-- ÍNDICES DAS FOREIGN KEYS
CREATE INDEX ix_funcionarios_id_filial
          ON funcionarios (id_filial);
