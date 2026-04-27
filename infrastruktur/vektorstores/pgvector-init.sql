-- pgvector Init
-- Ausführen nach erstem Postgres-Start:
--   psql -h localhost -U postgres -f pgvector-init.sql

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS dokumente (
    id BIGSERIAL PRIMARY KEY,
    titel TEXT,
    quelle TEXT,
    lizenz TEXT,
    text TEXT,
    embedding vector(1024),  -- für e5-large-instruct, bge-m3
    erstellt_am TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS dokumente_embedding_hnsw_cosine
    ON dokumente USING hnsw (embedding vector_cosine_ops);

CREATE INDEX IF NOT EXISTS dokumente_quelle_idx ON dokumente (quelle);

-- Beispiel-Insert (nach Embedding-Berechnung):
-- INSERT INTO dokumente (titel, quelle, lizenz, text, embedding)
-- VALUES ('DSGVO', 'Wikipedia DE', 'CC BY-SA 4.0', 'Die DSGVO ...', ARRAY[0.1, 0.2, ...]::vector);

-- Beispiel-Query:
-- SELECT id, titel, quelle, 1 - (embedding <=> $1) AS similarity
-- FROM dokumente
-- ORDER BY embedding <=> $1
-- LIMIT 5;
