/* Exclui o banco de dados "empresa", caso o banco de dados exista */
DROP DATABASE IF EXISTS empresa;

/* Cria o banco de dados "empresa" */
CREATE DATABASE empresa;

/* Define o banco de dados "empresa" como o banco de dados atual */
USE empresa;

/* Cria a tabela "fornecedores" */
CREATE TABLE fornecedores (
    id_fornecedor INT PRIMARY KEY,
    nome_fornecedor VARCHAR(50),
    cidade VARCHAR(50),
    uf CHAR(2)
);

/* Cria a tabela "unidades" */
CREATE TABLE unidades (
    id_unidade INT PRIMARY KEY,
    nome_unidade VARCHAR(50)
);

/* Cria a tabela "materiais" */
CREATE TABLE materiais (
    id_material INT PRIMARY KEY,
    id_fornecedor INT,
    nome_material VARCHAR(100),
    quantidade_estoque INT,
    quantidade_estoque_minima INT,
    id_unidade INT,
    FOREIGN KEY (id_fornecedor) REFERENCES fornecedores(id_fornecedor),
    FOREIGN KEY (id_unidade) REFERENCES unidades(id_unidade)
);

/* Cria a tabela "pedidos" */
CREATE TABLE pedidos (
    id_pedido INT PRIMARY KEY,
    data_pedido DATE
);

/* Cria a tabela "itens_pedido" */
CREATE TABLE itens_pedido (
    id_item_pedido INT PRIMARY KEY,
    id_pedido INT,
    id_material INT,
    quantidade_pedida INT,
    valor_unitario DECIMAL(10, 2),
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido),
    FOREIGN KEY (id_material) REFERENCES materiais(id_material)
);

/* Insere registros na tabela "Fornecedores" */
insert into fornecedores
(id_fornecedor, nome_fornecedor, cidade, uf)
values
('1', 'ABC Materiais Elétricos', 'Curitiba', 'PR'),
('2', 'XYZ Materiais de Escritório', 'Rio de Janeiro', 'RJ'),
('3', 'Hidra Materiais Hidraulicos', 'São Paulo', 'SP'),
('4', 'HidraX Materiais Elétricos e Hidraulicos', 'Porto Alegre', 'RS');

/* Mostra os registros da tabela "Fornecedores" */
select * from fornecedores;

/* Insere registros na tabela "Unidades" */
insert into unidades
(id_unidade, nome_unidade)
values
('1', 'Unidades'),
('2', 'Kg'),
('3', 'Litros'),
('4', 'Caixa com 12 unidades'),
('5', 'Caixa com 100 unidades'),
('6', 'Metros');

/* Mostra os registros da tabela "Unidades" */
select * from unidades;

/* Insere registros na tabela "Materiais" */
insert into materiais
(id_material , id_fornecedor, nome_material, quantidade_estoque, quantidade_estoque_minima, id_unidade)
values
('1', '1', 'Tomada elétrica 10A padrão novo', '12', '5', '1'),
('2', '1', 'Disjuntor elétrico 25A', '10', '5', '1'),
('3', '2', 'Resma papel branco A4', '32', '20', '4'),
('4', '2', 'Toner impressora HR5522', '6', '10', '1'),
('5', '3', 'Cano PVC 1/2 pol', '6', '10', '6'),
('6', '3', 'Cano PVC 3/4 pol', '8', '10', '6'),
('7', '3', 'Medidor hidráulico 1/2 pol', '3', '2', '1'),
('8', '3', 'Conector Joelho 1/2 pol', '18', '15', '1'),
('9', '1', 'Tomada elétrica 20A padrão novo', '8', '5', '1'),
('10', '2', 'Caneta esferográfica azul', '80', '120', '1'),
('11', '2', 'Grampeador mesa pequeno', '5', '5', '1'),
('12', '2', 'Caneta Marca Texto Amarela', '6', '15', '5'),
('13', '2', 'Lápis Preto HB', '15', '25', '1');

/* Mostra os registros da tabela "Materiais" */
select * from materiais;

/* Insere registros na tabela "Pedidos" */
insert into pedidos
(id_pedido, data_pedido)
values
('1', '2015-02-25'),
('2', '2014-02-10'),
('3', '2015-03-01');

/* Mostra os registros da tabela "Pedidos" */
select * from pedidos;

/* Insere registros na tabela "Itens pedido" */
insert into itens_pedido
(id_item_pedido, id_pedido, id_material, quantidade_pedida, valor_unitario)
values
('1', '1', '10', '100', '0.50'),
('2', '1', '13', '100', '0.25'),
('3', '2', '8', '50', '1.30'),
('4', '3', '11', '5', '76.00');

/* Mostra os registros da tabela "Itens pedidos" */
select * from itens_pedido;

/* 1 - Nome do material e nome da unidade */
SELECT m.nome_material, u.nome_unidade
FROM materiais m
JOIN unidades u ON m.id_unidade = u.id_unidade;

