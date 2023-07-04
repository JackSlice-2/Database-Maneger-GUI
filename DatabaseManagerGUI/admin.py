#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

# Database Initialization
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create tables
c.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL)''')

# Commit the changes and close the connection
conn.commit()
conn.close()

def create_user():
    username = entry_username.get()
    password = entry_password.get()
    role = combo_role.get()

    if not username or not password:
        messagebox.showwarning("Input Invalido", "Por Favor Preencher TODOS os campos.")
        return

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Check if the username already exists
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    existing_user = c.fetchone()

    if existing_user:
        messagebox.showerror("Erro", "Nome de usuário ja existe. Por Favor crie um novo.")
        conn.close()
        return

    # Insert the new user
    c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
              (username, password, role))
    conn.commit()
    conn.close()

    messagebox.showinfo("Sucesso", "Usuario Criado com Sucesso!")

    # Clear the entry fields
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)

def edit_user():
    username = entry_username2.get()
    password = entry_password2.get()
    role = combo_role2.get()

    if not username or not password:
        messagebox.showwarning("Input Invalido", "Por Favor Preencher TODOS os campos..")
        return

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Check if the username exists
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    existing_user = c.fetchone()

    if not existing_user:
        messagebox.showerror("Erro", "Nome de Usiario NÃO Existe.")
        conn.close()
        return

    # Update the user's password and role
    c.execute("UPDATE users SET password=?, role=? WHERE username=?", (password, role, username))
    conn.commit()
    conn.close()

    messagebox.showinfo("Sucesso", "Usuario Atualizado com Sucesso!")

    # Clear the entry fields
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)

def delete_user():
    username = entry_username4.get()

    if not username:
        messagebox.showwarning("Input Invalido", "Por Faavor Digite um Nome de Usuario.")
        return

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Check if the username exists
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    existing_user = c.fetchone()

    if not existing_user:
        messagebox.showerror("Erro", "Nome de Usuario NÃO existe.")
        conn.close()
        return

    # Delete the user
    c.execute("DELETE FROM users WHERE username=?", (username,))
    conn.commit()
    conn.close()

    messagebox.showinfo("Sucesso", "Usiario Apagado com Sucesso!")

    # Clear the entry fields
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)

def view_user_info(username):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Get user information
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()

    if not user:
        messagebox.showerror("Erro", "Usuario NÃO Encontrado.")
        conn.close()
        return

    messagebox.showinfo("Informaçao do Usuario", f"Nome de Usuario: {user[1]}\nSenha: {user[2]}\nCargo: {user[3]}")
    conn.close()

def show_user_list():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Get all users
    c.execute("SELECT username FROM users")
    users = c.fetchall()

    conn.close()

    user_list = ""
    for user in users:
        user_list += f"- {user[0]}\n"

    messagebox.showinfo("Lista de Funcionarios", user_list)

# Tkinter App
root = tk.Tk()
root.title("Admin App")

# Tab control
tab_control = ttk.Notebook(root)

# Add User Tab
add_user_tab = ttk.Frame(tab_control)
tab_control.add(add_user_tab, text="Adcionar Usuario")

# Username label and entry box
label_username = tk.Label(add_user_tab, text="Nome de Usuario:")
label_username.pack()
entry_username = tk.Entry(add_user_tab)
entry_username.pack()

# Password label and entry box
label_password = tk.Label(add_user_tab, text="Senha:")
label_password.pack()
entry_password = tk.Entry(add_user_tab, show="*")
entry_password.pack()

# Role label and combo box
label_role = tk.Label(add_user_tab, text="Cargo:")
label_role.pack()
combo_role = ttk.Combobox(add_user_tab, values=["doutores", "receptionista"])
combo_role.pack()

# Create user button
create_button = tk.Button(add_user_tab, text="Criar", command=create_user)
create_button.pack()

# Edit User Tab
edit_user_tab = ttk.Frame(tab_control)
tab_control.add(edit_user_tab, text="Editar Usuario")

# Username label and entry box
label_username2 = tk.Label(edit_user_tab, text="Nome de Usuario:")
label_username2.pack()
entry_username2 = tk.Entry(edit_user_tab)
entry_username2.pack()

# Password label and entry box
label_password2 = tk.Label(edit_user_tab, text="Senha:")
label_password2.pack()
entry_password2 = tk.Entry(edit_user_tab, show="*")
entry_password2.pack()

# Role label and combo box
label_role2 = tk.Label(edit_user_tab, text="Cargo:")
label_role2.pack()
combo_role2 = ttk.Combobox(edit_user_tab, values=["doutores", "receptionista"])
combo_role2.pack()

# Edit user button
edit_button = tk.Button(edit_user_tab, text="Editar Usuario", command=edit_user)
edit_button.pack()

# Delete User Tab
delete_user_tab = ttk.Frame(tab_control)
tab_control.add(delete_user_tab, text="Apagar Usuario")

# Username label and entry box
label_username4 = tk.Label(delete_user_tab, text="Nome de Usuario:")
label_username4.pack()
entry_username4 = tk.Entry(delete_user_tab)
entry_username4.pack()

# Delete user button
delete_button = tk.Button(delete_user_tab, text="Apagar Usuario", command=delete_user)
delete_button.pack()

# User List Tab
user_list_tab = ttk.Frame(tab_control)
tab_control.add(user_list_tab, text="Lista de Funcionarios")

# User list button
list_button = tk.Button(user_list_tab, text="Lista de Funcionarios", command=show_user_list)
list_button.pack()

# View user info button (for testing purposes)
view_button = tk.Button(user_list_tab, text="Vizualizar Informaçoes", command=lambda: view_user_info(entry_username.get()))
view_button.pack()

# Pack the tab control
tab_control.pack(expand=1, fill="both")

# Run the Tkinter event loop
root.mainloop()
