#!/usr/bin/env python3

import tkinter as tk
import sqlite3
from tkinter import messagebox

def create_comments_table():
    conn = sqlite3.connect('Doctors_Comments.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors_comments (
        id INTEGER PRIMARY KEY,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        doctor_name TEXT,
        patient_name TEXT,
        patient_rg TEXT,
        patient_cpf TEXT,
        comment TEXT
        )
    ''')

    conn.commit()
    conn.close()

def add_comment():
    doctor_name = doctor_name_entry.get()
    comment = comment_text.get(1.0, tk.END)

    if doctor_name and comment:
        conn = sqlite3.connect('Doctors_Comments.db')
        cursor = conn.cursor()

        cursor.execute('INSERT INTO doctors_comments (doctor_name, patient_name, patient_rg, patient_cpf, comment) VALUES (?,?,?,?,?)',
                       (doctor_name, selected_patient['nome'], selected_patient['rg'], selected_patient['cpf'], comment))
        conn.commit()
        conn.close()
        clear_entries()
    else:
        tk.messagebox.showerror("Error", "Please fill in all fields.")

def clear_entries():
    doctor_name_entry.delete(0, tk.END)
    comment_text.delete(1.0, tk.END)

def view_comments():
    conn = sqlite3.connect('Doctors_Comments.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM doctors_comments WHERE patient_rg=? OR patient_cpf=?', (selected_patient['rg'], selected_patient['cpf']))
    results = cursor.fetchall()

    patient_info = f"Nome: {selected_patient['nome']}\n" \
                   f"RG: {selected_patient['rg']}\n" \
                   f"CPF: {selected_patient['cpf']}\n"

    comments_info = "Doctor Comments:\n\n"
    for row in results:
        comments_info += f"Timestamp: {row[1]}\n"
        comments_info += f"Dr(a).: {row[2]}\n"
        comments_info += f"Commentario: {row[6]}\n"
        comments_info += "---------------------------\n"

    comments_text.delete(1.0, tk.END)
    comments_text.insert(tk.END, patient_info + "\n" + comments_info)

    conn.close()


def search_patient():
    search_term = search_entry.get()

    conn = sqlite3.connect('Banco de Dados +MaisSaude')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Pacientes WHERE rg=? OR cpf=?", (search_term, search_term))
    result = cursor.fetchone()

    if result is not None:
        global selected_patient
        selected_patient = {
            'nome': result[1],
            'rg': result[2],
            'cpf': result[3]
        }

        patient_info = f"Nome: {selected_patient['nome']}\n" \
                       f"RG: {selected_patient['rg']}\n" \
                       f"CPF: {selected_patient['cpf']}\n"

        patient_info_text.delete(1.0, tk.END)
        patient_info_text.insert(tk.END, patient_info)
        add_patient_btn.config(state=tk.NORMAL)
    else:
        tk.messagebox.showinfo("Patient Not Found", "No patient found with the provided CPF or RG.")
        add_patient_btn.config(state=tk.DISABLED)

    conn.close()

window = tk.Tk()
window.title('Doctor Comments')

create_comments_table()

title_label = tk.Label(window, text="Portal do Medico", font="20")
title_label.place(relx=0.02, rely=0.02)

search_label = tk.Label(window, text="Buscar (RG ou CPF):")
search_label.place(relx=0.06, rely=0.1, anchor="w")
search_entry = tk.Entry(window)
search_entry.place(relx=0.225, rely=0.1, anchor="w")

search_btn = tk.Button(window, text="Buscar", command=search_patient)
search_btn.place(relx=0.44, rely=0.1, anchor="w")

doctor_name_label = tk.Label(window, text="Nome do Medico:")
doctor_name_label.place(relx=0.06, rely=0.35, anchor="w")
doctor_name_entry = tk.Entry(window)
doctor_name_entry.place(relx=0.205, rely=0.35, anchor="w")

comment_label = tk.Label(window, text="Commentarios:")
comment_label.place(relx=0.06, rely=0.43, anchor="w")
comment_text = tk.Text(window, height=8, width=30)
comment_text.place(relx=0.19, rely=0.52, anchor="w")

add_comment_btn = tk.Button(window, text="Adcionar Commentario", command=add_comment)
add_comment_btn.place(relx=0.2, rely=0.7, anchor="w")

view_comments_btn = tk.Button(window, text="Vizualizar Histórico", command=view_comments)
view_comments_btn.place(relx=0.685, rely=0.1, anchor="w")

add_patient_btn = tk.Button(window, text="Add Patient", command=add_comment, state=tk.DISABLED)
add_patient_btn.place(relx=0.2, rely=0.8, anchor="w")

patient_info_text = tk.Text(window, height=5, width=33)
patient_info_text.place(relx=0.6, rely=0.8, anchor="w")

comments_text = tk.Text(window, height=19, width=33)
comments_text.place(relx=0.6, rely=0.43, anchor="w")

window.geometry('800x600')
window.mainloop()
