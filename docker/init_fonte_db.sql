CREATE DATABASE IF NOT EXISTS fonte_dados;

-- Cria a tabela para dados de energia eólicos
CREATE TABLE IF NOT EXISTS data (
    timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    wind_speed REAL,
    power REAL,
    ambient_temperature REAL,
    PRIMARY KEY (timestamp)
);