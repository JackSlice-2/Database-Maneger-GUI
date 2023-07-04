#!/usr/bin/env python3
import tkinter as tk
import sqlite3
from tkinter import messagebox
from fpdf import FPDF

def create_database():
    conn = sqlite3.connect('Banco de Dados +MaisSaude')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pacientes (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        rg TEXT,
        cpf TEXT,
        dia TEXT,
        mes TEXT,
        ano TEXT,
        telefone1 TEXT,
        telefone2 TEXT,
        tipo TEXT,
        cidade TEXT,
        bairro TEXT,
        rua TEXT,
        numero TEXT,
        complemento TEXT
        )
    ''')

    conn.commit()
    conn.close()

def search_pacientes():
    conn = sqlite3.connect('Banco de Dados +MaisSaude')
    cursor = conn.cursor()

    search_by_cpf = cpf_checkbox_var.get()
    search_by_rg = rg_checkbox_var.get()
    cpf_value = cpf_entry.get()
    rg_value = rg_entry.get()

    if not search_by_cpf and not search_by_rg:
        messagebox.showwarning('Warning', 'Please select a search method (CPF or RG).')
        return

    if (search_by_cpf and search_by_rg) or (search_by_cpf and not cpf_value) or (search_by_rg and not rg_value):
        messagebox.showwarning('Warning', 'Please enter the correct search value for the selected search method.')
        return
    
    if search_by_cpf and not search_by_rg:
        query = 'SELECT * FROM Pacientes WHERE cpf=?'
        params = (cpf_value,)
    elif search_by_rg and not search_by_cpf:
        query = 'SELECT * FROM Pacientes WHERE rg=?'
        params = (rg_value,)

    cursor.execute(query, params)
    results = cursor.fetchall()

    if len(results) == 0:
        messagebox.showerror('Error', 'Paciente não existe!')
    else:
        patient_info = 'Search Results:\n\n'
        for row in results:
            patient_info += f"Nome: {row[1]}\n"
            patient_info += f"RG: {row[2]}\n"
            patient_info += f"CPF: {row[3]}\n"
            patient_info += f"Data de Nascimento: {row[4]}/{row[5]}/{row[6]}\n"
            patient_info += f"Telefone(s) de contato: {row[7]} : {row[8]}"
            patient_info += f"Tipo de atendimento: {row[9]}"
            patient_info += f"Endereço: {row[10]}\n{row[11]}\n{row[12]}\n{row[13]}\n{row[14]}\n\n"

        messagebox.showinfo('Search Results', patient_info)

    conn.close()

def download_pdf():
    conn = sqlite3.connect('Banco de Dados +MaisSaude')
    cursor = conn.cursor()

    search_by_cpf = cpf_checkbox_var.get()
    search_by_rg = rg_checkbox_var.get()
    cpf_value = cpf_entry.get()
    rg_value = rg_entry.get()

    if search_by_cpf and search_by_rg:
        query = 'SELECT * FROM Pacientes WHERE cpf=? AND rg=?'
        params = (cpf_value, rg_value)
    elif search_by_cpf:
        query = 'SELECT * FROM Pacientes WHERE cpf=?'
        params = (cpf_value,)
    elif search_by_rg:
        query = 'SELECT * FROM Pacientes WHERE rg=?'
        params = (rg_value,)
    else:
        return

    cursor.execute(query, params)
    results = cursor.fetchall()

    if len(results) == 0:
        messagebox.showerror('Error', 'Patiente não existe!')
    else:
        for row in results:
            pdf = FPDF()
            pdf.set_title('Informação do Paciente')
            pdf.add_page()
            pdf.set_font('Arial', size=12)
            pdf.cell(0, 10, f'Nome: {row[1]}', ln=True)
            pdf.cell(0, 10, f'CPF: {row[3]}', ln=True)
            pdf.cell(0, 10, f'RG: {row[2]}', ln=True)
            pdf.cell(0, 10, f'Data de Nascimento: {row[4]}/{row[5]}/{row[6]}', ln=True)
            pdf.cell(0, 10, f"Telefone(s) de contato: {row[7]} : {row[8]}", ln=True)
            pdf.cell(0, 10, f"Tipo de atendimento: {row[9]}", ln=True)
            pdf.cell(0, 10, f"Endereço: {row[10]}\n{row[11]}\n{row[12]}\n{row[13]}\n{row[14]}", ln=True)
            pdf.output(f'patient_{row[1]}_info.pdf')

        messagebox.showinfo('PDF Baixado', f"PDF do paciente {results[0][1]} baixado com sucesso!")

    conn.close()

def add_paciente():
    nome = nome_entry.get()
    rg = rg_entry2.get()
    cpf = cpf_entry2.get()
    dia = dia_entry.get()
    mes = mes_entry.get()
    ano = ano_entry.get()
    tel1 = telefone1_entry.get()
    tel2 = telefone2_entry.get()
    tipo = tipo_entry.get()
    cidade = cidade_entry.get()
    bairro = bairro_entry.get()
    rua = rua_entry.get()
    num = numero_entry.get()
    comp = complemento_entry.get()

    if nome and rg and cpf and dia and mes and ano and tel1 and tel2 and tipo and cidade and bairro and rua and num and comp:
        conn = sqlite3.connect('Banco de Dados +MaisSaude')
        cursor = conn.cursor()

        cursor.execute('INSERT INTO Pacientes (nome, rg, cpf, dia, mes, ano, telefone1, telefone2, tipo, cidade, bairro, rua, numero, complemento) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                       (nome, rg, cpf, dia, mes, ano, tel1, tel2, tipo, cidade, bairro, rua, num, comp))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Paciente Adcionado com Sucesso!")
        clear_entries()
    else:
        messagebox.showerror("Erro", "Por Favor Preencher TODOS os Campos")

def clear_entries():
    nome_entry.delete(0, tk.END)
    rg_entry2.delete(0, tk.END)
    cpf_entry2.delete(0, tk.END)
    dia_entry.delete(0, tk.END)
    mes_entry.delete(0, tk.END)
    ano_entry.delete(0, tk.END)
    telefone1_entry.delete(0, tk.END)
    telefone2_entry.delete(0, tk.END)
    tipo_entry.delete(0, tk.END)
    cidade_entry.delete(0, tk.END)
    bairro_entry.delete(0, tk.END)
    rua_entry.delete(0, tk.END)
    numero_entry.delete(0, tk.END)
    complemento_entry.delete(0, tk.END)

window = tk.Tk()
window.title('Gerenciador Clinica Médica +Mais Saude')

create_database()

search_label = tk.Label(window, text="Buscar Pacientes:", font=("Arial", 16))
search_label.place(relx=0.01, rely=0.02, anchor="w")

cpf_checkbox_var = tk.IntVar()
cpf_checkbox = tk.Checkbutton(window, text="Search by CPF", variable=cpf_checkbox_var)
cpf_checkbox.place(relx=0.04, rely=0.07, anchor="w")

rg_checkbox_var = tk.IntVar()
rg_checkbox = tk.Checkbutton(window, text="Search by RG", variable=rg_checkbox_var)
rg_checkbox.place(relx=0.25, rely=0.07, anchor="w")

cpf_label = tk.Label(window, text="Buscar CPF:")
cpf_label.place(relx=0.02, rely=0.11, anchor="w")
cpf_entry = tk.Entry(window)
cpf_entry.place(relx=0.15, rely=0.11, anchor="w")

rg_label = tk.Label(window, text="Buscar RG:")
rg_label.place(relx=0.02, rely=0.15, anchor="w")
rg_entry = tk.Entry(window)
rg_entry.place(relx=0.15, rely=0.15, anchor="w")

search_btn = tk.Button(window, text="Search", command=search_pacientes)
search_btn.place(relx=0.47, rely=0.14, anchor="center")

add_label = tk.Label(window, text="Adcionar Pacientes:", font='16')
add_label.place(relx=0.01, rely=0.2, anchor="w")

nome_label = tk.Label(window, text="Nome:")
nome_label.place(relx=0.02, rely=0.25, anchor="w")
nome_entry = tk.Entry(window, width=20)
nome_entry.place(relx=0.09, rely=0.25, anchor="w")

rg_label2 = tk.Label(window, text="RG:")
rg_label2.place(relx=0.36, rely=0.25, anchor="w")
rg_entry2 = tk.Entry(window, width=12)
rg_entry2.place(relx=0.4, rely=0.25, anchor="w")

cpf_label2 = tk.Label(window, text="CPF:")
cpf_label2.place(relx=0.02, rely=0.3, anchor="w")
cpf_entry2 = tk.Entry(window, width=15)
cpf_entry2.place(relx=0.07, rely=0.3, anchor="w")

dia_label = tk.Label(window, text="Data de Nascimento:")
dia_label.place(relx=0.02, rely=0.35, anchor="w")

dia_entry = tk.Entry(window, width=3)
dia_entry.place(relx=0.02, rely=0.4, anchor="w")

slash_label = tk.Label(window, text="-")
slash_label.place(relx=0.07, rely=0.4, anchor="w")

mes_entry = tk.Entry(window, width=3)
mes_entry.place(relx=0.08, rely=0.4, anchor="w")

slash2_nasc_label = tk.Label(window, text="-")
slash2_nasc_label.place(relx=0.13, rely=0.4, anchor="w")

ano_entry = tk.Entry(window, width=5)
ano_entry.place(relx=0.14, rely=0.4, anchor="w")

telefone1_label = tk.Label(window, text="Telefone1:")
telefone1_label.place(relx=0.28, rely=0.3, anchor="w")
telefone1_entry = tk.Entry(window)
telefone1_entry.place(relx=0.39, rely=0.3, anchor="w")

telefone2_label = tk.Label(window, text="Telefone2:")
telefone2_label.place(relx=0.28, rely=0.35, anchor="w")
telefone2_entry = tk.Entry(window)
telefone2_entry.place(relx=0.39, rely=0.35, anchor="w")

tipo_label = tk.Label(window, text="Tipo de \nAtendimento:")
tipo_label.place(relx=0.25, rely=0.4, anchor="w")
tipo_entry = tk.Entry(window)
tipo_entry.place(relx=0.39, rely=0.41, anchor="w")

cidade_label = tk.Label(window, text="Cidade:")
cidade_label.place(relx=0.02, rely=0.46, anchor="w")
cidade_entry = tk.Entry(window, width=15)
cidade_entry.place(relx=0.1, rely=0.46, anchor="w")

bairro_label = tk.Label(window, text="Bairro:")
bairro_label.place(relx=0.31, rely=0.46, anchor="w")
bairro_entry = tk.Entry(window, width=15)
bairro_entry.place(relx=0.38, rely=0.46, anchor="w")

rua_label = tk.Label(window, text="Rua:")
rua_label.place(relx=0.02, rely=0.51, anchor="w")
rua_entry = tk.Entry(window, width=20)
rua_entry.place(relx=0.07, rely=0.51, anchor="w")

numero_label = tk.Label(window, text="N°:")
numero_label.place(relx=0.34, rely=0.51, anchor="w")
numero_entry = tk.Entry(window, width=8)
numero_entry.place(relx=0.38, rely=0.51, anchor="w")

complemento_label = tk.Label(window, text="Complemento:")
complemento_label.place(relx=0.02, rely=0.56, anchor="w")
complemento_entry = tk.Entry(window, width=8)
complemento_entry.place(relx=0.17, rely=0.56, anchor="w")

add_btn = tk.Button(window, text="Adcionar Paciente", command=add_paciente)
add_btn.place(relx=0.17, rely=0.65, anchor="center")

clear_btn = tk.Button(window, text="Clear Entries", command=clear_entries)
clear_btn.place(relx=0.4, rely=0.65, anchor="center")

pdf_btn = tk.Button(window, text="Download PDF", command=download_pdf)
pdf_btn.place(relx=0.15, rely=0.74, anchor="center")

conn = sqlite3.connect('Banco de Dados +MaisSaude')
cursor = conn.cursor()

# Add your application logic and GUI code here

conn.close()
window.geometry('650x550')
window.mainloop()







