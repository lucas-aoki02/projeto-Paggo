CREATE DATABASE IF NOT EXISTS alvo_dados;

-- Cria a tabela para dados de sinais processados
CREATE TABLE IF NOT EXISTS signal_ (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    data JSONB,
    timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    signal_id INTEGER NOT NULL,
    value REAL
);