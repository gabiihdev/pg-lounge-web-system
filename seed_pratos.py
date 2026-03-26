import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

pratos = [

    # CARNES
    ("Contra Filé", "Arroz, feijão, farofa e fritas", 26.00, "Carnes", "contra_file.jpg"),
    ("Contra Filé a Cavalo", "Arroz, feijão, farofa e fritas", 30.00, "Carnes", "contra_cavalo.jpg"),
    ("Picanha Lounge", "Arroz, feijão, farofa, fritas e molho à campanha", 42.00, "Carnes", "picanha.jpg"),
    ("Strogonoff de Carne", "Arroz e fritas", 27.00, "Carnes", "strogonoff_carne.jpg"),

    # AVES
    ("Frango Grelhado", "Arroz, feijão, farofa e fritas", 22.00, "Aves", "frango_grelhado.jpg"),
    ("Frango à Parmegiana", "Arroz, feijão e fritas", 25.00, "Aves", "frango_parmegiana.jpg"),
    ("Strogonoff de Frango", "Arroz e fritas", 25.00, "Aves", "strogonoff_frango.jpg"),

    # PESCADOS
    ("Filé de Peixe", "Arroz, feijão e salada", 25.00, "Pescados", "file_peixe.jpg"),
    ("Moqueca de Peixe", "Arroz, pirão e salada", 46.00, "Pescados", "moqueca.jpg"),
    ("Salmão Belle Meunière", "Arroz com brócolis e batata corada", 42.00, "Pescados", "salmao.jpg"),

    # MASSAS
    ("Espaguete à Bolonhesa", "Molho ao sugo com carne moída", 24.00, "Massas", "espaguete_bolonhesa.jpg"),
    ("Espaguete com Camarão", "Molho ao sugo ou branco", 42.00, "Massas", "espaguete_camarao.jpg"),

    # PETISCOS
    ("Batata Frita", "Porção de batata frita crocante", 23.00, "Petiscos", "batata.jpg"),
    ("Gurjão de Frango", "500g de frango crocante", 32.00, "Petiscos", "gurjao_frango.jpg"),
    ("Picanha Aperitivo", "400g de picanha", 70.00, "Petiscos", "picanha_aperitivo.jpg"),

    # SALADAS
    ("Salada do Chefe", "Salada completa com filé mignon", 40.00, "Saladas", "salada.jpg"),

    # GUARNIÇÕES
    ("Arroz à Piamontese", "Arroz cremoso especial", 25.00, "Guarnições", "arroz_piamontese.jpg"),
    ("Batata Corada", "Batatas douradas", 10.00, "Guarnições", "batata_corada.jpg"),

    # SOBREMESAS
    ("Pudim", "Pudim tradicional", 10.00, "Sobremesas", "pudim.jpg"),
    ("Petit Gateau", "Bolo quente com sorvete", 17.00, "Sobremesas", "petit_gateau.jpg"),

    # BEBIDAS
    ("Chopp Brahma", "Chopp gelado", 9.00, "Bebidas", "chopp.jpg"),
    ("Cerveja 600ml", "Cerveja gelada", 11.00, "Bebidas", "cerveja.jpg"),
    ("Refrigerante Lata", "Refrigerante gelado", 7.00, "Bebidas", "refri.jpg"),
]

cursor.executemany("""
INSERT INTO pratos (nome, descricao, preco, categoria, imagem)
VALUES (?, ?, ?, ?, ?)
""", pratos)

conn.commit()
conn.close()

print("Pratos inseridos com sucesso!")