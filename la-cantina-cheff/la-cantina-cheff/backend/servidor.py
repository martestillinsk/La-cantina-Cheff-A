from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# ─────────────────────────────────────
# FUNÇÃO AUXILIAR - conecta ao banco
# ─────────────────────────────────────

def conectar():
    conn = sqlite3.connect("cantina.db")
    conn.row_factory = sqlite3.Row  # permite acessar colunas pelo nome
    return conn

# ─────────────────────────────────────
# PRODUTOS
# ─────────────────────────────────────

# Listar todos os produtos
@app.route("/produtos", methods=["GET"])
def listar_produtos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    produtos = [dict(p) for p in cursor.fetchall()]
    conn.close()
    return jsonify(produtos)

# Cadastrar produto
@app.route("/produtos", methods=["POST"])
def cadastrar_produto():
    dados = request.get_json()
    nome        = dados.get("nome")
    preco       = dados.get("preco")
    quantidade  = dados.get("quantidade", 0)
    estoque_min = dados.get("estoque_min", 5)

    if not nome or not preco:
        return jsonify({"erro": "Nome e preço são obrigatórios!"}), 400

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO produtos (nome, preco, quantidade, estoque_min)
        VALUES (?, ?, ?, ?)
    """, (nome, preco, quantidade, estoque_min))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Produto cadastrado com sucesso!"}), 201

# Editar produto
@app.route("/produtos/<int:produto_id>", methods=["PUT"])
def editar_produto(produto_id):
    dados = request.get_json()
    nome        = dados.get("nome")
    preco       = dados.get("preco")
    quantidade  = dados.get("quantidade")
    estoque_min = dados.get("estoque_min")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE produtos
        SET nome=?, preco=?, quantidade=?, estoque_min=?
        WHERE id=?
    """, (nome, preco, quantidade, estoque_min, produto_id))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Produto atualizado com sucesso!"})

# Excluir produto
@app.route("/produtos/<int:produto_id>", methods=["DELETE"])
def excluir_produto(produto_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE id=?", (produto_id,))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Produto excluído com sucesso!"})

# ─────────────────────────────────────
# PEDIDOS
# ─────────────────────────────────────

# Listar todos os pedidos
@app.route("/pedidos", methods=["GET"])
def listar_pedidos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT pedidos.id, produtos.nome, pedidos.quantidade,
               pedidos.valor_total, pedidos.criado_em
        FROM pedidos
        JOIN produtos ON produtos.id = pedidos.produto_id
        ORDER BY pedidos.criado_em DESC
    """)
    pedidos = [dict(p) for p in cursor.fetchall()]
    conn.close()
    return jsonify(pedidos)

# Registrar pedido
@app.route("/pedidos", methods=["POST"])
def registrar_pedido():
    dados = request.get_json()
    produto_id = dados.get("produto_id")
    quantidade = dados.get("quantidade")

    conn = conectar()
    cursor = conn.cursor()

    # Busca o produto no banco
    cursor.execute("SELECT * FROM produtos WHERE id=?", (produto_id,))
    produto = cursor.fetchone()

    # Verifica se o produto existe
    if not produto:
        conn.close()
        return jsonify({"erro": "Produto não encontrado!"}), 404

    # Verifica se tem estoque suficiente
    if produto["quantidade"] < quantidade:
        conn.close()
        return jsonify({"erro": f"Estoque insuficiente! Disponível: {produto['quantidade']}"}), 400

    # Calcula o valor total
    valor_total = produto["preco"] * quantidade

    # Salva o pedido
    cursor.execute("""
        INSERT INTO pedidos (produto_id, quantidade, valor_total)
        VALUES (?, ?, ?)
    """, (produto_id, quantidade, valor_total))

    # Baixa o estoque automaticamente
    cursor.execute("""
        UPDATE produtos SET quantidade = quantidade - ?
        WHERE id=?
    """, (quantidade, produto_id))

    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Pedido registrado!", "valor_total": valor_total}), 201

# Cancelar pedido
@app.route("/pedidos/<int:pedido_id>", methods=["DELETE"])
def cancelar_pedido(pedido_id):
    conn = conectar()
    cursor = conn.cursor()

    # Busca o pedido
    cursor.execute("SELECT * FROM pedidos WHERE id=?", (pedido_id,))
    pedido = cursor.fetchone()

    if not pedido:
        conn.close()
        return jsonify({"erro": "Pedido não encontrado!"}), 404

    # Devolve o estoque ao produto
    cursor.execute("""
        UPDATE produtos SET quantidade = quantidade + ?
        WHERE id=?
    """, (pedido["quantidade"], pedido["produto_id"]))

    # Apaga o pedido
    cursor.execute("DELETE FROM pedidos WHERE id=?", (pedido_id,))

    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Pedido cancelado e estoque devolvido!"})

# Relatório semanal - só os últimos 7 dias
@app.route("/relatorios/semanal", methods=["GET"])
def relatorio_semanal():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT pedidos.id, produtos.nome, pedidos.quantidade,
               pedidos.valor_total, pedidos.criado_em
        FROM pedidos
        JOIN produtos ON produtos.id = pedidos.produto_id
        WHERE DATE(pedidos.criado_em) >= DATE('now', '-6 days')
        ORDER BY pedidos.criado_em DESC
    """)
    pedidos = [dict(p) for p in cursor.fetchall()]
    conn.close()
    return jsonify(pedidos)

