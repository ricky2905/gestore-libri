from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
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
    if search:
        collezioni = db.execute("SELECT * FROM collezioni WHERE nome LIKE ?", ('%' + search + '%',)).fetchall()
    else:
        collezioni = db.execute("SELECT * FROM collezioni").fetchall()
    return render_template('index.html', collezioni=collezioni, search=search)

@app.route('/aggiungi_collezione', methods=['GET', 'POST'])
def aggiungi_collezione():
    if request.method == 'POST':
        nome = request.form['nome']
        db = get_db()
        db.execute("INSERT INTO collezioni (nome) VALUES (?)", (nome,))
        db.commit()
        return redirect(url_for('index'))
    return render_template('aggiungi_collezione.html')

@app.route('/elimina_collezione/<int:collezione_id>', methods=['POST'])
def elimina_collezione(collezione_id):
    db = get_db()
    db.execute("DELETE FROM libri WHERE collezione_id = ?", (collezione_id,))
    db.execute("DELETE FROM collezioni WHERE id = ?", (collezione_id,))
    db.commit()
    return redirect(url_for('index'))

@app.route('/collezione/<int:collezione_id>')
def visualizza_collezione(collezione_id):
    search = request.args.get('q')
    db = get_db()
    collezione = db.execute("SELECT * FROM collezioni WHERE id = ?", (collezione_id,)).fetchone()
    if not collezione:
        return "Collezione non trovata", 404
    if search:
        libri = db.execute(
            "SELECT * FROM libri WHERE collezione_id = ? AND (titolo LIKE ? OR autore LIKE ?)",
            (collezione_id, f"%{search}%", f"%{search}%")
        ).fetchall()
    else:
        libri = db.execute("SELECT * FROM libri WHERE collezione_id = ?", (collezione_id,)).fetchall()
    return render_template('collezione.html', collezione=collezione, libri=libri, search=search)

@app.route('/aggiungi_libro/<int:collezione_id>', methods=['POST'])
def aggiungi_libro(collezione_id):
    titolo = request.form['titolo']
    autore = request.form['autore']
    anno = request.form.get('anno')
    db = get_db()
    db.execute("INSERT INTO libri (titolo, autore, anno, collezione_id, comprato) VALUES (?, ?, ?, ?, 0)",
               (titolo, autore, anno, collezione_id))
    db.commit()
    return redirect(url_for('visualizza_collezione', collezione_id=collezione_id))

@app.route('/elimina_libro/<int:libro_id>', methods=['POST'])
def elimina_libro(libro_id):
    db = get_db()
    collezione = db.execute("SELECT collezione_id FROM libri WHERE id = ?", (libro_id,)).fetchone()
    db.execute("DELETE FROM libri WHERE id = ?", (libro_id,))
    db.commit()
    return redirect(url_for('visualizza_collezione', collezione_id=collezione['collezione_id']))

@app.route('/modifica_libro/<int:libro_id>', methods=['POST'])
def modifica_libro(libro_id):
    titolo = request.form['titolo']
    autore = request.form['autore']
    anno = request.form.get('anno')
    comprato = 1 if request.form.get('comprato') == '1' else 0

    db = get_db()
    db.execute(
        "UPDATE libri SET titolo = ?, autore = ?, anno = ?, comprato = ? WHERE id = ?",
        (titolo, autore, anno, comprato, libro_id)
    )
    db.commit()

    collezione = db.execute("SELECT collezione_id FROM libri WHERE id = ?", (libro_id,)).fetchone()
    return redirect(url_for('visualizza_collezione', collezione_id=collezione['collezione_id']))

if __name__ == '__main__':
    app.run(debug=True)
