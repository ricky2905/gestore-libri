from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'libri.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS libri (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            collezione TEXT NOT NULL,
            titolo TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT collezione, titolo FROM libri')
    libri = c.fetchall()
    conn.close()
    return render_template('index.html', libri=libri)

@app.route('/aggiungi', methods=['POST'])
def aggiungi_libro():
    collezione = request.form['collezione']
    titolo = request.form['titolo']

    if collezione and titolo:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO libri (collezione, titolo) VALUES (?, ?)', (collezione, titolo))
        conn.commit()
        conn.close()

    return redirect('/')

# solo su Render chiamato via gunicorn
init_db()

# non usare app.run per Render