/* 2 - Nome do material e nome da unidade dos materiais vendidos em unidades */
SELECT m.nome_material, u.nome_unidade
FROM materiais m
JOIN unidades u ON m.id_unidade = u.id_unidade
WHERE u.nome_unidade = 'Unidades';

/* 3 - Quantidade de materiais por nome de unidade */
SELECT u.nome_unidade, COUNT(m.id_material) AS quantidade_materiais
FROM unidades u
LEFT JOIN materiais m ON u.id_unidade = m.id_unidade
GROUP BY u.nome_unidade;

/* 4 - Quantidade de materiais por nome de unidade, incluindo as unidade sem nenhum material relacionado */
SELECT u.nome_unidade, COUNT(m.id_material) AS quantidade_materiais
FROM unidades u
LEFT JOIN materiais m ON u.id_unidade = m.id_unidade
GROUP BY u.nome_unidade;

/* 5 - Nome do material, nome do fornecedor e nome da unidade */
SELECT m.nome_material, f.nome_fornecedor, u.nome_unidade
FROM materiais m
JOIN fornecedores f ON m.id_fornecedor = f.id_fornecedor
JOIN unidades u ON m.id_unidade = u.id_unidade;

/* 6 - Nome do material e nome da unidade dos materiais vendidos por metro */
SELECT m.nome_material, u.nome_unidade
FROM materiais m
JOIN unidades u ON m.id_unidade = u.id_unidade
WHERE u.nome_unidade = 'Metros';

/* 7 - Nome do material e nome da unidade dos materiais vendidos em caixas com 12 ou com 100 unidades */
SELECT m.nome_material, u.nome_unidade
FROM materiais m
JOIN unidades u ON m.id_unidade = u.id_unidade
WHERE u.nome_unidade IN ('Caixa com 12 unidades', 'Caixa com 100 unidades');

/* 8 - Nome do material e sua quantidade em estoque */
SELECT nome_material, quantidade_estoque
FROM materiais;

/* 9 - Nome do material e sua quantidade em estoque, apenas para materiais com menos de 10 unidades em estoque */
SELECT nome_material, quantidade_estoque
FROM materiais
WHERE quantidade_estoque < 10;

/* 10 - Nome do material, sua quantidade em estoque e sua quantidade mínima em estoque */
SELECT nome_material, quantidade_estoque, quantidade_estoque_minima
FROM materiais;

/* 11 - Nome do material, sua quantidade em estoque e sua quantidade mínima em estoque,
apenas para materiais onde a quantidade em estoque esteja abaixo da quantidade mínima em estoque */
SELECT nome_material, quantidade_estoque, quantidade_estoque_minima
FROM materiais
WHERE quantidade_estoque < quantidade_estoque_minima;

/* 12 - Nome e cidade dos fornecedores */
SELECT nome_fornecedor, cidade
FROM fornecedores;

/* 13 - Nome e cidade dos fornecedores da cidade de Curitiba */
SELECT nome_fornecedor, cidade
FROM fornecedores
WHERE cidade = 'Curitiba';

/* 14 - Nome dos fornecedores e seus materiais */
SELECT f.nome_fornecedor, m.nome_material
FROM fornecedores f
JOIN materiais m ON f.id_fornecedor = m.id_fornecedor;

/* 15 - Nome dos fornecedores e seus materiais, incluindo os fornecedores sem nenhum material relacionado */
SELECT f.nome_fornecedor, m.nome_material
FROM fornecedores f
LEFT JOIN materiais m ON f.id_fornecedor = m.id_fornecedor;

/* 16 - Nome dos fornecedores e quantidade de materiais fornecidos pelo mesmo */
SELECT f.nome_fornecedor, COUNT(m.id_material) AS quantidade_materiais
FROM fornecedores f
LEFT JOIN materiais m ON f.id_fornecedor = m.id_fornecedor
GROUP BY f.nome_fornecedor;

/* 17 - Nome dos fornecedores e quantidade de materiais fornecidos pelo mesmo,
incluindo os fornecedores sem nenhum material relacionado */
SELECT f.nome_fornecedor, COUNT(m.id_material) AS quantidade_materiais
FROM fornecedores f
LEFT JOIN materiais m ON f.id_fornecedor = m.id_fornecedor
GROUP BY f.nome_fornecedor;

/* 18 - Nome dos fornecedores e quantidade de materiais fornecidos pelo mesmo,
incluindo os fornecedores sem nenhum material relacionado,
apenas para fornecedores com menos de 5 materiais relacionados */
SELECT f.nome_fornecedor, COUNT(m.id_material) AS quantidade_materiais
FROM fornecedores f
LEFT JOIN materiais m ON f.id_fornecedor = m.id_fornecedor
GROUP BY f.nome_fornecedor
HAVING COUNT(m.id_material) < 5;

/* 19 - Nome dos fornecedores, nome do material e sua quantidade em estoque */
SELECT f.nome_fornecedor, m.nome_material, m.quantidade_estoque
FROM fornecedores f
JOIN materiais m ON f.id_fornecedor = m.id_fornecedor;

