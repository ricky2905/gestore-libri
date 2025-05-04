from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Home: lista collezioni con ricerca
@app.route('/')
def index():
    search = request.args.get('search', '')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    if search:
        cursor.execute("SELECT * FROM collezioni WHERE nome LIKE ?", ('%' + search + '%',))
    else:
        cursor.execute("SELECT * FROM collezioni")
    collezioni = cursor.fetchall()
    conn.close()
    return render_template('index.html', collezioni=collezioni, search=search)

# Aggiungi collezione
@app.route('/aggiungi_collezione', methods=['GET', 'POST'])
def aggiungi_collezione():
    if request.method == 'POST':
        nome = request.form['nome']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO collezioni (nome) VALUES (?)", (nome,))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('aggiungi_collezione.html')

# Modifica collezione
@app.route('/modifica_collezione/<int:id>', methods=['GET', 'POST'])
def modifica_collezione(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        nuovo_nome = request.form['nome']
        cursor.execute("UPDATE collezioni SET nome = ? WHERE id = ?", (nuovo_nome, id))
        conn.commit()
        conn.close()
        return redirect('/')
    cursor.execute("SELECT * FROM collezioni WHERE id = ?", (id,))
    collezione = cursor.fetchone()
    conn.close()
    return render_template('modifica_collezione.html', collezione=collezione)

# Elimina collezione
@app.route('/elimina_collezione/<int:id>')
def elimina_collezione(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM libri WHERE collezione_id = ?", (id,))
    cursor.execute("DELETE FROM collezioni WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# Lista libri per collezione
@app.route('/collezione/<int:id>')
def collezione(id):
    search = request.args.get('search', '')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM collezioni WHERE id = ?", (id,))
    collezione_nome = cursor.fetchone()[0]
    if search:
        cursor.execute("SELECT * FROM libri WHERE collezione_id = ? AND titolo LIKE ?", (id, '%' + search + '%'))
    else:
        cursor.execute("SELECT * FROM libri WHERE collezione_id = ?", (id,))
    libri = cursor.fetchall()
    conn.close()
    return render_template('collezione.html', libri=libri, collezione_id=id, collezione_nome=collezione_nome, search=search)

# Aggiungi libro
@app.route('/aggiungi_libro/<int:collezione_id>', methods=['GET', 'POST'])
def aggiungi_libro(collezione_id):
    if request.method == 'POST':
        titolo = request.form['titolo']
        autore = request.form['autore']
        anno = request.form['anno']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO libri (titolo, autore, anno, collezione_id) VALUES (?, ?, ?, ?)",
                       (titolo, autore, anno, collezione_id))
        conn.commit()
        conn.close()
        return redirect(url_for('collezione', id=collezione_id))
    return render_template('aggiungi_libro.html', collezione_id=collezione_id)

# Modifica libro
@app.route('/modifica_libro/<int:id>', methods=['GET', 'POST'])
def modifica_libro(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        titolo = request.form['titolo']
        autore = request.form['autore']
        anno = request.form['anno']
        cursor.execute("UPDATE libri SET titolo = ?, autore = ?, anno = ? WHERE id = ?", (titolo, autore, anno, id))
        conn.commit()
        cursor.execute("SELECT collezione_id FROM libri WHERE id = ?", (id,))
        collezione_id = cursor.fetchone()[0]
        conn.close()
        return redirect(url_for('collezione', id=collezione_id))
    cursor.execute("SELECT * FROM libri WHERE id = ?", (id,))
    libro = cursor.fetchone()
    conn.close()
    return render_template('modifica_libro.html', libro=libro)

# Elimina libro
@app.route('/elimina_libro/<int:id>')
def elimina_libro(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT collezione_id FROM libri WHERE id = ?", (id,))
    collezione_id = cursor.fetchone()[0]
    cursor.execute("DELETE FROM libri WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('collezione', id=collezione_id))

# Avvio locale
if __name__ == '__main__':
    app.run(debug=True)
