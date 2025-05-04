import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Tabella collezioni
cursor.execute('''
    CREATE TABLE IF NOT EXISTS collezioni (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
''')

# Tabella libri
cursor.execute('''
    CREATE TABLE IF NOT EXISTS libri (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titolo TEXT NOT NULL,
        autore TEXT,
        anno INTEGER,
        collezione_id INTEGER,
        FOREIGN KEY(collezione_id) REFERENCES collezioni(id) ON DELETE CASCADE
    )
''')

conn.commit()
conn.close()

print("Database inizializzato correttamente.")
