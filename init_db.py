import sqlite3

conn = sqlite3.connect('libri.db')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS collezioni (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS libri (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titolo TEXT NOT NULL,
    autore TEXT NOT NULL,
    collezione_id INTEGER NOT NULL,
    FOREIGN KEY (collezione_id) REFERENCES collezioni(id)
)
''')

conn.commit()
conn.close()
