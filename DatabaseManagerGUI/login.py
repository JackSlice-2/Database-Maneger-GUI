#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox
import sqlite3
import os

def login():
    # Retrieve the input values
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Erro", "Por Favor Preencher TODOS os Campos.")
        return

    # Connect to the database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Check if the user is in the "users" table
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()

    if user:
        role = user[3]
        if role == "doutores":
            messagebox.showinfo("Login Sucesso", "Login Medico com sucesso.")
            conn.close()
            # Redirect to doutores.py
            # Replace the following line with your redirection logic
            os.system("/bin/python3 /home/jackslice2/Desktop/new/medico.py")
        elif role == "receptionista":
            messagebox.showinfo("Login Sucesso", "Login Recepção com sucesso.")
            conn.close()
            # Redirect to receptionista.py
            # Replace the following line with your redirection logic
            os.system("/bin/python3 /home/jackslice2/Desktop/new/receptionista.py")
        elif role == "":
            messagebox.showinfo("Login Sucesso", "Login Adm com sucesso.")
            conn.close()
            # Redirect to receptionista.py
            # Replace the following line with your redirection logic
            os.system("/bin/python3 /home/jackslice2/Desktop/new/admin.py")
    else:
        messagebox.showerror("Login Falhou", "Nome de usuario ou Senha Incorretos.")
        conn.close()

# Create the main Tkinter window
window = tk.Tk()
window.title("Página de Login")

# Create the username label and entry box
username_label = tk.Label(window, text="Nome de usuário:")
username_label.pack()
username_entry = tk.Entry(window)
username_entry.pack()

# Create the password label and entry box
password_label = tk.Label(window, text="Senha:")
password_label.pack()
password_entry = tk.Entry(window, show="*")
password_entry.pack()

# Create the login button
login_button = tk.Button(window, text="Entrar", command=login)
login_button.pack()

# Run the main Tkinter event loop
window.mainloop()
