from flask import Flask, render_template, request, redirect, url_for, session, flash, Response
import sqlite3
from datetime import datetime

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

def get_pratos_admin():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, preco, categoria
        FROM pratos
        ORDER BY categoria
    """)

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

def get_feedbacks_admin():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, comentario, avaliacao
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

    cursor.execute("SELECT COUNT(*) FROM curriculos")
    total_curriculos = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(avaliacao) FROM feedbacks")
    media_avaliacoes = cursor.fetchone()[0]

    conn.close()

    if media_avaliacoes is None:
        media_avaliacoes = 0

    return {
        "total_pratos": total_pratos,
        "total_feedbacks": total_feedbacks,
        "total_curriculos": total_curriculos,
        "media_avaliacoes": round(media_avaliacoes, 1)
    }
    
def get_curriculos():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            nome,
            email,
            telefone,
            area_interesse,
            disponibilidade,
            experiencia,
            data_envio
        FROM curriculos
        ORDER BY id DESC
    """)

    curriculos = cursor.fetchall()

    conn.close()

    return curriculos

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

@app.route("/admin/feedbacks")
def admin_feedbacks():

    if "admin" not in session:
        return redirect(url_for("login"))

    feedbacks = get_feedbacks_admin()

    return render_template(
        "admin_feedbacks.html",
        feedbacks=feedbacks
    )
    
@app.route("/admin/excluir-feedback/<int:id>")
def excluir_feedback(id):

    if "admin" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM feedbacks WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    flash("Feedback excluído com sucesso!")

    return redirect(url_for("admin_feedbacks"))

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form["usuario"]
        senha = request.form["senha"]

        if usuario == ADMIN_USER and senha == ADMIN_PASSWORD:

            session["admin"] = True

            flash("Login realizado com sucesso!")

            return redirect(url_for("admin"))

        flash("Usuário ou senha inválidos!")

    return render_template("login.html")

@app.route("/admin")
def admin():

    if "admin" not in session:
        return redirect(url_for("login"))

    dashboard = get_dashboard_data()

    return render_template("admin.html", dashboard=dashboard)

@app.route("/logout")
def logout():

    session.pop("admin", None)

    return redirect(url_for("home"))

@app.route("/admin/cardapio")
def admin_cardapio():

    if "admin" not in session:
        return redirect(url_for("login"))

    pratos = get_pratos_admin()

    return render_template(
        "admin_cardapio.html",
        pratos=pratos
    )
    
@app.route("/admin/excluir-prato/<int:id>")
def excluir_prato(id):

    if "admin" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM pratos WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()
    
    flash("Prato excluído com sucesso!")

    return redirect(url_for("admin_cardapio"))

@app.route("/admin/adicionar-prato", methods=["GET", "POST"])
def adicionar_prato():

    if "admin" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        nome = request.form["nome"]
        descricao = request.form["descricao"]
        preco = request.form["preco"]
        categoria = request.form["categoria"]
        imagem = request.form["imagem"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO pratos
            (nome, descricao, preco, categoria, imagem)
            VALUES (?, ?, ?, ?, ?)
        """, (
            nome,
            descricao,
            preco,
            categoria,
            imagem
        ))

        conn.commit()
        conn.close()

        flash("Prato cadastrado com sucesso!")
        
        return redirect(url_for("admin_cardapio"))

    return render_template("adicionar_prato.html")

@app.route("/admin/editar-prato/<int:id>", methods=["GET", "POST"])
def editar_prato(id):

    if "admin" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":

        nome = request.form["nome"]
        descricao = request.form["descricao"]
        preco = request.form["preco"]
        categoria = request.form["categoria"]
        imagem = request.form["imagem"]

        cursor.execute("""
            UPDATE pratos
            SET nome = ?,
                descricao = ?,
                preco = ?,
                categoria = ?,
                imagem = ?
            WHERE id = ?
        """, (
            nome,
            descricao,
            preco,
            categoria,
            imagem,
            id
        ))

        conn.commit()
        conn.close()
        
        flash("Prato atualizado com sucesso!")

        return redirect(url_for("admin_cardapio"))

    cursor.execute("""
        SELECT id, nome, descricao, preco, categoria, imagem
        FROM pratos
        WHERE id = ?
    """, (id,))

    prato = cursor.fetchone()

    conn.close()

    return render_template(
        "editar_prato.html",
        prato=prato
    )

@app.route("/trabalhe-conosco", methods=["GET", "POST"])
def trabalhe_conosco():

    if request.method == "POST":

        nome = request.form["nome"]
        email = request.form["email"]
        telefone = request.form["telefone"]
        area_interesse = request.form["area_interesse"]
        disponibilidade = request.form["disponibilidade"]
        experiencia = request.form["experiencia"]
        data_envio = datetime.now().strftime("%d/%m/%Y %H:%M")

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO curriculos (
            nome,
            email,
            telefone,
            area_interesse,
            disponibilidade,
            experiencia,
            data_envio
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            nome,
            email,
            telefone,
            area_interesse,
            disponibilidade,
            experiencia,
            data_envio
        ))

        conn.commit()
        conn.close()

        flash("Currículo enviado com sucesso!")

        return redirect(url_for("trabalhe_conosco"))

    return render_template("trabalhe_conosco.html")

@app.route("/admin/curriculos")
def admin_curriculos():

    if "admin" not in session:
        return redirect(url_for("login"))

    curriculos = get_curriculos()

    return render_template(
        "admin_curriculos.html",
        curriculos=curriculos
    )
    
@app.route("/admin/excluir-curriculo/<int:id>")
def excluir_curriculo(id):

    if "admin" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM curriculos WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    flash("Currículo excluído com sucesso!")

    return redirect(url_for("admin_curriculos"))

@app.route("/admin/exportar-curriculos")
def exportar_curriculos():

    if "admin" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            nome,
            email,
            telefone,
            area_interesse,
            disponibilidade,
            experiencia,
            data_envio
        FROM curriculos
    """)

    curriculos = cursor.fetchall()

    conn.close()

    def gerar_csv():

        yield "Nome,E-mail,Telefone,Área,Disponibilidade,Experiência,Data de Envio\n"

        for curriculo in curriculos:
            yield ",".join(str(campo) for campo in curriculo) + "\n"

    return Response(
        gerar_csv(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=curriculos.csv"
        }
    )

if __name__ == "__main__":
    app.run(debug=True)