# ─────────────────────────────────────
# ESTOQUE
# ─────────────────────────────────────

# Listar estoque atual
@app.route("/estoque", methods=["GET"])
def listar_estoque():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    produtos = [dict(p) for p in cursor.fetchall()]
    conn.close()
    return jsonify(produtos)

# Listar movimentações
@app.route("/estoque/movimentacoes", methods=["GET"])
def listar_movimentacoes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT movimentacoes.id, produtos.nome, movimentacoes.tipo,
               movimentacoes.quantidade, movimentacoes.motivo,
               movimentacoes.criado_em
        FROM movimentacoes
        JOIN produtos ON produtos.id = movimentacoes.produto_id
    """)
    movimentacoes = [dict(m) for m in cursor.fetchall()]
    conn.close()
    return jsonify(movimentacoes)

# Entrada de estoque
@app.route("/estoque/entrada", methods=["POST"])
def entrada_estoque():
    dados = request.get_json()
    produto_id = dados.get("produto_id")
    quantidade = dados.get("quantidade")
    motivo     = dados.get("motivo", "Entrada manual")

    if not produto_id or not quantidade or quantidade <= 0:
        return jsonify({"erro": "Produto e quantidade são obrigatórios!"}), 400

    conn = conectar()
    cursor = conn.cursor()

    # Verifica se o produto existe
    cursor.execute("SELECT * FROM produtos WHERE id=?", (produto_id,))
    produto = cursor.fetchone()

    if not produto:
        conn.close()
        return jsonify({"erro": "Produto não encontrado!"}), 404

    # Adiciona ao estoque
    cursor.execute("""
        UPDATE produtos SET quantidade = quantidade + ?
        WHERE id=?
    """, (quantidade, produto_id))

    # Registra a movimentação
    cursor.execute("""
        INSERT INTO movimentacoes (produto_id, tipo, quantidade, motivo)
        VALUES (?, 'entrada', ?, ?)
    """, (produto_id, quantidade, motivo))

    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Entrada registrada com sucesso!"})

# Saída de estoque
@app.route("/estoque/saida", methods=["POST"])
def saida_estoque():
    dados = request.get_json()
    produto_id = dados.get("produto_id")
    quantidade = dados.get("quantidade")
    motivo     = dados.get("motivo", "Saída manual")

    if not produto_id or not quantidade or quantidade <= 0:
        return jsonify({"erro": "Produto e quantidade são obrigatórios!"}), 400

    conn = conectar()
    cursor = conn.cursor()

    # Verifica se o produto existe
    cursor.execute("SELECT * FROM produtos WHERE id=?", (produto_id,))
    produto = cursor.fetchone()

    if not produto:
        conn.close()
        return jsonify({"erro": "Produto não encontrado!"}), 404

    # Verifica se tem estoque suficiente
    if produto["quantidade"] < quantidade:
        conn.close()
        return jsonify({"erro": f"Estoque insuficiente! Disponível: {produto['quantidade']}"}), 400

    # Remove do estoque
    cursor.execute("""
        UPDATE produtos SET quantidade = quantidade - ?
        WHERE id=?
    """, (quantidade, produto_id))

    # Registra a movimentação
    cursor.execute("""
        INSERT INTO movimentacoes (produto_id, tipo, quantidade, motivo)
        VALUES (?, 'saida', ?, ?)
    """, (produto_id, quantidade, motivo))

    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Saída registrada com sucesso!"})

# ─────────────────────────────────────
# INICIAR O SERVIDOR
# ─────────────────────────────────────

if __name__ == "__main__":
    print("Servidor rodando em http://localhost:5000")
    app.run(debug=True, port=5000)