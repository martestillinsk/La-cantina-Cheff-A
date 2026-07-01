import sqlite3

# Conecta ao banco de dados (cria o arquivo cantina.db se não existir)
conn = sqlite3.connect("cantina.db")

# cursor é o que executa os comandos no banco
cursor = conn.cursor()

# Cria a tabela de produtos
cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        nome        TEXT    NOT NULL,
        preco       REAL    NOT NULL,
        quantidade  INTEGER NOT NULL DEFAULT 0,
        estoque_min INTEGER NOT NULL DEFAULT 5
    )
""")

# Cria a tabela de pedidos
cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id  INTEGER NOT NULL,
        quantidade  INTEGER NOT NULL,
        valor_total REAL    NOT NULL,
        criado_em        TEXT    DEFAULT (datetime('now', 'localtime'))
    )
""")

# Cria a tabela de movimentações de estoque
cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimentacoes (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER NOT NULL,
        tipo       TEXT    NOT NULL,
        quantidade INTEGER NOT NULL,
        motivo     TEXT,
        criado_em  TEXT    DEFAULT (datetime('now', 'localtime'))
    )
""")

# Salva tudo e fecha a conexão
conn.commit()
conn.close()

print("Banco de dados criado com sucesso!")