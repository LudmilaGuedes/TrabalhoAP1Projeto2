CREATE DATABASE IF NOT EXISTS db_imoveis;
USE db_imoveis;

CREATE TABLE tb_imoveis (
    titulo INT,
    preco INT,
    metragem INT,
    quarto INT,
    descricao TEXT
);

SELECT * FROM tb_imoveis;
