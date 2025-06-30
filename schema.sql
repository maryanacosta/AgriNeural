CREATE DATABASE IF NOT EXISTS agrineural;

USE agrineural;

-- 1) Tabela de usuários (sem mudanças)
CREATE TABLE usuarios (
    cpf VARCHAR(20) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    tipo ENUM('produtor', 'operador', 'mosaiqueiro') NOT NULL
);

-- 2) Tabela de fazendas, com id auto‑increment e CCIR exposto
CREATE TABLE fazendas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cpf_produtor VARCHAR(20) NOT NULL,
    ccir VARCHAR(50) NOT NULL UNIQUE,
    nome VARCHAR(100) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    ext_territorial FLOAT NOT NULL,
    FOREIGN KEY (cpf_produtor) REFERENCES usuarios(cpf) ON DELETE CASCADE
);

-- 3) Associação muitos-para-muitos entre usuários (operador/mosaiqueiro) e fazendas
CREATE TABLE usuarios_fazendas (
    cpf_usuario VARCHAR(20) NOT NULL,
    fazenda_id INT       NOT NULL,
    PRIMARY KEY (cpf_usuario, fazenda_id),
    FOREIGN KEY (cpf_usuario)   REFERENCES usuarios(cpf)   ON DELETE CASCADE,
    FOREIGN KEY (fazenda_id)    REFERENCES fazendas(id)    ON DELETE CASCADE
);

-- 4) Imagens vinculadas a fazendas
CREATE TABLE imagens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fazenda_id INT       NOT NULL,
    nome VARCHAR(255)    NOT NULL,
    latitude FLOAT       NOT NULL,
    longitude FLOAT      NOT NULL,
    FOREIGN KEY (fazenda_id) REFERENCES fazendas(id) ON DELETE CASCADE
);

-- 5) Resultados das detecções
CREATE TABLE resultados (
    id INT PRIMARY KEY,     -- corresponde a imagens.id
    anomala BOOLEAN NOT NULL,
    FOREIGN KEY (id) REFERENCES imagens(id) ON DELETE CASCADE
);
