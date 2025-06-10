CREATE DATABASE IF NOT EXISTS agrineural;

USE agrineural;

CREATE TABLE usuarios (
    cpf VARCHAR(20) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    tipo ENUM('produtor', 'operador', 'mosaiqueiro') NOT NULL,
    cpf_produtor VARCHAR(20),

    -- Restrição: Se não for produtor, cpf_produtor deve existir e ser de um produtor
    CONSTRAINT fk_cpf_produtor FOREIGN KEY (cpf_produtor) REFERENCES usuarios(cpf) ON DELETE CASCADE,

    -- Restrição de lógica de negócio
    CONSTRAINT chk_cpf_produtor
    CHECK (
        (tipo = 'produtor' AND cpf_produtor IS NULL) OR
        (tipo IN ('operador', 'mosaiqueiro') AND cpf_produtor IS NOT NULL)
    )
);

CREATE TABLE imagens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cpf_produtor VARCHAR(20) NOT NULL,
    nome VARCHAR(255) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    FOREIGN KEY (cpf_produtor) REFERENCES usuarios(cpf) ON DELETE CASCADE
);


CREATE TABLE resultados (
    id INT PRIMARY KEY,
    anomala BOOLEAN NOT NULL,
    FOREIGN KEY (id) REFERENCES imagens(id) ON DELETE CASCADE
);

// nao executei ainda
CREATE TABLE localizacao (
    cpf_produtor VARCHAR(20) PRIMARY KEY,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    ext_territorial FLOAT NOT NULL,
    FOREIGN KEY (cpf_produtor) REFERENCES usuarios(cpf)
);
