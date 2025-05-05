import psycopg2
import os
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.environ.get("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
c = conn.cursor()

# Creazione tabella collezioni
c.execute('''
    CREATE TABLE IF NOT EXISTS collezioni (
        id SERIAL PRIMARY KEY,
        nome TEXT NOT NULL
    )
''')

# Creazione tabella libri
c.execute('''
    CREATE TABLE IF NOT EXISTS libri (
        id SERIAL PRIMARY KEY,
        titolo TEXT NOT NULL,
        autore TEXT,
        anno INTEGER,
        collezione_id INTEGER REFERENCES collezioni(id),
        comprato INTEGER DEFAULT 0
    )
''')

conn.commit()
conn.close()
