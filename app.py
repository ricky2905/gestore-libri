from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('libri.db')
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
    conn = sqlite3.connect('libri.db')
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
        conn = sqlite3.connect('libri.db')
        c = conn.cursor()
        c.execute('INSERT INTO libri (collezione, titolo) VALUES (?, ?)', (collezione, titolo))
        conn.commit()
        conn.close()

    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=10000)

