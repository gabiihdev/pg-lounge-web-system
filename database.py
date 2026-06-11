import sqlite3

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pratos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT NOT NULL,
        preco REAL NOT NULL,
        categoria TEXT,
        imagem TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedbacks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        comentario TEXT NOT NULL,
        avaliacao INTEGER NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS curriculos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL,
        telefone TEXT NOT NULL,
        area_interesse TEXT NOT NULL,
        disponibilidade TEXT NOT NULL,
        experiencia TEXT,
        data_envio TEXT NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS eventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descricao TEXT NOT NULL,
        data_evento TEXT NOT NULL,
        imagem TEXT
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()