from flask import Flask, render_template, request, redirect, url_for, g
import psycopg2
import psycopg2.extras
import os

app = Flask(__name__)
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor)
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    search = request.args.get('q')
    db = get_db()
    cur = db.cursor()
    if search:
        cur.execute("SELECT * FROM collezioni WHERE nome ILIKE %s", (f'%{search}%',))
    else:
        cur.execute("SELECT * FROM collezioni")
    collezioni = cur.fetchall()
    return render_template('index.html', collezioni=collezioni, search=search)

@app.route('/aggiungi_collezione', methods=['GET', 'POST'])
def aggiungi_collezione():
    if request.method == 'POST':
        nome = request.form['nome']
        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO collezioni (nome) VALUES (%s)", (nome,))
        db.commit()
        return redirect(url_for('index'))
    return render_template('aggiungi_collezione.html')

@app.route('/elimina_collezione/<int:collezione_id>', methods=['POST'])
def elimina_collezione(collezione_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM libri WHERE collezione_id = %s", (collezione_id,))
    cur.execute("DELETE FROM collezioni WHERE id = %s", (collezione_id,))
    db.commit()
    return redirect(url_for('index'))

@app.route('/collezione/<int:collezione_id>')
def visualizza_collezione(collezione_id):
    search = request.args.get('q')
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM collezioni WHERE id = %s", (collezione_id,))
    collezione = cur.fetchone()
    if not collezione:
        return "Collezione non trovata", 404
    if search:
        cur.execute(
            "SELECT * FROM libri WHERE collezione_id = %s AND (titolo ILIKE %s OR autore ILIKE %s)",
            (collezione_id, f"%{search}%", f"%{search}%")
        )
    else:
        cur.execute("SELECT * FROM libri WHERE collezione_id = %s", (collezione_id,))
    libri = cur.fetchall()
    return render_template('collezione.html', collezione=collezione, libri=libri, search=search)

@app.route('/aggiungi_libro/<int:collezione_id>', methods=['POST'])
def aggiungi_libro(collezione_id):
    titolo = request.form['titolo']
    autore = request.form['autore']
    anno = request.form.get('anno')
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO libri (titolo, autore, anno, collezione_id, comprato) VALUES (%s, %s, %s, %s, 0)",
        (titolo, autore, anno, collezione_id)
    )
    db.commit()
    return redirect(url_for('visualizza_collezione', collezione_id=collezione_id))

@app.route('/elimina_libro/<int:libro_id>', methods=['POST'])
def elimina_libro(libro_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT collezione_id FROM libri WHERE id = %s", (libro_id,))
    collezione = cur.fetchone()
    cur.execute("DELETE FROM libri WHERE id = %s", (libro_id,))
    db.commit()
    return redirect(url_for('visualizza_collezione', collezione_id=collezione['collezione_id']))

@app.route('/modifica_libro/<int:libro_id>', methods=['POST'])
def modifica_libro(libro_id):
    titolo = request.form['titolo']
    autore = request.form['autore']
    anno = request.form.get('anno')
    comprato = 1 if request.form.get('comprato') == '1' else 0

    db = get_db()
    cur = db.cursor()
    cur.execute(
        "UPDATE libri SET titolo = %s, autore = %s, anno = %s, comprato = %s WHERE id = %s",
        (titolo, autore, anno, comprato, libro_id)
    )
    db.commit()

    cur.execute("SELECT collezione_id FROM libri WHERE id = %s", (libro_id,))
    collezione = cur.fetchone()
    return redirect(url_for('visualizza_collezione', collezione_id=collezione['collezione_id']))

if __name__ == '__main__':
    app.run(debug=True)

