from flask import Flask, request, render_template, redirect
import sqlite3
import os

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists('database.db'):
        conn = sqlite3.connect('database.db')
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
                collezione_id INTEGER NOT NULL,
                nome TEXT NOT NULL,
                FOREIGN KEY (collezione_id) REFERENCES collezioni(id) ON DELETE CASCADE
            )
        ''')

        conn.commit()
        conn.close()
        print("✅ Database inizializzato su Render")

# Esegui solo su Render
if os.environ.get("RENDER") == "true":
    init_db()

@app.route("/")
def index():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT id, nome FROM collezioni')
    collezioni = c.fetchall()
    conn.close()
    return render_template("index.html", collezioni=collezioni)

@app.route("/aggiungi", methods=["POST"])
def aggiungi():
    nome_collezione = request.form["nome"]
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO collezioni (nome) VALUES (?)", (nome_collezione,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/elimina/<int:id>", methods=["POST"])
def elimina(id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM collezioni WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