/* 20 - Nome dos fornecedores, nome do material e sua quantidade em estoque,
apenas para quantidade em estoque entre 10 e 20 */
SELECT f.nome_fornecedor, m.nome_material, m.quantidade_estoque
FROM fornecedores f
JOIN materiais m ON f.id_fornecedor = m.id_fornecedor
WHERE m.quantidade_estoque BETWEEN 10 AND 20;

/* 21 - Nome do fornecedor, nome do material e nome da unidade,
apenas para fornecedores de materiais em unidades ou metros */
SELECT f.nome_fornecedor, m.nome_material, u.nome_unidade
FROM fornecedores f
JOIN materiais m ON f.id_fornecedor = m.id_fornecedor
JOIN unidades u ON m.id_unidade = u.id_unidade
WHERE u.nome_unidade IN ('Unidades', 'Metros');

/* 22 - Pedidos realizados em 2015 */
SELECT *
FROM pedidos
WHERE YEAR(data_pedido) = 2015;

/* 23 - Pedidos realizados em fevereiro de 2015 */
SELECT *
FROM pedidos
WHERE data_pedido BETWEEN '2015-02-01' AND '2015-02-28';

/* 24 - Número do pedido e o nome dos materiais constantes no pedido */
SELECT p.id_pedido, m.nome_material
FROM pedidos p
JOIN itens_pedido i ON p.id_pedido = i.id_pedido
JOIN materiais m ON i.id_material = m.id_material;

/* 25 - Materiais que constam nos pedidos */
SELECT DISTINCT m.nome_material
FROM materiais m
JOIN itens_pedido i ON m.id_material = i.id_material;

/* 26 - Materiais que não constam nos pedidos */
SELECT m.nome_material
FROM materiais m
LEFT JOIN itens_pedido i ON m.id_material = i.id_material
WHERE i.id_material IS NULL;

/* 27 - Número do pedido e a quantidade de itens em cada pedido */
SELECT p.id_pedido, COUNT(i.id_item_pedido) AS quantidade_itens
FROM pedidos p
JOIN itens_pedido i ON p.id_pedido = i.id_pedido
GROUP BY p.id_pedido;

/* 28 - Número do pedido e o valor total do pedido */
SELECT p.id_pedido, SUM(i.quantidade_pedida * i.valor_unitario) AS valor_total
FROM pedidos p
JOIN itens_pedido i ON p.id_pedido = i.id_pedido
GROUP BY p.id_pedido;

/* 29 - Número do pedido e o valor total do pedido, apenas para pedidos com valor total abaixo de 100,00 */
SELECT p.id_pedido, SUM(i.quantidade_pedida * i.valor_unitario) AS valor_total
FROM pedidos p
JOIN itens_pedido i ON p.id_pedido = i.id_pedido
GROUP BY p.id_pedido
HAVING valor_total < 100.00;

/* 34 - Número do pedido e o valor total do pedido inserido no item 32 */
SELECT p.id_pedido, SUM(i.quantidade_pedida * i.valor_unitario) AS valor_total
FROM pedidos p
JOIN itens_pedido i ON p.id_pedido = i.id_pedido
WHERE p.id_pedido = 4
GROUP BY p.id_pedido;

/* 35 - Exclua o material "Tomada elétrica 10A padrão novo" do banco de dados */
DELETE FROM materiais WHERE nome_material = 'Tomada elétrica 10A padrão novo' LIMIT 1;

SELECT * FROM materiais;

/* 36 - Exclua o material "Lápis Preto HB" do banco de dados */
DELETE FROM itens_pedido WHERE id_material = (SELECT id_material FROM materiais WHERE nome_material = 'Lápis Preto HB' LIMIT 1);

DELETE FROM materiais WHERE nome_material = 'Lápis Preto HB' LIMIT 1;

SELECT * FROM itens_pedido;
SELECT * FROM materiais;

/* 37 - Exclua o fornecedor "HidraX Materiais Elétricos e Hidraulicos" do banco de dados */
DELETE FROM materiais WHERE id_fornecedor = (SELECT id_fornecedor FROM fornecedores WHERE nome_fornecedor = 'HidraX Materiais Elétricos e Hidraulicos' limit 1);
DELETE FROM fornecedores WHERE nome_fornecedor = 'HidraX Materiais Elétricos e Hidraulicos' LIMIT 1;

SELECT * FROM fornecedores;

/* 38 - Exclua o fornecedor "XYZ Materiais de Escritório" do banco de dados */
DELETE FROM materiais WHERE id_fornecedor = (SELECT id_fornecedor FROM fornecedores WHERE nome_fornecedor = 'XYZ Materiais de Escritório' limit 1);
DELETE FROM fornecedores WHERE nome_fornecedor = 'XYZ Materiais de Escritório' LIMIT 1;

SELECT * FROM fornecedores;

