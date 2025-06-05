CREATE DATABASE IF NOT EXISTS agrineural;

USE agrineural;

CREATE TABLE IF NOT EXISTS usuarios (
    cpf VARCHAR(11) PRIMARY KEY,
    senha VARCHAR(255) NOT NULL,
    nome VARCHAR(100) NOT NULL,
    tipo ENUM('produtor', 'operador', 'mosaiqueiro') NOT NULL
);
