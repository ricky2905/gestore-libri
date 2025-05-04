from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('libri.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS collezioni (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS libri (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titolo TEXT NOT NULL,
            collezione_id INTEGER NOT NULL,
            FOREIGN KEY (collezione_id) REFERENCES collezioni(id)
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('libri.db')
    c = conn.cursor()
    c.execute('SELECT id, nome FROM collezioni')
    collezioni = c.fetchall()
    conn.close()
    return render_template('index.html', collezioni=collezioni)

@app.route('/collezione/<int:id>')
def vista_collezione(id):
    conn = sqlite3.connect('libri.db')
    c = conn.cursor()
    c.execute('SELECT nome FROM collezioni WHERE id = ?', (id,))
    nome_collezione = c.fetchone()
    if not nome_collezione:
        return "Collezione non trovata", 404
    nome_collezione = nome_collezione[0]
    c.execute('SELECT titolo FROM libri WHERE collezione_id = ?', (id,))
    libri = c.fetchall()
    conn.close()
    return render_template('collezione.html', collezione_id=id, nome_collezione=nome_collezione, libri=libri)

@app.route('/aggiungi_collezione', methods=['POST'])
def aggiungi_collezione():
    nome = request.form['nome']
    if nome:
        conn = sqlite3.connect('libri.db')
        c = conn.cursor()
        c.execute('INSERT OR IGNORE INTO collezioni (nome) VALUES (?)', (nome,))
        conn.commit()
        conn.close()
    return redirect('/')

@app.route('/collezione/<int:id>/aggiungi_libro', methods=['POST'])
def aggiungi_libro(id):
    titolo = request.form['titolo']
    if titolo:
        conn = sqlite3.connect('libri.db')
        c = conn.cursor()
        c.execute('INSERT INTO libri (titolo, collezione_id) VALUES (?, ?)', (titolo, id))
        conn.commit()
        conn.close()
    return redirect(url_for('vista_collezione', id=id))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=10000)
