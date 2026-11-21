-- =========================================
-- FUNÇÃO: fn_gerar_nome_aleatorio
-- Depende de: (nenhuma)
--
-- Retorna um nome completo fictício, sempre com as 3 partes:
--   Nome + nome do meio + sobrenome   (ex.: Ana Clara Ribeiro)
--
-- As partes são sorteadas de forma independente a cada chamada:
--   100 nomes         (50 femininos + 50 masculinos)
--   100 nomes do meio (50 femininos + 50 masculinos)
--   100 sobrenomes
-- O nome e o nome do meio são sempre do mesmo gênero, para não gerar
-- combinações como "Maria Henrique". Nenhum nome se repete entre as
-- listas, então nunca sai "Ana Ana" ou "Silva Silva".
--
-- Total de combinações: 2 x 50 x 50 x 100 = 500.000 nomes diferentes.
--
-- VOLATILE: o PostgreSQL executa a função de novo em cada linha,
-- então cada registro de um INSERT ... SELECT recebe um nome diferente.
-- =========================================
CREATE FUNCTION fn_gerar_nome_aleatorio()
        RETURNS VARCHAR
       LANGUAGE PLPGSQL
       VOLATILE
AS $$
DECLARE
    v_nomes_femininos          TEXT[] := ARRAY[
        'Ana',       'Maria',     'Juliana',   'Fernanda',  'Patrícia',  'Aline',     'Camila',    'Bruna',     'Amanda',    'Jéssica',
        'Letícia',   'Larissa',   'Beatriz',   'Gabriela',  'Mariana',   'Rafaela',   'Carolina',  'Isabela',   'Vanessa',   'Débora',
        'Tatiane',   'Priscila',  'Renata',    'Sabrina',   'Simone',    'Cláudia',   'Adriana',   'Luciana',   'Márcia',    'Sandra',
        'Daniela',   'Natália',   'Bianca',    'Raquel',    'Viviane',   'Elaine',    'Michele',   'Thaís',     'Yasmin',    'Lorena',
        'Heloísa',   'Alice',     'Sophia',    'Valentina', 'Giovana',   'Manuela',   'Lívia',     'Cecília',   'Melissa',   'Rebeca'
    ];

    v_nomes_masculinos         TEXT[] := ARRAY[
        'João',      'Pedro',     'Lucas',     'Gabriel',   'Mateus',    'Rafael',    'Gustavo',   'Felipe',    'Bruno',     'Rodrigo',
        'Thiago',    'Diego',     'André',     'Marcelo',   'Leonardo',  'Ricardo',   'Eduardo',   'Fernando',  'Daniel',    'Vinícius',
        'Leandro',   'Fábio',     'Marcos',    'Paulo',     'Carlos',    'José',      'Antônio',   'Francisco', 'Luiz',      'Sérgio',
        'Roberto',   'Márcio',    'Alexandre', 'Renato',    'Igor',      'Caio',      'Arthur',    'Bernardo',  'Heitor',    'Davi',
        'Samuel',    'Enzo',      'Murilo',    'Otávio',    'Nicolas',   'Guilherme', 'Vítor',     'Wesley',    'Douglas',   'Diogo'
    ];

    v_nomes_do_meio_femininos  TEXT[] := ARRAY[
        'Eduarda',    'Clara',      'Luiza',      'Vitória',    'Cristina',   'Helena',     'Júlia',      'Paula',      'Carla',      'Regina',
        'Teresa',     'Lúcia',      'Aparecida',  'Rosa',       'Estela',     'Fátima',     'Rita',       'Isabel',     'Laura',      'Elisa',
        'Gisele',     'Sílvia',     'Mônica',     'Rosana',     'Lara',       'Luana',      'Flávia',     'Fabiana',    'Karina',     'Cristiane',
        'Eliane',     'Rosângela',  'Vera',       'Lilian',     'Antônia',    'Francisca',  'Joana',      'Marta',      'Alessandra', 'Bárbara',
        'Caroline',   'Emanuele',   'Valéria',    'Ingrid',     'Kelly',      'Lorraine',   'Nicole',     'Olívia',     'Pietra',     'Stefany'
    ];

    v_nomes_do_meio_masculinos TEXT[] := ARRAY[
        'Henrique',  'Miguel',    'Augusto',   'César',     'Emanuel',   'Raimundo',  'Benedito',  'Sebastião', 'Manoel',    'Joaquim',
        'Alberto',   'Alfredo',   'Aurélio',   'Batista',   'Cristiano', 'Damião',    'Domingos',  'Elias',     'Emílio',    'Ernesto',
        'Estevão',   'Fabrício',  'Fausto',    'Flávio',    'Frederico', 'Geraldo',   'Gilberto',  'Hugo',      'Inácio',    'Jorge',
        'Júlio',     'Lauro',     'Lorenzo',   'Mauro',     'Moisés',    'Natan',     'Nelson',    'Orlando',   'Osvaldo',   'Rogério',
        'Rui',       'Sílvio',    'Tadeu',     'Teodoro',   'Valter',    'Vicente',   'Wagner',    'Wilson',    'Yuri',      'Zacarias'
    ];

    v_sobrenomes               TEXT[] := ARRAY[
        'Silva',       'Santos',      'Oliveira',    'Souza',       'Rodrigues',   'Ferreira',    'Alves',       'Pereira',     'Lima',        'Gomes',
        'Costa',       'Ribeiro',     'Martins',     'Carvalho',    'Almeida',     'Lopes',       'Soares',      'Fernandes',   'Vieira',      'Barbosa',
        'Rocha',       'Dias',        'Nascimento',  'Andrade',     'Moreira',     'Nunes',       'Marques',     'Machado',     'Mendes',      'Freitas',
        'Cardoso',     'Ramos',       'Gonçalves',   'Santana',     'Teixeira',    'Araújo',      'Pinto',       'Correia',     'Moraes',      'Campos',
        'Monteiro',    'Cavalcanti',  'Borges',      'Duarte',      'Farias',      'Fonseca',     'Guimarães',   'Macedo',      'Medeiros',    'Miranda',
        'Nogueira',    'Pacheco',     'Pires',       'Queiroz',     'Reis',        'Rezende',     'Sales',       'Siqueira',    'Tavares',     'Vasconcelos',
        'Barros',      'Brito',       'Cunha',       'Coelho',      'Castro',      'Aguiar',      'Amaral',      'Antunes',     'Azevedo',     'Bezerra',
        'Brandão',     'Bueno',       'Caldeira',    'Camargo',     'Cordeiro',    'Coutinho',    'Cruz',        'Esteves',     'Figueiredo',  'Franco',
        'Galvão',      'Garcia',      'Leite',       'Magalhães',   'Melo',        'Neves',       'Paiva',       'Peixoto',     'Prado',       'Rangel',
        'Sampaio',     'Serra',       'Toledo',      'Valente',     'Vidal',       'Moura',       'Porto',       'Rios',        'Matos',       'Bastos'
    ];

    v_nome         VARCHAR(50);
    v_nome_do_meio VARCHAR(50);
    v_sobrenome    VARCHAR(50);
BEGIN
    -- Sorteia o gênero; nome e nome do meio seguem o mesmo gênero
    IF RANDOM() < 0.5
        THEN v_nome         := v_nomes_femininos[1 + FLOOR(RANDOM() * CARDINALITY(v_nomes_femininos))::INTEGER];
             v_nome_do_meio := v_nomes_do_meio_femininos[1 + FLOOR(RANDOM() * CARDINALITY(v_nomes_do_meio_femininos))::INTEGER];

        ELSE v_nome         := v_nomes_masculinos[1 + FLOOR(RANDOM() * CARDINALITY(v_nomes_masculinos))::INTEGER];
             v_nome_do_meio := v_nomes_do_meio_masculinos[1 + FLOOR(RANDOM() * CARDINALITY(v_nomes_do_meio_masculinos))::INTEGER];
    END IF;

    v_sobrenome := v_sobrenomes[1 + FLOOR(RANDOM() * CARDINALITY(v_sobrenomes))::INTEGER];

    RETURN v_nome || ' ' || v_nome_do_meio || ' ' || v_sobrenome;
END;
$$;
