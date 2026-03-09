from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_pratos():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT nome, descricao, preco, categoria, imagem FROM pratos")
    pratos = cursor.fetchall()
    
    conn.close()
    return pratos

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/cardapio")
def cardapio():
    pratos = get_pratos()
    return render_template("cardapio.html", pratos=pratos)

@app.route("/contato")
def contato():
    return render_template("contato.html")

if __name__ == "__main__":
    app.run(debug=True)