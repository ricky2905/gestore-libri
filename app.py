from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    collezioni = conn.execute('SELECT * FROM collezioni').fetchall()
    conn.close()
    return render_template('index.html', collezioni=collezioni)

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

@app.route('/collezione/<int:id>')
def collezione(id):
    conn = get_db_connection()
    collezione = conn.execute('SELECT * FROM collezioni WHERE id = ?', (id,)).fetchone()
    libri = conn.execute('SELECT * FROM libri WHERE collezione_id = ?', (id,)).fetchall()
    conn.close()
    if collezione is None:
        return "Collezione non trovata", 404
    return render_template('collezione.html', collezione=collezione, libri=libri)

@app.route('/collezione/<int:id>/aggiungi_libro', methods=['GET', 'POST'])
def aggiungi_libro(id):
    if request.method == 'POST':
        titolo = request.form['titolo']
        autore = request.form['autore']
        conn = get_db_connection()
        conn.execute('INSERT INTO libri (titolo, autore, collezione_id) VALUES (?, ?, ?)', (titolo, autore, id))
        conn.commit()
        conn.close()
        return redirect(url_for('collezione', id=id))
    return render_template('aggiungi_libro.html', collezione_id=id)

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        conn = get_db_connection()
        conn.execute('CREATE TABLE collezioni (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT)')
        conn.execute('CREATE TABLE libri (id INTEGER PRIMARY KEY AUTOINCREMENT, titolo TEXT, autore TEXT, collezione_id INTEGER)')
        conn.commit()
        conn.close()
    app.run(debug=True)
