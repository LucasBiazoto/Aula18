import mysql.connector
from datetime import date

# ===============================
# Conexão com o Banco de Dados
# ===============================
def conectar_banco():
    """Função para conectar ao banco de dados MySQL."""
    return mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='Toronto01#',
        database='loja1'   # Certifique-se que está usando 'loja1'
    )

# ===============================
# Funções de Cadastro
# ===============================
def cadastrar_produto(nome, preco):
    """Cadastra um novo produto na tabela Produtos."""
    conexao = conectar_banco()
    cursor = conexao.cursor()
    try:
        cursor.execute("INSERT INTO Produtos (Nome, Preco) VALUES (%s, %s)", (nome, preco))
        conexao.commit()
        print(f"Produto '{nome}' cadastrado com sucesso!")
    except mysql.connector.Error as erro:
        print("Erro ao cadastrar produto:", erro)
    finally:
        cursor.close()
        conexao.close()

def cadastrar_fornecedor(nome, contato):
    """Cadastra um novo fornecedor na tabela Fornecedores."""
    conexao = conectar_banco()
    cursor = conexao.cursor()
    try:
        cursor.execute("INSERT INTO Fornecedores (Nome, Contato) VALUES (%s, %s)", (nome, contato))
        conexao.commit()
        print(f"Fornecedor '{nome}' cadastrado com sucesso!")
    except mysql.connector.Error as erro:
        print("Erro ao cadastrar fornecedor:", erro)
    finally:
        cursor.close()
        conexao.close()

def cadastrar_entrada_estoque(produto_id, fornecedor_id, quantidade):
    """Cadastra uma nova entrada de estoque na tabela Estoque."""
    if quantidade < 0:
        print("Erro: A quantidade não pode ser negativa.")
        return
    conexao = conectar_banco()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "INSERT INTO Estoque (ProdutoID, FornecedorID, Quantidade, DataEntrada) VALUES (%s, %s, %s, %s)",
            (produto_id, fornecedor_id, quantidade, date.today())
        )
        conexao.commit()
        print("Entrada de estoque cadastrada com sucesso!")
    except mysql.connector.Error as erro:
        print("Erro ao inserir dados:", erro)
    finally:
        cursor.close()
        conexao.close()

# ===============================
# Funções de Consulta
# ===============================
def consultar_estoque():
    """Consulta todos os registros do estoque."""
    conexao = conectar_banco()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM Estoque")
        return cursor.fetchall()
    except mysql.connector.Error as erro:
        print("Erro ao consultar estoque:", erro)
        return []
    finally:
        cursor.close()
        conexao.close()

def consultar_produto_por_id(produto_id):
    """Consulta um produto específico no estoque pelo ProdutoID."""
    conexao = conectar_banco()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM Estoque WHERE ProdutoID = %s", (produto_id,))
        return cursor.fetchall()
    except mysql.connector.Error as erro:
        print("Erro ao consultar produto:", erro)
        return []
    finally:
        cursor.close()
        conexao.close()

# ===============================
# Testes do Sistema
# ===============================
if __name__ == "__main__":
    print("--- TESTES DO SISTEMA DE ESTOQUE ---")

    print("\n--- Teste de Cadastro de Produto e Fornecedor ---")
    cadastrar_produto("Camiseta", 59.90)
    cadastrar_fornecedor("Fornecedor A", "email@fornecedor.com")

    print("\n--- Teste de Cadastro no Estoque ---")
    cadastrar_entrada_estoque(1, 1, 10)  # ProdutoID=1, FornecedorID=1

    print("\n--- Teste de Validação ---")
    cadastrar_entrada_estoque(1, 1, -5)  # Quantidade negativa -> erro

    print("\n--- Consulta Geral do Estoque ---")
    registros = consultar_estoque()
    for registro in registros:
        print(registro)

    print("\n--- Pesquisa por ProdutoID ---")
    resultado = consultar_produto_por_id(1)
    for registro in resultado:
        print(registro)

    print("\n--- FIM DOS TESTES ---")
