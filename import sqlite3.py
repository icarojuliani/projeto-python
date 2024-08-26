import sqlite3

# Conexão ao banco de dados
conn = sqlite3.connect('empresa.db')
cursor = conn.cursor()

# Criação das tabelas
cursor.execute('''
CREATE TABLE IF NOT EXISTS colaboradores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    funcao TEXT NOT NULL,
    contato TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS pecas (
    codigo TEXT PRIMARY KEY,
    descricao TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    ultima_troca DATE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS trocas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    colaborador_id INTEGER,
    peca_codigo TEXT,
    data_troca DATE,
    FOREIGN KEY(colaborador_id) REFERENCES colaboradores(id),
    FOREIGN KEY(peca_codigo) REFERENCES pecas(codigo)
)
''')

conn.commit()

def cadastrar_colaborador(nome, funcao, contato):
    cursor.execute('''
    INSERT INTO colaboradores (nome, funcao, contato)
    VALUES (?, ?, ?)
    ''', (nome, funcao, contato))
    conn.commit()

# Exemplo de uso:
cadastrar_colaborador('João Silva', 'Técnico', 'joao@empresa.com')

def cadastrar_peca(codigo, descricao, quantidade, ultima_troca):
    cursor.execute('''
    INSERT INTO pecas (codigo, descricao, quantidade, ultima_troca)
    VALUES (?, ?, ?, ?)
    ''', (codigo, descricao, quantidade, ultima_troca))
    conn.commit()

# Exemplo de uso:
cadastrar_peca('PEC123', 'Peça de reposição A', 50, '2024-08-08')

from datetime import datetime

def registrar_troca(colaborador_id, peca_codigo):
    data_troca = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('''
    INSERT INTO trocas (colaborador_id, peca_codigo, data_troca)
    VALUES (?, ?, ?)
    ''', (colaborador_id, peca_codigo, data_troca))
    cursor.execute('''
    UPDATE pecas SET quantidade = quantidade - 1, ultima_troca = ?
    WHERE codigo = ?
    ''', (data_troca, peca_codigo))
    conn.commit()

# Exemplo de uso:
registrar_troca(1, 'PEC123')

