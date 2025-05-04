from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_FILE = 'libri.db'

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    collezioni = conn.execute('SELECT * FROM collezioni').fetchall()
    conn.close()
    return render_template('index.html', collezioni=collezioni)

@app.route('/collezione/<int:id>')
def collezione(id):
    conn = get_db_connection()
    collezione = conn.execute('SELECT * FROM collezioni WHERE id = ?', (id,)).fetchone()
    libri = conn.execute('SELECT * FROM libri WHERE collezione_id = ?', (id,)).fetchall()
    conn.close()
    return render_template('collezione.html', collezione=collezione, libri=libri)

@app.route('/aggiungi_collezione', methods=['GET', 'POST'])
def aggiungi_collezione():
    if request.method == 'POST':
        nome = request.form['nome']
        conn = get_db_connection()
        conn.execute('INSERT INTO collezioni (nome) VALUES (?)', (nome,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('aggiungi_collezione.html')

@app.route('/aggiungi_libro/<int:collezione_id>', methods=['GET', 'POST'])
def aggiungi_libro(collezione_id):
    if request.method == 'POST':
        titolo = request.form['titolo']
        autore = request.form['autore']
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO libri (titolo, autore, collezione_id) VALUES (?, ?, ?)',
            (titolo, autore, collezione_id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('collezione', id=collezione_id))
    return render_template('aggiungi_libro.html', collezione_id=collezione_id)

if __name__ == '__main__':
    app.run(debug=True)
