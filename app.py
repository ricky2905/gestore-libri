from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DB_NAME = "libri.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    collezioni = conn.execute("SELECT * FROM collezioni").fetchall()
    conn.close()
    return render_template("index.html", collezioni=collezioni)

@app.route("/aggiungi_collezione", methods=["GET", "POST"])
def aggiungi_collezione():
    if request.method == "POST":
        nome = request.form["nome"]
        descrizione = request.form["descrizione"]
        conn = get_db_connection()
        conn.execute("INSERT INTO collezioni (nome, descrizione) VALUES (?, ?)", (nome, descrizione))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("aggiungi_collezione.html")

@app.route("/collezione/<int:id>")
def collezione(id):
    conn = get_db_connection()
    collezione = conn.execute("SELECT * FROM collezioni WHERE id = ?", (id,)).fetchone()
    libri = conn.execute("SELECT * FROM libri WHERE collezione_id = ?", (id,)).fetchall()
    conn.close()
    return render_template("collezione.html", collezione=collezione, libri=libri)

@app.route("/aggiungi_libro/<int:collezione_id>", methods=["GET", "POST"])
def aggiungi_libro(collezione_id):
    if request.method == "POST":
        titolo = request.form["titolo"]
        autore = request.form["autore"]
        anno = request.form["anno"]
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO libri (titolo, autore, anno, collezione_id) VALUES (?, ?, ?, ?)",
            (titolo, autore, anno, collezione_id),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("collezione", id=collezione_id))
    return render_template("aggiungi_libro.html", collezione_id=collezione_id)

@app.route("/elimina_libro/<int:id>")
def elimina_libro(id):
    conn = get_db_connection()
    libro = conn.execute("SELECT collezione_id FROM libri WHERE id = ?", (id,)).fetchone()
    conn.execute("DELETE FROM libri WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("collezione", id=libro["collezione_id"]))

@app.route("/elimina_collezione/<int:id>")
def elimina_collezione(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM libri WHERE collezione_id = ?", (id,))
    conn.execute("DELETE FROM collezioni WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/modifica_libro/<int:id>", methods=["GET", "POST"])
def modifica_libro(id):
    conn = get_db_connection()
    libro = conn.execute("SELECT * FROM libri WHERE id = ?", (id,)).fetchone()
    if request.method == "POST":
        titolo = request.form["titolo"]
        autore = request.form["autore"]
        anno = request.form["anno"]
        conn.execute("UPDATE libri SET titolo = ?, autore = ?, anno = ? WHERE id = ?", (titolo, autore, anno, id))
        conn.commit()
        conn.close()
        return redirect(url_for("collezione", id=libro["collezione_id"]))
    conn.close()
    return render_template("modifica_libro.html", libro=libro)

@app.route("/modifica_collezione/<int:id>", methods=["GET", "POST"])
def modifica_collezione(id):
    conn = get_db_connection()
    collezione = conn.execute("SELECT * FROM collezioni WHERE id = ?", (id,)).fetchone()
    if request.method == "POST":
        nome = request.form["nome"]
        descrizione = request.form["descrizione"]
        conn.execute("UPDATE collezioni SET nome = ?, descrizione = ? WHERE id = ?", (nome, descrizione, id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    conn.close()
    return render_template("modifica_collezione.html", collezione=collezione)

if __name__ == "__main__":
    app.run(debug=True)
