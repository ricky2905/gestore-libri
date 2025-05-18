# Gestore Libri 🇮🇹

Un’applicazione web per gestire le tue collezioni di libri: creazione, modifica e visualizzazione di raccolte e titoli. Backend in Python (Flask), interfaccia HTML/CSS e database PostgreSQL ospitato gratis su Railway.

---

## 📁 Struttura delle directory

```
gestore-libri/
├── app.py                     # entry point dell’app Flask
├── init_db.py                 # script per inizializzare il database
├── README.md                  # documentazione del progetto
├── requirements.txt           # dipendenze Python
├── static/
│   └── style.css              # file CSS per lo styling
└── templates/
    ├── aggiungi_collezione.html
    ├── aggiungi_libro.html
    ├── collezione.html
    ├── index.html
    ├── modifica_collezione.html
    └── modifica_libro.html
```

---

## 🧰 Requisiti di sistema

* Python 3.8+
* `git`, `pip`, `virtualenv`
* Accesso a Railway gratuito per PostgreSQL (incluso)

---

## 📦 Installazione su Ubuntu/Debian

```bash
sudo apt-get update
sudo apt-get install python3-venv python3-pip
```

---

## ⚙️ Setup ambiente virtuale

```bash
git clone https://github.com/<tuo-username>/gestore-libri.git
cd gestore-libri
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📋 Contenuto di requirements.txt

```
Flask
psycopg2-binary
python-dotenv
```

---

## 🔗 Configurazione Database (Railway)

1. Crea un progetto su Railway e aggiungi un’istanza PostgreSQL.
2. Copia l’URL di connessione (es. `DATABASE_URL`) e inseriscilo in un file `.env` nella root:

   ```bash
   DATABASE_URL=postgres://user:pass@host:port/dbname
   ```
3. Esegui l’inizializzazione:

   ```bash
   python init_db.py
   ```

> **Link all’app in produzione:**
> [https://gestore-libri-production.up.railway.app/](https://gestore-libri-production.up.railway.app/)

---

## 🚀 Avvio dell’applicazione

Con l’ambiente virtuale attivo:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development     # opzionale: abilita il debug
flask run
```

Apri il browser su `http://127.0.0.1:5000/`.

---

## ✅ Funzionalità

* **Collezioni:** crea, modifica, elimina raccolte di libri.
* **Libri:** aggiungi, modifica, elimina libri all’interno di ogni collezione.
* **Interfaccia:** template HTML con CSS personalizzato (`static/style.css`).
* **Database remoti:** PostgreSQL gratuito su Railway.

---

## 🧹 Pulizia

```bash
deactivate
rm -rf venv __pycache__
```

Per rimuovere i dati locali di testing:

```bash
dropdb <nome_database_locale>
```

---

## ❓ FAQ

**Perché usare Railway?**
Railway offre un piano gratuito per PostgreSQL, ideale per prototipi e piccoli progetti.

**Come resettare il database?**
Elimina tutte le tabelle (`DROP SCHEMA public CASCADE; CREATE SCHEMA public;`) o ricrea il database e riesegui `init_db.py`.

---

# Book Collection Manager 🇬🇧

A web app to manage your book collections: create, edit and view collections and titles. Built with Python (Flask), HTML/CSS, and PostgreSQL hosted for free on Railway.

---

## 📁 Directory Structure

```
gestore-libri/
├── app.py                     # Flask application entry point
├── init_db.py                 # database initialization script
├── README.md                  # project documentation
├── requirements.txt           # Python dependencies
├── static/
│   └── style.css              # styling
└── templates/
    ├── aggiungi_collezione.html
    ├── aggiungi_libro.html
    ├── collezione.html
    ├── index.html
    ├── modifica_collezione.html
    └── modifica_libro.html
```

---

## 🧰 System Requirements

* Python 3.8+
* `git`, `pip`, `virtualenv`
* Free PostgreSQL on Railway

---

## 📦 Install on Ubuntu/Debian

```bash
sudo apt-get update
sudo apt-get install python3-venv python3-pip
```

---

## ⚙️ Virtual Environment Setup

```bash
git clone https://github.com/<your-username>/gestore-libri.git
cd gestore-libri
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📋 requirements.txt

```
Flask
psycopg2-binary
python-dotenv
```

---

## 🔗 Database Configuration (Railway)

1. Create a Railway project and add a PostgreSQL plugin.
2. Copy the connection URL (e.g. `DATABASE_URL`) into a `.env` file:

   ```bash
   DATABASE_URL=postgres://user:pass@host:port/dbname
   ```
3. Initialize the schema:

   ```bash
   python init_db.py
   ```

> **Production app link:**
> [https://gestore-libri-production.up.railway.app/](https://gestore-libri-production.up.railway.app/)

---

## 🚀 Running the Application

With venv activated:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development     # optional: enables debug
flask run
```

Open `http://127.0.0.1:5000/` in your browser.

---

## ✅ Features

* **Collections:** create, edit, delete book collections.
* **Books:** add, edit, delete books within collections.
* **UI:** HTML templates with custom CSS (`static/style.css`).
* **Remote DB:** free PostgreSQL via Railway.

---

## 🧹 Cleanup

```bash
deactivate
rm -rf venv __pycache__
```

To clear local test data:

```bash
dropdb <local_database_name>
```

---

## ❓ FAQ

**Why use Railway?**
Railway’s free tier offers a managed PostgreSQL instance, perfect for prototypes.

**How to reset the database?**
Drop and recreate the schema (`DROP SCHEMA public CASCADE; CREATE SCHEMA public;`) or delete the database and rerun `init_db.py`.

Happy coding! 🚀
