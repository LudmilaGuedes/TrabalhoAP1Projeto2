-- Criação do banco de dados com charset UTF-8
CREATE DATABASE IF NOT EXISTS db_escola 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

USE db_escola;

-- Tabela de tb_enderecos
CREATE TABLE tb_enderecos (
    cep VARCHAR(10) PRIMARY KEY,
    endereco VARCHAR(255) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    estado VARCHAR(2) NOT NULL
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Tabela de tb_carros
CREATE TABLE tb_carros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fabricante VARCHAR(100) NOT NULL,
    modelo VARCHAR(100) NOT NULL,
    especificacao VARCHAR(255)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Tabela de tb_alunos
CREATE TABLE tb_alunos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_aluno VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    cep VARCHAR(10),
    carro_id INT,
    FOREIGN KEY (cep) REFERENCES tb_enderecos(cep),
    FOREIGN KEY (carro_id) REFERENCES tb_carros(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Tabela de tb_disciplinas
CREATE TABLE tb_disciplinas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_disciplina VARCHAR(255) NOT NULL,
    carga INT NOT NULL,
    semestre INT NOT NULL
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Tabela de tb_notas
CREATE TABLE tb_notas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    aluno_id INT NOT NULL,
    disciplina_id INT NOT NULL,
    nota DECIMAL(5, 2),
    FOREIGN KEY (aluno_id) REFERENCES tb_alunos(id),
    FOREIGN KEY (disciplina_id) REFERENCES tb_disciplinas(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;