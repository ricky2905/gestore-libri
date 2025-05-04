import sqlite3

conn = sqlite3.connect('libri.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE collezioni (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
''')

c.execute('''
    CREATE TABLE libri (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titolo TEXT NOT NULL,
        autore TEXT,
        anno INTEGER,
        collezione_id INTEGER,
        comprato INTEGER DEFAULT 0,
        FOREIGN KEY(collezione_id) REFERENCES collezioni(id)
    )
''')

conn.commit()
conn.close()
