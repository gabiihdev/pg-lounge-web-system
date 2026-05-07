from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "pg_lounge_secret"

ADMIN_USER = "pglounge_admin"
ADMIN_PASSWORD = "pg2026"

def get_pratos():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT nome, descricao, preco, categoria, imagem FROM pratos")
    pratos = cursor.fetchall()
    
    conn.close()
    return pratos

def get_feedbacks_home():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT nome, comentario, avaliacao 
        FROM feedbacks 
        ORDER BY id DESC 
        LIMIT 3
    """)

    feedbacks = cursor.fetchall()
    conn.close()
    return feedbacks


def get_feedbacks():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT nome, comentario, avaliacao 
        FROM feedbacks 
        ORDER BY id DESC
    """)

    feedbacks = cursor.fetchall()
    conn.close()
    return feedbacks

def get_dashboard_data():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM pratos")
    total_pratos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM feedbacks")
    total_feedbacks = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(avaliacao) FROM feedbacks")
    media_avaliacoes = cursor.fetchone()[0]

    conn.close()

    if media_avaliacoes is None:
        media_avaliacoes = 0

    return {
        "total_pratos": total_pratos,
        "total_feedbacks": total_feedbacks,
        "media_avaliacoes": round(media_avaliacoes, 1)
    }

@app.route("/")
def home():
    feedbacks = get_feedbacks_home()
    return render_template("index.html", feedbacks=feedbacks)


@app.route("/cardapio")
def cardapio():
    pratos = get_pratos()
    
    categorias = {}
    
    for prato in pratos:
        categoria = prato[3]
        
        if categoria not in categorias:
            categorias[categoria] = []
            
        categorias[categoria].append(prato)
    
    return render_template("cardapio.html", categorias=categorias)


@app.route("/contato")
def contato():
    return render_template("contato.html")

@app.route("/feedback", methods=["GET", "POST"])
def feedback():

    if request.method == "POST":
        nome = request.form["nome"]
        comentario = request.form["comentario"]
        avaliacao = int(request.form["avaliacao"])

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO feedbacks (nome, comentario, avaliacao)
            VALUES (?, ?, ?)
        """, (nome, comentario, avaliacao))

        conn.commit()
        conn.close()

        return redirect(url_for("feedbacks")) 

    return render_template("feedback.html")


@app.route("/feedbacks")
def feedbacks():
    feedbacks = get_feedbacks()
    return render_template("feedbacks.html", feedbacks=feedbacks)

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form["usuario"]
        senha = request.form["senha"]

        if usuario == ADMIN_USER and senha == ADMIN_PASSWORD:

            session["admin"] = True

            return redirect(url_for("admin"))

    return render_template("login.html")


@app.route("/admin")
def admin():

    if "admin" not in session:
        return redirect(url_for("login"))

    dashboard = get_dashboard_data()

    return render_template("admin.html", dashboard=dashboard)

if __name__ == "__main__":
    app.run(debug=True)