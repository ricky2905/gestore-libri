import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Crea la tabella collezioni
c.execute('''
    CREATE TABLE IF NOT EXISTS collezioni (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
''')

# Crea la tabella libri
c.execute('''
    CREATE TABLE IF NOT EXISTS libri (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        collezione_id INTEGER NOT NULL,
        nome TEXT NOT NULL,
        FOREIGN KEY (collezione_id) REFERENCES collezioni(id) ON DELETE CASCADE
    )
''')

conn.commit()
conn.close()
print("Database inizializzato correttamente.")

