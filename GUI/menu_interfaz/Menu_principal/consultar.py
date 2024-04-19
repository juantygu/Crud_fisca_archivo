import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import ttk


class Consultar:
    def __init__(self, ventana_principal, elementos, interfaz):
        self.ventana_principal = ventana_principal
        self.elementos = elementos
        self.interfaz = interfaz

    def mostrar_consultar(self):
        # Etiqueta centrada en la parte superior
        self.elementos.label_titulo = tk.Label(self.ventana_principal, text="Seleccione el tipo de busqueda",
                                               font=("Arial", 30, "bold"), fg="black", bg="#E6F7FF")
        self.elementos.label_titulo.pack(pady=20)  # pady añade un espacio en la parte inferior de la etiqueta

        self.elementos.boton_atras = tk.Button(self.ventana_principal, text="ATRAS", font=("Arial", 12, "bold"),
                                               fg="black", bg="white", bd=4, relief=tk.GROOVE, width=15, height=2,
                                               command=self.interfaz.atras)
        self.elementos.boton_atras.place(x=900, y=500)
        self.interfaz.estado_actual ="consulta"
        print(self.interfaz.estado_actual)