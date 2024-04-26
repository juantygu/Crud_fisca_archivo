import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import ttk
from GUI.menu_interfaz.Menu_principal.modulo_gestion.auditor_crud import AuditorCrud


class Gestion:
    def __init__(self,ventana_principal, elementos, interfaz):
        self.ventana_principal = ventana_principal
        self.elementos = elementos
        self.interfaz = interfaz

    def mostrar_gestion(self):
        # ====CALCULO POSICION BOTONES
        altura_pantalla = self.interfaz.window_height
        ancho_pantalla = self.interfaz.window_width
        posicion_x1 = self.interfaz.calcular_posiciones_horizontal_botones(3, 300, ancho_pantalla)
        posicion_y_fila1 = (altura_pantalla / 4)
        posicion_x2 = self.interfaz.calcular_posiciones_horizontal_botones(2, 300, ancho_pantalla)
        posicion_y_fila2 = (altura_pantalla / 2)



        # ======BOTON ATRAS========
        self.elementos.boton_atras = tk.Button(self.ventana_principal, text="ATRAS", font=("Arial", 12, "bold"),
                                               fg="black", bg="white", bd=4, relief=tk.GROOVE, width=15, height=2,
                                               command=self.interfaz.atras)
        self.elementos.boton_atras.place(x=(ancho_pantalla - 250), y=(altura_pantalla - 150))

        # Etiqueta centrada en la parte superior
        self.elementos.label_titulo = tk.Label(self.ventana_principal, text="GESTIÓN DEL ARCHIVO",
                                               font=("Arial", 30, "bold"), fg="black", bg="#E6F7FF")
        self.elementos.label_titulo.pack(side="top", pady=20)  # pady añade un espacio en la parte inferior de la etiqueta

        # ======BOTON EXPEDIENTE========
        self.elementos.boton_expediente = tk.Button(self.ventana_principal, text="Expediente", font=("Arial", 20, "bold"),
                                                 fg="black", bg="white", bd=4, relief=tk.GROOVE, width=300, height=150,
                                                 command=self.on_boton_auditor)
        self.elementos.boton_expediente.place(x=posicion_x1[0], y=posicion_y_fila1)
        self.elementos.imagen_expediente = PhotoImage(file="D:\pythonProject\Crud_fisca_archivo\imagenes\expediente.png")
        self.elementos.imagen_expediente = self.elementos.imagen_expediente.subsample(
            3)  # Ajusta el factor de reducción según sea necesario
        self.elementos.boton_expediente.config(image=self.elementos.imagen_expediente, compound="bottom")

        # ======BOTON CONTRIBUYENTE========
        self.elementos.boton_contribuyente = tk.Button(self.ventana_principal, text="Contribuyente",
                                                    font=("Arial", 20, "bold"),
                                                    fg="black", bg="white", bd=4, relief=tk.GROOVE, width=300,
                                                    height=150,
                                                    command=self.on_boton_auditor)
        self.elementos.boton_contribuyente.place(x=posicion_x1[1], y=posicion_y_fila1)
        self.elementos.imagen_contribuyente = PhotoImage(
            file="D:\pythonProject\Crud_fisca_archivo\imagenes\contrbuyente.png")
        self.elementos.imagen_contribuyente = self.elementos.imagen_contribuyente.subsample(
            3)  # Ajusta el factor de reducción según sea necesario
        self.elementos.boton_contribuyente.config(image=self.elementos.imagen_contribuyente, compound="bottom")

        # ======BOTON AUDITOR========
        self.elementos.boton_auditor = tk.Button(self.ventana_principal, text="Auditor", font=("Arial", 20, "bold"),
                                                 fg="black", bg="white", bd=4, relief=tk.GROOVE, width=300, height=150,
                                                 command=self.on_boton_auditor)
        self.elementos.boton_auditor.place(x=posicion_x1[2], y=posicion_y_fila1)
        self.elementos.imagen_auditor = PhotoImage(file="D:\pythonProject\Crud_fisca_archivo\imagenes\Auditor.png")
        self.elementos.imagen_auditor = self.elementos.imagen_auditor.subsample(
            3)  # Ajusta el factor de reducción según sea necesario
        self.elementos.boton_auditor.config(image=self.elementos.imagen_auditor, compound="bottom")

        # =====BOTON PROCESO =======
        self.elementos.boton_proceso = tk.Button(self.ventana_principal, text="Proceso", font=("Arial", 20, "bold"),
                                                 fg="black", bg="white", bd=4, relief=tk.GROOVE, width=300, height=150,
                                                 command=self.on_boton_auditor)
        self.elementos.boton_proceso.place(x=posicion_x2[0], y=posicion_y_fila2)
        self.elementos.imagen_proceso = PhotoImage(file="D:\pythonProject\Crud_fisca_archivo\imagenes\proceso.png")
        self.elementos.imagen_proceso = self.elementos.imagen_proceso.subsample(
            3)  # Ajusta el factor de reducción según sea necesario
        self.elementos.boton_proceso.config(image=self.elementos.imagen_proceso, compound="bottom")

        #=====BOTON PRESTAMO=====
        self.elementos.boton_prestamo = tk.Button(self.ventana_principal, text="Prestamo", font=("Arial", 20, "bold"),
                                                 fg="black", bg="white", bd=4, relief=tk.GROOVE, width=300, height=150,
                                                 command=self.on_boton_auditor)
        self.elementos.boton_prestamo.place(x=posicion_x2[1], y=posicion_y_fila2)
        self.elementos.imagen_prestamo = PhotoImage(file="D:\pythonProject\Crud_fisca_archivo\imagenes\prestamo.png")
        self.elementos.imagen_prestamo = self.elementos.imagen_prestamo.subsample(
            3)  # Ajusta el factor de reducción según sea necesario
        self.elementos.boton_prestamo.config(image=self.elementos.imagen_prestamo, compound="bottom")


        self.interfaz.estado_actual = "gestion"
        print(self.interfaz.estado_actual)

    def on_boton_auditor(self):
        self.interfaz.borrar_estado_anterior("gestion")
        auditor_crud = AuditorCrud(self.ventana_principal, self.elementos, self.interfaz)
        auditor_crud.mostrar_auditor_crud()

