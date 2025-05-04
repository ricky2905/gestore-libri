from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DB_PATH = 'libri.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS collezioni (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS libri (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titolo TEXT NOT NULL,
            collezione_id INTEGER,
            FOREIGN KEY(collezione_id) REFERENCES collezioni(id)
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, nome FROM collezioni')
    collezioni = c.fetchall()

    collezione_libri = []
    for collezione_id, nome in collezioni:
        c.execute('SELECT id, titolo FROM libri WHERE collezione_id = ?', (collezione_id,))
        libri = c.fetchall()
        collezione_libri.append({
            'id': collezione_id,
            'nome': nome,
            'libri': libri
        })

    conn.close()
    return render_template('index.html', collezione_libri=collezione_libri)

@app.route('/aggiungi_collezione', methods=['POST'])
def aggiungi_collezione():
    nome = request.form['nome']
    if nome:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO collezioni (nome) VALUES (?)', (nome,))
        conn.commit()
        conn.close()
    return redirect('/')

@app.route('/aggiungi_libro/<int:collezione_id>', methods=['POST'])
def aggiungi_libro(collezione_id):
    titolo = request.form['titolo']
    if titolo:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO libri (titolo, collezione_id) VALUES (?, ?)', (titolo, collezione_id))
        conn.commit()
        conn.close()
    return redirect('/')

@app.route('/modifica_collezione/<int:id>', methods=['POST'])
def modifica_collezione(id):
    nuovo_nome = request.form['nuovo_nome']
    if nuovo_nome:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('UPDATE collezioni SET nome = ? WHERE id = ?', (nuovo_nome, id))
        conn.commit()
        conn.close()
    return redirect('/')

@app.route('/elimina_collezione/<int:id>', methods=['POST'])
def elimina_collezione(id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM libri WHERE collezione_id = ?', (id,))
    c.execute('DELETE FROM collezioni WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/modifica_libro/<int:id>', methods=['POST'])
def modifica_libro(id):
    nuovo_titolo = request.form['nuovo_titolo']
    if nuovo_titolo:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('UPDATE libri SET titolo = ? WHERE id = ?', (nuovo_titolo, id))
        conn.commit()
        conn.close()
    return redirect('/')

@app.route('/elimina_libro/<int:id>', methods=['POST'])
def elimina_libro(id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM libri WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=10000)
