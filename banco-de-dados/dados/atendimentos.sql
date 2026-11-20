-- =========================================
-- DADOS: atendimentos (100 registros)
-- Depende de: clientes, funcionarios
--
-- Os JOINs com clientes e funcionarios garantem que todo dado citado
-- na descrição (nome, CPF, telefone, e-mail) é do mesmo cliente gravado
-- em id_cliente, e que id_funcionario aponta para um funcionário real.
-- CPF e telefone aparecem formatados, como alguém digitaria no texto.
-- =========================================
INSERT INTO atendimentos (
    id_cliente,
    id_funcionario,
    data_e_hora,
    canal,
    descricao,
    ip_de_origem,
    status
)
SELECT clientes.id_cliente,
       funcionarios.id_funcionario,
       CURRENT_TIMESTAMP - (numero || ' hours')::INTERVAL,

       CASE WHEN numero % 3 = 0 THEN 'chat'
            WHEN numero % 3 = 1 THEN 'telefone'
            ELSE 'email'
       END,

       CASE WHEN numero % 4 = 0 THEN 'Cliente ' || clientes.nome_completo || ', CPF ' || REGEXP_REPLACE(clientes.cpf, '(\d{3})(\d{3})(\d{3})(\d{2})', '\1.\2.\3-\4') || ', solicitou troca do produto.'
            WHEN numero % 4 = 1 THEN 'Solicitação de cancelamento de pedido.'
            WHEN numero % 4 = 2 THEN 'Contato realizado por ' || clientes.nome_completo || ' telefone ' || REGEXP_REPLACE(clientes.telefone, '(\d{2})(\d{5})(\d{4})', '(\1) \2-\3') || '.'
            ELSE 'Cliente informou e-mail ' || clientes.email || '.'
       END,

       '192.168.1.' || (numero % 255),

       CASE WHEN numero % 3 = 0 THEN 'ABERTO'
            WHEN numero % 3 = 1 THEN 'EM_ANALISE'
            ELSE 'FINALIZADO'
       END

  FROM GENERATE_SERIES(1, 100) numero
  JOIN clientes ON clientes.id_cliente = ((numero - 1) % 100) + 1
  JOIN funcionarios ON funcionarios.id_funcionario = ((numero - 1) % 100) + 1;
