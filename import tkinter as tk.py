import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# Conexão ao banco de dados
conn = sqlite3.connect('empresa.db')
cursor = conn.cursor()

# Funções para a aplicação
def cadastrar_colaborador():
    nome = entry_nome.get()
    funcao = entry_funcao.get()
    contato = entry_contato.get()
    
    if nome and funcao:
        cursor.execute('''
        INSERT INTO colaboradores (nome, funcao, contato)
        VALUES (?, ?, ?)
        ''', (nome, funcao, contato))
        conn.commit()
        messagebox.showinfo("Sucesso", "Colaborador cadastrado com sucesso!")
        limpar_campos()
    else:
        messagebox.showwarning("Atenção", "Por favor, preencha todos os campos obrigatórios.")

def cadastrar_peca():
    codigo = entry_codigo.get()
    descricao = entry_descricao.get()
    quantidade = entry_quantidade.get()
    
    if codigo and descricao and quantidade.isdigit():
        cursor.execute('''
        INSERT INTO pecas (codigo, descricao, quantidade, ultima_troca)
        VALUES (?, ?, ?, ?)
        ''', (codigo, descricao, int(quantidade), None))
        conn.commit()
        messagebox.showinfo("Sucesso", "Peça cadastrada com sucesso!")
        limpar_campos()
    else:
        messagebox.showwarning("Atenção", "Por favor, preencha todos os campos corretamente.")

def registrar_troca():
    colaborador_id = entry_colaborador_id.get()
    peca_codigo = entry_peca_codigo.get()
    
    if colaborador_id.isdigit() and peca_codigo:
        data_troca = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
        INSERT INTO trocas (colaborador_id, peca_codigo, data_troca)
        VALUES (?, ?, ?)
        ''', (int(colaborador_id), peca_codigo, data_troca))
        
        cursor.execute('''
        UPDATE pecas SET quantidade = quantidade - 1, ultima_troca = ?
        WHERE codigo = ?
        ''', (data_troca, peca_codigo))
        
        conn.commit()
        messagebox.showinfo("Sucesso", "Troca registrada com sucesso!")
        limpar_campos()
    else:
        messagebox.showwarning("Atenção", "Por favor, preencha todos os campos corretamente.")

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_funcao.delete(0, tk.END)
    entry_contato.delete(0, tk.END)
    entry_codigo.delete(0, tk.END)
    entry_descricao.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)
    entry_colaborador_id.delete(0, tk.END)
    entry_peca_codigo.delete(0, tk.END)

# Interface Gráfica
root = tk.Tk()
root.title("Sistema de Registro de Colaboradores e Peças")

# Cadastro de Colaboradores
frame_colaborador = tk.LabelFrame(root, text="Cadastro de Colaboradores")
frame_colaborador.pack(fill="both", expand="yes", padx=10, pady=10)

tk.Label(frame_colaborador, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
entry_nome = tk.Entry(frame_colaborador)
entry_nome.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_colaborador, text="Função:").grid(row=1, column=0, padx=5, pady=5)
entry_funcao = tk.Entry(frame_colaborador)
entry_funcao.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_colaborador, text="Contato:").grid(row=2, column=0, padx=5, pady=5)
entry_contato = tk.Entry(frame_colaborador)
entry_contato.grid(row=2, column=1, padx=5, pady=5)

tk.Button(frame_colaborador, text="Cadastrar Colaborador", command=cadastrar_colaborador).grid(row=3, columnspan=2, pady=10)

# Cadastro de Peças
frame_peca = tk.LabelFrame(root, text="Cadastro de Peças")
frame_peca.pack(fill="both", expand="yes", padx=10, pady=10)

tk.Label(frame_peca, text="Código:").grid(row=0, column=0, padx=5, pady=5)
entry_codigo = tk.Entry(frame_peca)
entry_codigo.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_peca, text="Descrição:").grid(row=1, column=0, padx=5, pady=5)
entry_descricao = tk.Entry(frame_peca)
entry_descricao.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_peca, text="Quantidade:").grid(row=2, column=0, padx=5, pady=5)
entry_quantidade = tk.Entry(frame_peca)
entry_quantidade.grid(row=2, column=1, padx=5, pady=5)

tk.Button(frame_peca, text="Cadastrar Peça", command=cadastrar_peca).grid(row=3, columnspan=2, pady=10)

# Registro de Trocas
frame_troca = tk.LabelFrame(root, text="Registro de Trocas")
frame_troca.pack(fill="both", expand="yes", padx=10, pady=10)

tk.Label(frame_troca, text="ID do Colaborador:").grid(row=0, column=0, padx=5, pady=5)
entry_colaborador_id = tk.Entry(frame_troca)
entry_colaborador_id.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_troca, text="Código da Peça:").grid(row=1, column=0, padx=5, pady=5)
entry_peca_codigo = tk.Entry(frame_troca)
entry_peca_codigo.grid(row=1, column=1, padx=5, pady=5)

tk.Button(frame_troca, text="Registrar Troca", command=registrar_troca).grid(row=2, columnspan=2, pady=10)

root.mainloop()